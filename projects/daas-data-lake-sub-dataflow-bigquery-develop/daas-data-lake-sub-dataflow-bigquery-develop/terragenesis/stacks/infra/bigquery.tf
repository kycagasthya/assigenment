resource "google_bigquery_dataset" "bq_dataset" {
  dataset_id    = var.dataset_id
  friendly_name = var.dataset_id
  location      = "US"
  project       = var.project
  labels        = var.labels
}

resource "google_bigquery_dataset" "bq_billing" {
  dataset_id    = "datalake_gcp_billing"
  friendly_name = "Datalake GCP billing"
  location      = "US"
  project       = var.project
  labels        = var.labels
}

module "google_bigquery" {
  source       = "../../modules/bigquery"
  for_each     = var.tables
  project      = var.project
  dataset_id   = google_bigquery_dataset.bq_dataset.dataset_id
  table_id     = each.value.table_id
  description  = each.value.description
  table_schema = file("../../src/schemas/${each.value.table_schema_file}")
  protected    = var.env == "production" ? true : false
  labels       = var.labels
}
