output "dataflow_bucket" {
  value = google_storage_bucket.df_bucket.name
}

output "backup_bucket" {
  value = google_storage_bucket.backup_bucket.name
}

output "artifacts_bucket" {
  value = google_storage_bucket.artifacts.name
}

output "dataflow_service_account" {
  value = module.dataflow_custom_iam.service_account_email
}

output "service_id" {
  value = google_monitoring_custom_service.datalake.service_id
}

output "opsgenie_channel" {
  value = google_monitoring_notification_channel.opsgenie.name
}
