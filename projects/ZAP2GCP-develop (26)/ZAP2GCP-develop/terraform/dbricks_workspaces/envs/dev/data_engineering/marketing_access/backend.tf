terraform {
  backend "gcs" {
    bucket = "za-global-terraform-p-tf-state"
    prefix = "non-prod/databricks/its-managed-dbx-zap-d/dbricks_workspaces/data_engineering/mktg/state"
  }
}