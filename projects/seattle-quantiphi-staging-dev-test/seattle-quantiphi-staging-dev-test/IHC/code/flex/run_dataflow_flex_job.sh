#!/bin/bash

#Export Template GCS path
export TEMPLATE_PATH="gs://seagen_dataflow/templates/dev_ihc/v2.json"

#Export Region to run the Dataflow Job in
export REGION="us-west1"

#Export JOB_NAME
now=$(date +"%Y%m%d-%H%M%S")
JOB_NAME="dev-flex-test-v2-$now"
export JOB_NAME=$JOB_NAME

#Export SUBNETWORK
export SUBNETWORK="regions/us-west1/subnetworks/oregon-subnet"

#Run Dataflow flex Job
gcloud dataflow flex-template run "$JOB_NAME" \
--template-file-gcs-location "$TEMPLATE_PATH" \
--parameters config_file="seagen_dataflow/ihc_config/config.json" \
--parameters input_path="gs://seagen_dataflow/input_csvs/input_paths_1.csv" \
--parameters output_path="gs://seagen_dataflow/results_runner/dev-ihc-flex-output" \
--region "$REGION" \
--subnetwork "$SUBNETWORK"
