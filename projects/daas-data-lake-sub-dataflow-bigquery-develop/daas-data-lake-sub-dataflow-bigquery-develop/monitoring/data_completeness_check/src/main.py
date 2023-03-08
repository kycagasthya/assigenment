"""
Cloud Function that compares records from main and raw dump tables,
stores the difference (missed records) into BQ and send needed metrics
"""
import datetime
import logging
import os
from typing import List
from typing import Dict

import yaml
from google.api_core.exceptions import NotFound
from google.cloud import bigquery
from google.cloud import monitoring_v3
from google.cloud.bigquery import QueryJobConfig
from google.cloud.bigquery.table import RowIterator

CONFIG_FILE_NAME = 'config.yml'
SLO_SERVICE_LABEL = 'slo'
SERVICE_BQ_LABEL_KEY = 'service'
GLOBAL_MONITORING_RESOURCE_TYPE = 'global'
DATA_SOURCE_LABEL_NAME = 'data_source'
DATA_COMPLETENESS_LABEL_NAME = 'data_completeness'
RECORDS_TYPE_LABEL_NAME = 'records_type'

RECORDS_TYPE_ALL_LABEL_NAME = 'all_records'
RECORDS_TYPE_MISSED_LABEL_NAME = 'missed_records'
RECORDS_TYPE_SUCCEEDED_LABEL_NAME = 'succeeded_records'

END_DT_TIME_SHIFT = datetime.timedelta(hours=1)
CALCULATION_RANGE = datetime.timedelta(hours=8)
PARTITION_TIME_BUFFER = datetime.timedelta(hours=1)

BATCH_SIZE = 100

MISSED_RECORDS_METRIC_TYPE_TEMPLATE = "custom.googleapis.com/missed_records__{client_name_underscored}"
RAW_RECORDS_METRIC_TYPE_TEMPLATE = "custom.googleapis.com/raw_records__{client_name_underscored}"
DATA_COMPLETENESS_METRIC_TYPE_TEMPLATE = "custom.googleapis.com/data_completeness__{client_name_underscored}"
RECORDS_TRACKING_METRIC_TYPE_TEMPLATE = "custom.googleapis.com/records_tracking__{client_name_underscored}"

RAW_COUNT_QUERY = """
SELECT
  COUNT(*) as count_number
FROM
  `{project_id}.raw_datalake_{client_name_underscored}.raw_{source_name}`
WHERE
  _PARTITIONTIME >= '{start_partition_dt}' 
  AND publish_time >= '{start_dt}'
  AND publish_time < '{end_dt}'
"""

DIFF_QUERY_TEMPLATE = """
SELECT
  message_id
FROM
  `{project_id}.raw_datalake_{client_name_underscored}.raw_{source_name}`
WHERE
  _PARTITIONTIME >= '{start_partition_dt}' 
  AND publish_time >= '{start_dt}'
  AND publish_time < '{end_dt}'
  
EXCEPT DISTINCT

SELECT
  __pubsub_message_id
FROM
  `{project_id}.datalake_{client_name_underscored}.{source_name}`
WHERE
  _PARTITIONTIME >= '{start_partition_dt}' 
  AND __publish_timestamp >= '{start_dt}'
  AND __publish_timestamp < '{end_dt}'
  
EXCEPT DISTINCT

SELECT
  __pubsub_message_id
FROM
  `{project_id}.dl_service.ingest_errors`
WHERE
  _PARTITIONTIME >= '{start_partition_dt}' 
  AND __publish_timestamp >= '{start_dt}'
  AND __publish_timestamp < '{end_dt}'
"""


def main(request):
    """
    Main entry point to the Cloud Function
    :param request: HTTP request object.
    """

    logging.basicConfig(level=logging.INFO)

    GCP_PROJECT = os.getenv('GCP_PROJECT')
    MISSED_RECORDS_BQ_DATASET = os.getenv('MISSED_RECORDS_BQ_DATASET')
    MISSED_RECORDS_BQ_TABLE_NAME = os.getenv('MISSED_RECORDS_BQ_TABLE_NAME')
    missed_records_bq_table = f'{GCP_PROJECT}.{MISSED_RECORDS_BQ_DATASET}.{MISSED_RECORDS_BQ_TABLE_NAME}'

    bq_client = bigquery.Client()
    metric_service_client = monitoring_v3.MetricServiceClient()

    current_sdt = datetime.datetime.utcnow()
    end_dt = current_sdt.replace(minute=0, second=0, microsecond=0) - END_DT_TIME_SHIFT
    start_dt = end_dt - CALCULATION_RANGE
    start_partition_dt = start_dt - PARTITION_TIME_BUFFER

    config = load_yaml(CONFIG_FILE_NAME)

    bq_job_config = QueryJobConfig()
    bq_job_config.labels = {SERVICE_BQ_LABEL_KEY: SLO_SERVICE_LABEL}

    monitoring_start_time_dict = monitoring_time_interval_value_dict_from_dt(start_dt)
    monitoring_end_time_dict = monitoring_time_interval_value_dict_from_dt(end_dt)

    for client_name, sources in config.items():
        logging.info(f"Working with {client_name} sources")
        client_name_underscored = client_name.replace('-', '_')
        source_raw_counts = {}
        source_missed_counts = {}
        for source_name in sources:
            logging.info(f"Working with {client_name}:{source_name}")
            query_params = {'project_id': GCP_PROJECT,
                            'client_name': client_name,
                            'client_name_underscored': client_name_underscored,
                            'source_name': source_name,
                            'start_partition_dt': str(start_partition_dt),
                            'start_dt': str(start_dt),
                            'end_dt': str(end_dt)}
            try:
                raw_count_result = get_raw_records_count_result(bq_client=bq_client,
                                                                bq_job_config=bq_job_config,
                                                                **query_params)

                diff_result = get_diff_result(bq_client=bq_client,
                                              bq_job_config=bq_job_config,
                                              **query_params)
            except NotFound:
                logging.warning(f"BQ table for {client_name}:{source_name} is not found")
            except Exception as exception:
                logging.error(exception)
                exit(1)
            else:
                raw_records_count = get_raw_records_count(raw_count_result)
                logging.debug(f"Found {raw_records_count} raw records for {client_name}:{source_name}")
                source_raw_counts[source_name] = raw_records_count
                missed_records_counts = dump_missed_records_and_return_count(bq_client, diff_result, client_name,
                                                                             source_name, missed_records_bq_table)

                logging.debug(f"Found {missed_records_counts} missed records for {client_name}:{source_name}")
                source_missed_counts[source_name] = missed_records_counts
        add_metrics(metric_service_client=metric_service_client,
                    project_id=GCP_PROJECT,
                    client_name_underscored=client_name_underscored,
                    monitoring_start_time_dict=monitoring_start_time_dict,
                    monitoring_end_time_dict=monitoring_end_time_dict,
                    source_raw_counts=source_raw_counts,
                    source_missed_counts=source_missed_counts)

    return 'Success!'


def add_metrics(metric_service_client: monitoring_v3.MetricServiceClient, project_id: str,
                client_name_underscored: str, monitoring_start_time_dict: Dict, monitoring_end_time_dict: Dict,
                source_raw_counts: Dict, source_missed_counts: Dict):
    """
    Adds 4 metrics to GCP Monitoring: missed records count, raw_records count, data completeness
    and records tracking

    :param monitoring_v3.MetricServiceClient metric_service_client: GCP Monitoring client
    :param str project_id: GCP project id
    :param str client_name_underscored: client name underscored
    :param Dict monitoring_start_time_dict: monitoring time interval start time dict
    :param Dict monitoring_end_time_dict: monitoring time interval end time dict
    :param Dict source_raw_counts: dictionary with source names and raw records counts
    :param Dict source_missed_counts: dictionary with source names and missed records counts
    """
    end_time_dict = {"end_time": monitoring_end_time_dict}
    start_end_time_dict = {"start_time": monitoring_start_time_dict, "end_time": monitoring_end_time_dict}

    missed_records_metric_type = MISSED_RECORDS_METRIC_TYPE_TEMPLATE.format(
        client_name_underscored=client_name_underscored)

    add_metric(metric_service_client, project_id, missed_records_metric_type,
               end_time_dict, DATA_SOURCE_LABEL_NAME, source_missed_counts)

    raw_records_metric_type = RAW_RECORDS_METRIC_TYPE_TEMPLATE.format(
        client_name_underscored=client_name_underscored)
    add_metric(metric_service_client, project_id, raw_records_metric_type,
               end_time_dict, DATA_SOURCE_LABEL_NAME, source_raw_counts)

    source_raw_counts_sum = sum(source_raw_counts.values())
    source_missed_counts_sum = sum(source_missed_counts.values())
    source_succeeded_counts_sum = source_raw_counts_sum - source_missed_counts_sum

    if source_raw_counts_sum > 0:
        completeness_value = (source_raw_counts_sum - source_missed_counts_sum) / source_raw_counts_sum
    else:
        completeness_value = 1.0
    data_completeness_metric_type = DATA_COMPLETENESS_METRIC_TYPE_TEMPLATE.format(
        client_name_underscored=client_name_underscored)
    add_metric(metric_service_client, project_id, data_completeness_metric_type,
               end_time_dict, DATA_COMPLETENESS_LABEL_NAME,
               {DATA_COMPLETENESS_LABEL_NAME: float(completeness_value)})

    records_tracking_metric_type = RECORDS_TRACKING_METRIC_TYPE_TEMPLATE.format(
        client_name_underscored=client_name_underscored)
    labels_and_points = {
        RECORDS_TYPE_ALL_LABEL_NAME: source_raw_counts_sum,
        RECORDS_TYPE_SUCCEEDED_LABEL_NAME: source_succeeded_counts_sum,
        RECORDS_TYPE_MISSED_LABEL_NAME: source_missed_counts_sum
    }
    add_metric(metric_service_client, project_id, records_tracking_metric_type,
               start_end_time_dict, RECORDS_TYPE_LABEL_NAME, labels_and_points)


def add_metric(metric_service_client: monitoring_v3.MetricServiceClient,
               project_id: str, metric_type: str, monitoring_time_dict: Dict,
               label_name: str, labels_and_points: Dict):
    """
    Adds global custom metric to GCP Monitoring based on provided labels, time and point

    :param monitoring_v3.MetricServiceClient metric_service_client: GCP Monitoring client
    :param str project_id: GCP project id
    :param str metric_type: metric type value
    :param Dict monitoring_time_dict: monitoring time interval dict
    :param str label_name: metric label name
    :param Dict labels_and_points: dictionary of label values and point values
    """
    series_list = []
    for label_value, point_value in labels_and_points.items():
        series = monitoring_v3.TimeSeries()
        series.metric.type = metric_type
        series.resource.type = GLOBAL_MONITORING_RESOURCE_TYPE
        series.resource.labels["project_id"] = project_id
        series.metric.labels[label_name] = label_value
        interval = monitoring_v3.TimeInterval(monitoring_time_dict)
        if isinstance(point_value, int):
            point_value_type = "int64_value"
        elif isinstance(point_value, float):
            point_value_type = "double_value"
        else:
            raise Exception('Not supported point type')
        point = monitoring_v3.Point({"interval": interval, "value": {point_value_type: point_value}})
        series.points = [point]
        logging.info(f'{metric_type}, {label_value}, {point_value}')
        series_list.append(series)
    project_name = f'projects/{project_id}'
    metric_service_client.create_time_series(name=project_name, time_series=series_list)
    logging.info(f"Series list has been sent to metric: {metric_type}")


def dump_missed_records_and_return_count(bq_client: bigquery.Client,
                                         missed_records_job_result: RowIterator,
                                         client_name: str, source_name: str,
                                         missed_records_bq_table: str) -> int:
    """
    Counts missed records and dumps them into BQ table

    :param bigquery.Client bq_client: BQ client
    :param RowIterator missed_records_job_result: missed records query result RowIterator
    :param str client_name: data client name
    :param str source_name: data source name
    :param str missed_records_bq_table: BQ table to dump missed records
    :return int: missed records count
    """
    missed_records_batch = []
    missed_records_counter = 0
    for result_row in missed_records_job_result:
        missed_message_id = result_row.get('message_id')
        missed_records_batch.append(
            create_missed_record_entity(missed_message_id, client_name, source_name))
        if len(missed_records_batch) >= BATCH_SIZE:
            dump_missed_records_into_bq(bq_client, missed_records_bq_table, missed_records_batch)
            missed_records_batch = []
        missed_records_counter += 1
    if missed_records_counter > 0:
        logging.warning(f"Found {missed_records_counter} missed records for {client_name}:{source_name}")
    else:
        logging.info(f"Data source {client_name}:{source_name} "
                     f"does not have missed records for the last {CALCULATION_RANGE} hours")
    dump_missed_records_into_bq(bq_client, missed_records_bq_table, missed_records_batch)
    return missed_records_counter


def get_raw_records_count(raw_count_job_result: RowIterator) -> int:
    """
    Fetches raw records count from query result RowIterator

    :param RowIterator raw_count_job_result: query result RowIterator
    :return int: raw records count
    """
    return next(iter(raw_count_job_result)).get('count_number')


def get_raw_records_count_result(bq_client: bigquery.Client,
                                 bq_job_config: bigquery.QueryJobConfig, **query_params):
    """
    Runs raw data count query and returns query result RowIterator

    :param bigquery.Client bq_client: BQ client
    :param bigquery.QueryJobConfig bq_job_config: BQ job configuration
    :param query_params: parameters to build a query
    :return RowIterator: query result RowIterator
    """
    raw_count_query = RAW_COUNT_QUERY.format(
        project_id=query_params['project_id'],
        client_name=query_params['client_name'],
        client_name_underscored=query_params['client_name_underscored'],
        source_name=query_params['source_name'],
        start_partition_dt=query_params['start_partition_dt'],
        start_dt=query_params['start_dt'],
        end_dt=query_params['end_dt'],
    )
    return get_query_result(bq_client, bq_job_config, query_params['project_id'], raw_count_query)


def get_diff_result(bq_client: bigquery.Client,
                    bq_job_config: bigquery.QueryJobConfig, **query_params) -> RowIterator:
    """
    Runs missed records detection query and returns query result RowIterator

    :param bigquery.Client bq_client: BQ client
    :param bigquery.QueryJobConfig bq_job_config: BQ job configuration
    :param query_params: parameters to build a query
    :return RowIterator: query result RowIterator
    """
    diff_query = DIFF_QUERY_TEMPLATE.format(
        project_id=query_params['project_id'],
        client_name=query_params['client_name'],
        client_name_underscored=query_params['client_name_underscored'],
        source_name=query_params['source_name'],
        start_partition_dt=query_params['start_partition_dt'],
        start_dt=query_params['start_dt'],
        end_dt=query_params['end_dt'],
    )
    return get_query_result(bq_client, bq_job_config, query_params['project_id'], diff_query)


def get_query_result(bq_client: bigquery.Client,
                     bq_job_config: bigquery.QueryJobConfig,
                     project_id: str,
                     query: str) -> RowIterator:
    """
    Runs BQ query and returns query result RowIterator

    :param bigquery.Client bq_client: BQ client
    :param bigquery.QueryJobConfig bq_job_config: BQ job configuration
    :param str project_id: GCP project id
    :param str query: query to run
    :return RowIterator: query result RowIterator
    """
    logging.debug(f"Running query:\n{query}")
    job = bq_client.query(query=query, project=project_id, job_config=bq_job_config)
    diff_result = job.result()
    return diff_result


def load_yaml(yaml_path: str) -> Dict:
    """
    Loads YAML file content as dict

    :param str yaml_path: YAML file local path
    :return dict: loaded YAML content
    """
    with open(yaml_path, "r") as stream:
        return yaml.safe_load(stream)


def dump_missed_records_into_bq(bq_client: bigquery.Client, table_id: str, missed_records_to_upload: List[dict]):
    """
    Dumps missed records entities batch into BQ table

    :param bigquery.Client bq_client: BigQuery client
    :param str table_id: BigQuery table id to write results
    :param List[dict] missed_records_to_upload: list of missed records entities to upload
    """
    if len(missed_records_to_upload) > 0:
        errors = bq_client.insert_rows_json(table_id, missed_records_to_upload)
        if len(errors) > 0:
            logging.error(f"Found {len(errors)} errors during insertion of missed errors into BQ")


def create_missed_record_entity(message_id: str, client_name: str, source_name: str) -> Dict:
    """
    Creates an entity for writing missed record info into BQ

    :param str message_id: PubSub message id of the missed record
    :param str client_name: client name
    :param str source_name: source name
    :return dict: missed record entity dict
    """
    return {
        "pubsub_message_id": message_id,
        "reprocessed": False,
        "reprocess_timestamp": None,
        "__client_name": client_name,
        "__source_name": source_name,
        "__ingest_timestamp": 'AUTO',
    }


def monitoring_time_interval_value_dict_from_dt(dt: datetime.datetime) -> Dict:
    """
    Generates GCP Monitoring time interval value dictionary from datetime
    :param datetime dt: input datetime value
    :return Dict[str, int]: GCP Monitoring time interval value dictionary
    """
    ts = dt.timestamp()
    seconds = int(ts)
    nanos = int((ts - seconds) * 10 ** 9)
    return {"seconds": seconds, "nanos": nanos}
