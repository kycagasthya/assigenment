data "google_storage_bucket" "databricks_2348922014507522" {
  name = "databricks-2348922014507522"
}

data "google_storage_bucket" "databricks_2348922014507522_system" {
  name = "databricks-2348922014507522-system"
}

data "google_storage_bucket" "glo_workarea" {
  name = "its-managed-dbx-ds-01-t-glo-workarea"
}

data "google_storage_bucket" "goas_finance" {
  name = "its-managed-dbx-ds-01-t-goas-finance"
}

data "google_storage_bucket" "goas_workarea" {
  name = "its-managed-dbx-ds-01-t-goas-workarea"
}

data "google_storage_bucket" "mktg_workarea" {
  name = "its-managed-dbx-ds-01-t-mktg-workarea"
}

data "google_storage_bucket" "pipeline_code" {
  name = "its-managed-dbx-ds-01-t-pipeline-code"
}

data "google_storage_bucket" "user_work_area" {
  name = "its-managed-dbx-ds-01-t-user-work-area"
}
