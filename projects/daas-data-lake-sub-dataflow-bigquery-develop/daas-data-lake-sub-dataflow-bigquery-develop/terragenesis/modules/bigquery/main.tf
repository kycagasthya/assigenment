resource "google_bigquery_table" "bq_table" {
  dataset_id  = var.dataset_id
  table_id    = var.table_id
  project     = var.project
  description = var.description

  schema              = var.table_schema
  deletion_protection = var.protected

  time_partitioning {
    type = "DAY"
  }

  labels = var.labels
}