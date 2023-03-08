"""
Cloud Function script that counts new data from Snowflake and BigQuery
and stores count results into separate BigQuery table
"""
import os
import datetime
import logging

from dataclasses import dataclass
from typing import Any, List, Tuple

import yaml
from google.cloud import bigquery
from google.cloud.bigquery.job import QueryJob
from google.api_core.exceptions import NotFound
from google.cloud import logging as gcp_logging
from google.cloud import logging_v2
from google.logging.type import log_severity_pb2 as log_severity
import snowflake.connector
from snowflake.connector.cursor import SnowflakeCursor

DT_FORMAT = '%Y-%m-%dT%H:%M:%S%z'
CONFIG_FILE = 'config.yml'

SNOWFLAKE_CONFIG_KEY = 'snowflake'
BQ_CONFIG_KEY = 'bq'
OMITTED_CLIENTS_KEY = 'omitted_clients'

RESULT_BQ_DATASET_NAME = 'dl_service'
RESULT_BQ_TABLE_NAME = 'count_validation'


class DBException(Exception):
    """
    A custom exception for handling non-existing tables
    """
    def __init__(self):
        super().__init__()


def main(request):
    """
    Main entry point to the Cloud Function
    :param request: HTTP request object.
    """

    logging.basicConfig(level=logging.INFO)

    BQ_PROJECT_ID = os.getenv('BQ_PROJECT_ID')
    SF_USER = os.getenv('SF_USER')
    SF_PASSWORD = os.getenv('SF_PASSWORD')
    SF_ACCOUNT = os.getenv('SF_ACCOUNT')
    SF_WAREHOUSE = os.getenv('SF_WAREHOUSE')
    LOGGER_NAME = "ValidationLogger"

    config = read_yaml(CONFIG_FILE)
    start_ts, end_ts = get_start_end_ts()

    gcp_log_client = gcp_logging.Client(project=BQ_PROJECT_ID)
    gcp_logger = logging.getLogger(LOGGER_NAME)
    gcp_logger.setLevel(logging.INFO)

    cloud_hdlr = logging_v2.handlers.CloudLoggingHandler(gcp_log_client, name=LOGGER_NAME)
    cloud_hdlr.setFormatter(
        logging.Formatter('[%(filename)s->%(className)s->%(callFuncName)s()]:  %(message)s'))
    if not gcp_logger.handlers:
        gcp_logger.addHandler(cloud_hdlr)

    bq_client = BqClient(project_id=BQ_PROJECT_ID, gcp_logger=gcp_logger)
    snowflake_client = SnowflakeClient(
        user=SF_USER,
        password=SF_PASSWORD,
        account=SF_ACCOUNT,
        warehouse=SF_WAREHOUSE,
        gcp_logger=gcp_logger
    )

    results = []
    ingest_timestamp = datetime.datetime.utcnow().strftime(DT_FORMAT)
    for client, source, bq_query_config, snowflake_query_config in query_config_iterator(config, start_ts, end_ts):
        try:
            bq_count = bq_client.get_day_count(bq_query_config)
            snowflake_count = snowflake_client.get_day_count(snowflake_query_config)
            diff_absolute = bq_count - snowflake_count
            diff_relative = diff_absolute / max(bq_count, snowflake_count) if diff_absolute != 0 else 0
            results.append({
                'source': source,
                'client': client,
                'start_ts': start_ts,
                'end_ts': end_ts,
                'bq_count': bq_count,
                'snowflake_count': snowflake_count,
                'diff_absolute': diff_absolute,
                'diff_relative': round(diff_relative, 3),
                '__ingest_timestamp': ingest_timestamp
            })
        except DBException as db_ect:
            continue

    bq_client.append_rows(BQ_PROJECT_ID, RESULT_BQ_DATASET_NAME, RESULT_BQ_TABLE_NAME, results)
    return 'Success!'


@dataclass
class QueryConfig:
    """
    Dataclass which represents parameters
    for the data count query
    """
    client: str
    source: str
    time_column_to_filter: str
    start_ts: str
    end_ts: str


class DBClient:
    """
    Abstract class for wrapping interactions with DB
    """

    def build_day_count_query(self, table_name: str, start_ts: str,
                              end_ts: str, time_column_to_filter: str) -> str:
        """
        Builds query for fetching count of the records in time range
        :param str table_name: DB table name
        :param str start_ts: time range start timestamp formatted according to DT_FORMAT
        :param str end_ts:  time range end timestamp formatted according to DT_FORMAT
        :param str time_column_to_filter: table column to apply time filtering
        :return str: query string
        """
        raise Exception('build_query is not implemented')

    def run_query(self, query: str) -> Any:
        """
        Executes query in DB
        :param str query: query to execute
        :return: query result
        """
        raise Exception('run_query is not implemented')

    def get_day_count(self, query_config: QueryConfig) -> int:
        """
        Fetches records day count info from DB according to the provided QueryConfig
        :param QueryConfig query_config: query parameter to fetch day count info
        :return int: day count info
        """
        raise Exception('get_day_count is not implemented')

    def log_gcp_msg(self, msg: str, severity: int, method_name: str) -> None:
        """
        Logs error message in GCP Logging end enriches it with extra param
        :param str msg: message to be logged
        :param int severity: the severity of the message based on
                             google.logging.type.log_severity_pb2 constants
        :param str method_name: name of the method that triggered logging
        :return None
        """
        raise Exception('log_gcp_error is not implemented')


class BasicLoggingDBClient(DBClient):
    """
    A basic wrapper class implementing one of the methods of DBClient interface
    """
    def __init__(self, gcp_logger):
        self.gcp_logger = gcp_logger
        self.logger_extra_dict = {'className': BasicLoggingDBClient.__name__}

    def log_gcp_msg(self, msg: str, severity: int, method_name: str = None) -> None:
        """
        Logs error message in GCP Logging end enriches it with extra param
        :param str msg: message to be logged
        :param int severity: the severity of the message based on
                             google.logging.type.log_severity_pb2 constants
        :param str method_name: name of the method that triggered logging
        :return None
        """
        local_logger_extra = self.logger_extra_dict
        local_logger_extra['callFuncName'] = method_name if method_name else BasicLoggingDBClient.log_gcp_msg.__name__
        self.gcp_logger.log(severity, msg, extra=local_logger_extra)


class SnowflakeClient(BasicLoggingDBClient):
    """
    Wrapper class to work with Snowflake DB

    :param str user: Snowflake user
    :param str password: Snowflake user password
    :param str account: Snowflake account name
    :param str warehouse: Snowflake warehouse name
    :param logging.Logger gcp_logger: logger instance with CloudLoggingHandler set up
    """

    def __init__(self, user: str, password: str, account: str, warehouse: str,
                 gcp_logger: logging.Logger):
        super().__init__(gcp_logger)
        self.logger_extra_dict = {'className': SnowflakeClient.__name__}
        self.sf_connection = snowflake.connector.connect(
            user=user, password=password, account=account, warehouse=warehouse
        )
        self.sf_cursor = self.sf_connection.cursor()
        self.sf_cursor.execute("USE ROLE ETL_ROLE")
        self.sf_cursor.execute("alter session set timezone = 'UTC'")

    def build_day_count_query(self, table_name: str, start_ts: str,
                              end_ts: str, time_column_to_filter: str) -> str:
        """
        Builds Snowflake query for fetching count of the records in time range
        :param str table_name: DB table name
        :param str start_ts: time range start timestamp formatted according to DT_FORMAT
        :param str end_ts:  time range end timestamp formatted according to DT_FORMAT
        :param str time_column_to_filter: table column to apply time filtering
        :return str: query string
        """
        return f"""
SELECT 
    COUNT(*) as c 
FROM 
    {table_name}
WHERE 
    {time_column_to_filter} >= '{start_ts}'
    and {time_column_to_filter} < '{end_ts}'
    """

    def run_query(self, query: str) -> SnowflakeCursor:
        """
        Executes query in Snowflake DB
        :param str query: query to execute
        :return SnowflakeCursor: query result
        """
        logging.debug(f"Running Snowflake: \n{query}")
        return self.sf_cursor.execute(query)

    def get_day_count(self, query_config: QueryConfig) -> int:
        """
        Fetches records day count info from Snowflake DB according to the provided QueryConfig
        :param QueryConfig query_config: query parameter to fetch day count info
        :return int: day count info
        """
        table_name = f'{query_config.client}.DATA_LAKE.{query_config.source}'
        try:
            result = self.run_query(self.build_day_count_query(table_name,
                                                               query_config.start_ts,
                                                               query_config.end_ts,
                                                               query_config.time_column_to_filter))
            row = result.fetchone()
            if row and len(row) > 0:
                return int(row[0])
        except snowflake.connector.errors.ProgrammingError as not_found_exc:
            self.log_gcp_msg(msg=f'Client={query_config.client}, source={query_config.source} does not exist '
                                 f'in on the client side: {not_found_exc.raw_msg}.',
                             severity=log_severity.ERROR,
                             method_name=SnowflakeClient.get_day_count.__name__)
            raise DBException
        except snowflake.connector.Exception as sf_e:
            self.log_gcp_msg(msg=f'Client={query_config.client}, source={query_config.source} returned '
                                 f'and error on the client side: {sf_e.raw_msg}.',
                             severity=log_severity.ERROR,
                             method_name=SnowflakeClient.get_day_count.__name__)
            raise DBException


class BqClient(BasicLoggingDBClient):
    """
    Wrapper class to work with BigQuery DB

    :param str project_id: GCP project id to work with BQ
    :param logging.Logger gcp_logger: logger instance with CloudLoggingHandler set up
    """

    def __init__(self, project_id: str, gcp_logger: logging.Logger):
        super().__init__(gcp_logger)
        self.logger_extra_dict = {'className': BqClient.__name__}
        self.bq_client = bigquery.Client(project=project_id)
        self.project_id = project_id

    def build_day_count_query(self, table_name: str, start_ts: str,
                              end_ts: str, time_column_to_filter: str) -> str:
        """
        Builds Snowflake query for fetching count of the records in time range
        :param str table_name: DB table name
        :param str start_ts: time range start timestamp formatted according to DT_FORMAT
        :param str end_ts:  time range end timestamp formatted according to DT_FORMAT
        :param str time_column_to_filter: table column to apply time filtering
        :return str: query string
        """
        start_ts_parts = start_ts.split('T')
        start_ts_midnight = f"{start_ts_parts[0]}T00:00:00"
        return f"""
SELECT 
    COUNT(*) as c 
FROM 
    `{table_name}`
WHERE 
    {time_column_to_filter} >= '{start_ts}'
    and {time_column_to_filter} < '{end_ts}'
    and _PARTITIONTIME >= '{start_ts_midnight}'
            """

    def run_query(self, query: str) -> QueryJob:
        """
        Executes query in BigQuery DB
        :param str query: query to execute
        :return QueryJob: query result
        """
        logging.debug(f"Running BQ: \n{query}")
        return self.bq_client.query(query)

    def get_day_count(self, query_config: QueryConfig) -> int:
        """
        Fetches records day count info from BigQuery DB according to the provided QueryConfig
        :param QueryConfig query_config: query parameter to fetch day count info
        :return int: day count info
        """
        dataset_name = f'datalake_{query_config.client}'.replace('-', '_')
        table_name = f'{self.project_id}.{dataset_name}.{query_config.source}'
        try:
            query_job = self.run_query(self.build_day_count_query(table_name,
                                                                  query_config.start_ts,
                                                                  query_config.end_ts,
                                                                  query_config.time_column_to_filter))
            row = next(iter(query_job), None)
            if row and len(row) > 0:
                return int(row[0])
        except NotFound as not_found_exc:
            self.log_gcp_msg(msg=f'Client={query_config.client}, source={query_config.source} does not exist '
                                 f'in subscription project {self.project_id}',
                             severity=log_severity.ERROR,
                             method_name=BqClient.get_day_count.__name__)
            raise DBException

    def append_rows(self, project_id: str, dataset_name: str, table_name: str, records: List[dict]):
        """
        Appends new records to the BigQuery table
        :param str project_id: GCP project id to work with BQ
        :param str dataset_name: BigQuery dataset name
        :param str table_name: BigQuery table name
        :param records: list of records in form of dictionaries
        :return: append job result
        """
        table_id = f"{project_id}.{dataset_name}.{table_name}"

        job_config = bigquery.LoadJobConfig(source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON)
        job = self.bq_client.load_table_from_json(records, table_id, job_config=job_config)

        result = job.result()
        return result


def read_yaml(yaml_path: str) -> dict:
    """
    Reads YAML file as dictionary
    :param str yaml_path: path to YAML file
    :return dict: yaml dictionary representation
    """
    with open(yaml_path, "r") as f:
        content = yaml.safe_load(f)
    return content


def get_start_end_ts() -> Tuple[str, str]:
    """
    Prepares start and end timestamps formatted according to DT_FORMAT.
    End timestamp - the beginning of previous hour
    Start timestamp - (End timestamp) - 24 hours
    :return Tuple[str, str]: pair of Start timestamp and End timestamp
    """
    end_ts = (datetime.datetime.utcnow() - datetime.timedelta(hours=1)). \
        replace(minute=0, second=0, microsecond=0)
    start_ts = end_ts - datetime.timedelta(hours=24)
    return start_ts.strftime(DT_FORMAT), end_ts.strftime(DT_FORMAT)


def query_config_iterator(config: dict, start_ts: str, end_ts: str):
    """
    Generator function that provides query configurations
    for Snowflake and BigQuery databases according
    to the provided configuration dictionary
    :param dict config: configuration dictionary
    :param str start_ts: time range start timestamp formatted according to DT_FORMAT
    :param str end_ts:  time range end timestamp formatted according to DT_FORMAT
    :return generator: client name, source name, BQ and Snowflake query configurations
    """
    for client, client_data in config['clients'].items():
        for source, source_data in [source_tuple for source_tuple in config['sources'].items() if
                                    client not in source_tuple[1].get(OMITTED_CLIENTS_KEY, list())]:
            bq_query_config = QueryConfig(client=client_data[BQ_CONFIG_KEY],
                                          source=source_data[BQ_CONFIG_KEY]['table_name'],
                                          time_column_to_filter=source_data[BQ_CONFIG_KEY][
                                              'time_column_to_filter'],
                                          start_ts=start_ts,
                                          end_ts=end_ts)
            snowflake_query_config = QueryConfig(client=client_data[SNOWFLAKE_CONFIG_KEY],
                                                 source=source_data[SNOWFLAKE_CONFIG_KEY]['table_name'],
                                                 time_column_to_filter=source_data[SNOWFLAKE_CONFIG_KEY][
                                                     'time_column_to_filter'],
                                                 start_ts=start_ts,
                                                 end_ts=end_ts)
            yield client, source, bq_query_config, snowflake_query_config
