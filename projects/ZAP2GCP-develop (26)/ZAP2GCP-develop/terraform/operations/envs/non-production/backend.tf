terraform {
  backend "gcs" {
    bucket = "za-global-terraform-p-tf-state"
    prefix = "non-prod/databricks/its-managed-dbx-edlops-t/operations/state"
  }
}