PROJECT_ID="$1"
SF_ACCOUNT="$2"
SF_WAREHOUSE="$3"

gcloud config set project $PROJECT_ID

SF_USER_PATH=$(gcloud secrets describe SF_USER --format="value(name)")
SF_PASSWORD_PATH=$(gcloud secrets describe SF_PASSWORD --format="value(name)")
gcloud functions deploy bq-sf-count-comparison \
    --source=src/ \
    --entry-point main \
    --runtime=python38 \
    --memory 256MB \
    --trigger-http \
    --timeout 540s\
    --set-env-vars BQ_PROJECT_ID=$PROJECT_ID,SF_ACCOUNT=$SF_ACCOUNT,SF_WAREHOUSE=$SF_WAREHOUSE \
    --set-secrets SF_USER=$SF_USER_PATH:latest,SF_PASSWORD=$SF_PASSWORD_PATH:latest