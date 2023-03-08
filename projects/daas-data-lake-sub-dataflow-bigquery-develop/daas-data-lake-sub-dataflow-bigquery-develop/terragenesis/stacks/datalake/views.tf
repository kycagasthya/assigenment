resource "google_bigquery_table" "bq_view_table" {
  for_each            = var.views
  dataset_id          = google_bigquery_dataset.bq_dataset.dataset_id
  table_id            = each.value.view_id
  project             = var.project
  deletion_protection = false

  view {
    query          = file("../../../conf/${var.client_id}/views/${each.value.view_query_file}")
    use_legacy_sql = false
  }

  labels = (merge(
    local.labels,
    local.sandbox_label
  ))

  depends_on = [
    module.google_bigquery
  ]
}