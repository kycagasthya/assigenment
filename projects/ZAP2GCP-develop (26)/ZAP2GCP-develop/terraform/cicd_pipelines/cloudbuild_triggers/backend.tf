
terraform {
  backend "gcs" {
    bucket = "za-global-terraform-p-tf-state"
    prefix = "cicd_pipelines/cloudbuild_triggers/its-registry-it-kcl-p/state"
  }
}








