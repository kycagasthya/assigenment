locals {
  labels = {
    client_name = var.client_id
  }
  sandbox_label = var.env == "sandbox" ? { jira = var.tag } : {}
}

resource "google_bigquery_dataset" "bq_dataset" {
  dataset_id    = var.dataset_id
  friendly_name = var.dataset_id
  location      = "US"
  project       = var.project
  labels = (merge(
    local.labels,
    local.sandbox_label
  ))
}

module "google_bigquery" {
  source       = "../../modules/bigquery"
  for_each     = var.tables
  project      = var.project
  dataset_id   = google_bigquery_dataset.bq_dataset.dataset_id
  table_id     = each.value.table_id
  description  = each.value.description
  table_schema = var.env == "sandbox" ? file("../../../.sandbox/conf/${var.client_id}/tables/${each.value.table_id}/${each.value.table_schema_file}") : file("../../../conf/${var.client_id}/tables/${each.value.table_id}/${each.value.table_schema_file}")
  protected    = var.env == "production" ? true : false
  labels = (merge(
    local.labels,
    local.sandbox_label,
    var.labels,
    each.value.client_labels
  ))
}

resource "google_bigquery_dataset" "bq_dataset_raw" {
  dataset_id    = "${var.raw_prefix}_${var.dataset_id}"
  friendly_name = "${var.raw_prefix}_${var.dataset_id}"
  location      = "US"
  project       = var.project
  labels = (merge(
    local.labels,
    local.sandbox_label
  ))
}


module "google_bigquery_raw" {
  source       = "../../modules/bigquery"
  for_each     = var.tables
  project      = var.project
  dataset_id   = google_bigquery_dataset.bq_dataset_raw.dataset_id
  table_id     = "${var.raw_prefix}_${each.value.table_id}"
  description  = "PubSub RAW data from ${var.client_id}'s ${each.value.table_id} source"
  table_schema = file("../../src/schemas/raw_export_bq_schema.json")
  protected    = var.env == "production" ? true : false
  labels = (merge(
    local.labels,
    local.sandbox_label
  ))
}
