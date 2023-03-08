terraform {
  backend "gcs" {
    bucket = "za-global-terraform-p-tf-state"
    prefix = "non-prod/databricks/its-managed-dbx-ds-01-t/dbricks_workspaces/dbx-ds/state"
  }
}