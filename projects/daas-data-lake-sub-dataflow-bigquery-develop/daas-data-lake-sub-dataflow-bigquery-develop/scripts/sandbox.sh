#!/usr/bin/env bash


PROJECT_ID="$1"


gcloud config set project $PROJECT_ID
gcloud services enable iam.googleapis.com \
    monitoring.googleapis.com \
    cloudbuild.googleapis.com \
    compute.googleapis.com \
    cloudresourcemanager.googleapis.com \
    bigquery.googleapis.com \
    dataflow.googleapis.com \
    artifactregistry.googleapis.com \
    run.googleapis.com
sleep 15
gcloud iam service-accounts create jumpbox-sa \
    --description="Jumpbox service account" \
    --display-name="Jumpbox SA"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:jumpbox-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/owner"
sleep 30
gsutil mb "gs://${PROJECT_ID}-service"
gsutil mb "gs://${PROJECT_ID}-state"
gsutil cp ./startup-jumpbox.sh "gs://${PROJECT_ID}-service/scripts/"
sleep 30

gcloud compute instances create tf-jumpbox \
    --zone="us-central1-a" \
    --machine-type="e2-standard-2" \
    --service-account="jumpbox-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
    --scopes="https://www.googleapis.com/auth/cloud-platform" \
    --metadata=startup-script-url="gs://${PROJECT_ID}-service/scripts/startup-jumpbox.sh"

if [ -f "${HOME}/.ssh/id_rsa.pub" ]; then
    echo "Add your SSH public key (default ~/.ssh/id_rsa.pub) to VM instance metadata"
else
    echo "SSH key pair not found. Create one and add your public key to VM instance metadata"
fi
