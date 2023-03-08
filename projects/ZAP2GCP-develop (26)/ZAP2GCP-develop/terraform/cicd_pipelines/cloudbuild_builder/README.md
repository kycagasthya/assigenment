To run the cloudbuild image build cd to cloudbuild_builder and run below commands:

"cd cicd_pipelines/cicd_ops/cloudbuild_builder/"

"gcloud builds submit --project its-registry-it-kcl-p --impersonate-service-account=quantiphi-terraform-dev@za-global-service-accounts-p.iam.gserviceaccount.com --config cloudbuild.yaml ."
