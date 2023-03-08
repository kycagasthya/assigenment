#!/bin/sh
# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

# This is the bash script to trigger the Composer DAG

if [ "$#" -ne 4 ]; then
  echo "Usage: sh $0 COMPOSER_ENV LOCATION DAG_ID JSON_FILE" >&2
  echo "Example: sh $0 docai-mlops-composer-env-01 asia-south1 cdc_pipeline config_samples/cdc.json" >&2
  exit 1
fi
if ! [ -e "$4" ]; then
  echo "$4 is not found" >&2
  exit 1
fi
if ! [ -f "$4" ]; then
  echo "$4 is not a file" >&2
  exit 1
fi

COMPOSER_ENV=$1
LOCATION=$2
DAG_ID=$3
JSON_DATA=`cat $4`
TOKEN=$(gcloud auth print-access-token)
WEB_SERVER_URL=$(gcloud composer environments describe ${COMPOSER_ENV} --location=${LOCATION} --format="value(config.airflowUri)")

curl -X POST "${WEB_SERVER_URL}/api/v1/dags/${DAG_ID}/dagRuns" \
-d '{"conf": '"$JSON_DATA"' }' \
-H "Authorization: Bearer ${TOKEN}" \
-H 'Content-Type: application/json' 
