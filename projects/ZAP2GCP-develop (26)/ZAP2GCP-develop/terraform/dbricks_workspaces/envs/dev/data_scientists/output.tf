
/******************************************
  Service Account Outputs
*******************************************/
output "dev_gcs_admin_sa_email" {
  description = "Service account email for gcs admin."
  value       = google_service_account.dev_gcs_admin_sa.email
}

/******************************************
  Output of GCS Bucket
*******************************************/
output "user_work_area_bucket_name" {
  value       = module.user_work_area_bucket.name
  description = "Bucket name for User work area"
}

output "dev_pipeline_bucket" {
  value       = module.dev_pipeline_bucket.name
  description = "Bucket name for pipeline codes in dev env"
}
