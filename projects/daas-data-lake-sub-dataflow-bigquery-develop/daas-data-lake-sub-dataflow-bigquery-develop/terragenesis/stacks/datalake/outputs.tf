output "subscr_list" {
  value = join(",", values(module.google_pubsub)[*].ps_subscr_name)
}

output "table_list" {
  value = join(",", values(module.google_bigquery)[*].bq_table_id)
}
