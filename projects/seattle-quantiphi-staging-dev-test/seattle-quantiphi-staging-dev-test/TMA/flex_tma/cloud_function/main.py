from googleapiclient.discovery import build
import google.auth
import time
import os
import json
from google.cloud import storage

def download_config(bucket_name, source_blob_name):
    """Downloads a blob from the bucket."""

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    json_data_string = blob.download_as_string()

    print("Blob {} downloaded as string".format(source_blob_name))
    return json_data_string

def hello_gcs(event, context):   
    credentials, _ = google.auth.default()
    service = build('dataflow', 'v1b3', credentials=credentials, cache_discovery=False)
    gcp_project = os.environ['GCP_PROJECT']

    template_path = 'gs://seagen_dataflow/templates/dev_tma/v4.json'
    job_name_prefix = "dev-flex-tma-v4"
    now = time.strftime("%Y%m%d-%H%M%S")
    jobName = f"{job_name_prefix}-{now}"
    input_path = f"gs://{event['bucket']}/{event['name']}"
    output_path = f"gs://seagen_dataflow/results_runner/output-dev-tma-flex4/{jobName}"
    config_file = 'gs://seagen_dataflow/dev_config_tma4/config.json'
    
    config_bucket = 'seagen_dataflow'
    config_blob_name = 'dev_config_tma4/config.json'
    config_string = download_config(config_bucket, config_blob_name)
    try:
        config_json = json.loads(config_string)
    except:
        print('Config is invalid JSON format')
        raise

    template_body = {
        "launchParameter": {
            "jobName": jobName,
            "parameters": {
                "config_file": config_file,
                "input_path": input_path,
                "output_path": output_path
            },
            "environment": config_json['environment'],
            "containerSpecGcsPath": template_path
        }
    }
    
    print(f"Launching job with template_path {template_path} and template_body {template_body}")

    request = service.projects().locations().flexTemplates().launch(
        projectId=gcp_project,
        location=config_json['pipeline_config']['region'],
        body=template_body
    )

    response = request.execute()

    print(response)
