from google import pubsub_v1
from google.api import metric_pb2 as ga_metric
from google.cloud import bigquery
from google.cloud import monitoring_v3
from utils.github import download_repo, check_workflow_run
from utils.secret import access_secret_version

import os
import sys
import time
import yaml


def client_enabled(config: dict) -> bool:
    return True if config.get('enabled', False) == True else False


def get_topics(config: dict) -> list:
    return [f"{config['client_id']}-{config['sources'][source]['source_name']}-{config['sources'][source]['schema_version']}" for source in config['sources']]


def get_tables(config: dict) -> list:
    return [config['tables'][table]['table_id'] for table in config['tables']]


def count_bigquery(project: str, vendor: str) -> list:
    """
    Count BigQuery tables in a single Datalake dataset

    :param vendor: client ID
    :return: the number of tables found
    """
    client = bigquery.Client()

    dataset_id = f"{project}.datalake_{vendor}"

    tables = client.list_tables(dataset_id)

    return [table.table_id for table in tables]


def count_pubsub(project: str) -> list:
    """
    Count Pub/Sub topics within the project

    :return: the number of topics found
    """
    client = pubsub_v1.PublisherClient()

    request = pubsub_v1.ListTopicsRequest(
        project=f"projects/{project}",
    )
    topics = client.list_topics(request=request)

    return [topic.name.split('/')[-1] for topic in topics]


def sort_pubsub_vendor(vendor: str, topics_total: list) -> list:
    return [topic for topic in topics_total if topic.startswith(vendor)]


def create_metric_descriptor(project: str):
    """
    Create metric descriptor only
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project}"
    descriptor = ga_metric.MetricDescriptor()
    descriptor.type = "custom.googleapis.com/datalake_availability"
    descriptor.metric_kind = ga_metric.MetricDescriptor.MetricKind.GAUGE
    descriptor.value_type = ga_metric.MetricDescriptor.ValueType.DOUBLE
    descriptor.description = "Datalake availability custom metric."

    descriptor = client.create_metric_descriptor(
        name=project_name, metric_descriptor=descriptor
    )
    print("Created {}.".format(descriptor.name))


def send_metric(project: str, value: int):
    """
    Create a gauge custom metric

    :param value: metric current value
    """
    client = monitoring_v3.MetricServiceClient()

    series = monitoring_v3.TimeSeries()
    series.metric.type = "custom.googleapis.com/datalake_availability"
    series.resource.type = "global"
    series.resource.labels["project_id"] = project
    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10 ** 9)
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {
                "seconds": seconds,
                "nanos": nanos
            }
        }
    )
    point = monitoring_v3.Point(
        {
            "interval": interval,
            "value": {
                "double_value": value
            }
        }
    )
    series.points = [point]
    client.create_time_series(name=f"projects/{project}", time_series=[series])


def run(request):
    project_id = os.getenv('GCP_PROJECT')
    # Create/update metric descriptor and exit if running in testing mode
    create_metric_descriptor(project_id)
    request_json = request.get_json(silent=True)
    if request_json and 'mode' in request_json:
        if request_json['mode'] == 'test':
            return "TESTED"
            sys.exit()

    repo = "TakeoffTech/daas-data-lake-sub-dataflow-bigquery"
    token = access_secret_version(project=project_id, secret_id="github-private-access-token")
    status = {
        "tables": {},
        "topics": {}
    }

    path = download_repo(token, repo)
    # Counting Pub/Sub topics found in Google Cloud
    topics_total = count_pubsub(project=project_id)

    for item in os.listdir(f"{path}/conf"):
        if os.path.isdir(f"{path}/conf/{item}"):
            client_config = f"{path}/conf/{item}/config.yml"
            with open(client_config, 'r') as file:
                yml = yaml.load(file, Loader=yaml.FullLoader)
            if client_enabled(yml):
                print(f"Validating {item}")
                # Counting Pub/Sub topics and BigQuery tables defined in source code
                topics_expected = get_topics(yml)
                tables_expected = get_tables(yml)
                # Counting BigQuery tables found in Google Cloud
                tables_found = count_bigquery(project_id, item.replace("-", "_"))
                for t in tables_expected:
                    if t in tables_found:
                        status['tables'][item] = "OK"
                    else:
                        status['tables'][item] = "ERROR"
                        break
                # Sorting topics by vendor
                topics_found = sort_pubsub_vendor(item, topics_total)
                for t in topics_expected:
                    if t in topics_found:
                        status['topics'][item] = "OK"
                    else:
                        status['topics'][item] = "ERROR"
                        break

    print(status)
    try:
        for resource in status.keys():
            for item in status[resource].keys():
                if status[resource][item] == "OK":
                    avail = 1
                else:
                    avail = 0
                    raise StopIteration
    except StopIteration:
        pass
    
    # Sending custom metric to Cloud Monitoring
    if check_workflow_run(token, repo):
        print("Deployment in progress found. Metric is not sent.")
    else:
        print("No deployment in progress found.")
        send_metric(project_id, avail)

    return "SUCCESS" if avail == 1 else "ERROR"
