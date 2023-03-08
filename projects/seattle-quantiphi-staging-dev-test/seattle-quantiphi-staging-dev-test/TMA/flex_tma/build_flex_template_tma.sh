#!/bin/bash

# choose directory cicd/
cd cicd

# Export Template Image path
export TEMPLATE_IMAGE="gcr.io/ihc-qc-sandbox/dataflow/dev-tma-flex-img4-base-image-df"

#Enable Kaniko cache use by default
gcloud config set builds/use_kaniko True

#Create image and push to gcr
gcloud builds submit --timeout 1800 --tag $TEMPLATE_IMAGE .

#Export Template GCS part
export TEMPLATE_PATH="gs://seagen_dataflow/templates/dev_tma/v4.json"

#Copy config file to GCS
gsutil cp ../config.json gs://seagen_dataflow/dev_config_tma4/config.json

#Build Flex template and store in TEMPLATE_PATH(GCS)
gcloud dataflow flex-template build $TEMPLATE_PATH \
    --image "$TEMPLATE_IMAGE" \
    --sdk-language "PYTHON" \
    --metadata-file "metadata.json"
