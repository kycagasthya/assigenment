data "google_storage_bucket" "databricks_2945417879364985" {
  name = "databricks-2945417879364985"
}

data "google_storage_bucket" "databricks_2945417879364985_system" {
  name = "databricks-2945417879364985-system"
}

data "google_storage_bucket" "fin_workarea" {
  name = "its-managed-dbx-ds-01-d-fin-workarea"
}

data "google_storage_bucket" "glo_workarea" {
  name = "its-managed-dbx-ds-01-d-glo-workarea"
}

data "google_storage_bucket" "goas_finance" {
  name = "its-managed-dbx-ds-01-d-goas-finance"
}

data "google_storage_bucket" "goas_workarea" {
  name = "its-managed-dbx-ds-01-d-goas-workarea"
}

data "google_storage_bucket" "mktg_workarea" {
  name = "its-managed-dbx-ds-01-d-mktg-workarea"
}

data "google_storage_bucket" "pipeline_code" {
  name = "its-managed-dbx-ds-01-d-pipeline-code"
}

data "google_storage_bucket" "user_work_area" {
  name = "its-managed-dbx-ds-01-d-user-work-area"
}
