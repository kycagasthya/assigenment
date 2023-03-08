
/******************************************
  Service Account Outputs
*******************************************/
output "test_gcs_admin_sa_email" {
  description = "Service account email for gcs admin."
  value       = google_service_account.test_gcs_admin_sa.email
}

/******************************************
  Output of GCS Bucket
*******************************************/
output "user_work_area_bucket_name" {
  value       = module.user_work_area_bucket.name
  description = "Bucket name for User work area"
}

output "pipeline_bucket" {
  value       = module.pipeline_bucket.name
  description = "Bucket name for pipeline codes "
}

output "mktg_workarea_bucket" {
  value       = module.mktg_workarea_bucket.name
  description = "Bucket name for mktg_workarea_bucket "
}

output "glo_workarea_bucket" {
  value       = module.glo_workarea_bucket.name
  description = "Bucket name for glo_workarea_bucket "
}


output "goas_workarea_bucket" {
  value       = module.goas_workarea_bucket.name
  description = "Bucket name for glo_workarea_bucket "
}

output "goas_finance__bucket" {
  value       = module.goas_finance__bucket.name
  description = "Bucket name for goas_finance__bucket "
}
