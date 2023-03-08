terraform {
  backend "gcs" {
    bucket = "za-global-terraform-p-tf-state"
    prefix = "non-prod/databricks/its-managed-dbx-de-01-t/dbricks_workspaces/data_engineering/mktg/state"
  }
}