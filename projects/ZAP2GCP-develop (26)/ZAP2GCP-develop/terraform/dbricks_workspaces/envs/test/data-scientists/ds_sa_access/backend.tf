terraform {
  backend "gcs" {
    bucket = "za-global-terraform-p-tf-state"
    prefix = "non-prod/databricks/its-managed-dbx-zap-d/dbricks_workspaces/data_scientists/TEST/temp_access/state"
  }
}