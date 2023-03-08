output "bq_table_id" {
  value = "${google_bigquery_table.bq_table.project}:${google_bigquery_table.bq_table.dataset_id}.${google_bigquery_table.bq_table.table_id}"
}
