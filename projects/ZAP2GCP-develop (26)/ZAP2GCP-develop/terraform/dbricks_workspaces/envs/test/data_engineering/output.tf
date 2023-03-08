
/******************************************
  Service Account Outputs
*******************************************/
output "test_gcs_admin_sa_email" {
  description = "Service account email for gcs admin for test environment."
  value       = google_service_account.test_gcs_admin_sa.email
}

output "test_gcs_reader_sa_email" {
  description = "Service account email for gcs reader for test environment."
  value       = google_service_account.test_gcs_reader_sa.email
}

/******************************************
  Output of GCS Bucket
*******************************************/
output "test_landing_bucket_name" {
  value       = module.test_landing_bucket.name
  description = "Bucket name for dev landing zone"
}

output "test_delta_sfdc_bucket_name" {
  value       = module.test_delta_sfdc_bucket.name
  description = "Bucket name for delta table sfdc"
}

output "test_landing_eol_bucket" {
  value       = module.test_landing_eol_bucket.name
  description = "Bucket name for landing zone for EOL"
}

output "test_delta_eol_bucket" {
  value       = module.test_delta_eol_bucket.name
  description = "Bucket name for delta table EOL"
}


output "test_landing_planib_bucket" {
  value       = module.test_landing_planib_bucket.name
  description = "Bucket name for landing zone for Plan IB"
}

output "test_delta_bs_planib_bucket" {
  value       = module.test_delta_bs_planib_bucket.name
  description = "Bucket name for delta table Plan IB"
}

output "test_pipeline_bucket" {
  value       = module.test_pipeline_bucket.name
  description = "Bucket name for pipeline codes in test env"
}

output "test_landing_evergage_bucket" {
  value       = module.test_landing_evergage_bucket.name
  description = "Bucket name for test_landing_evergage_bucket in test env"
}

output "test_delta_bs_evergage_bucket" {
  value       = module.test_delta_bs_evergage_bucket.name
  description = "Bucket name for test_delta_bs_evergage_bucket test env"
}

