
/******************************************
  Service Account Outputs
*******************************************/
output "dev_gcs_admin_sa_email" {
  description = "Service account email for gcs admin."
  value       = google_service_account.dev_gcs_admin_sa.email
}

output "dev_gcs_reader_sa_email" {
  description = "Service account email for gcs reader."
  value       = google_service_account.dev_gcs_reader_sa.email
}

/******************************************
  Output of GCS Bucket
*******************************************/
output "dev_landing_bucket_name" {
  value       = module.nc_dev_delta_sfdc_bucket.name
  description = "Bucket name for dev landing zone"
}

output "dev_delta_sfdc_bucket_name" {
  value       = module.nc_dev_landing_eol_bucket.name
  description = "Bucket name for delta table sfdc"
}

output "dev_landing_eol_bucket" {
  value       = module.nc_dev_delta_eol_bucket.name
  description = "Bucket name for landing zone for EOL"
}

output "dev_landing_planib_bucket" {
  value       = module.nc_dev_landing_planib_bucket.name
  description = "Bucket name for landing zone for Plan IB"
}

output "dev_delta_bs_planib_bucket" {
  value       = module.nc_dev_delta_bs_planib_bucket.name
  description = "Bucket name for delta table Plan IB"
}

output "dev_pipeline_bucket" {
  value       = module.dev_pipeline_bucket.name
  description = "Bucket name for pipeline codes in dev env"
}


#Added for Marketing team

output "delta_bs_gst_bucket" {
  value       = module.delta_bs_gst_bucket.name
  description = "Bucket name for delta_bs_gst_bucket in dev env"
}

output "landing_vistex_bucket" {
  value       = module.landing_vistex_bucket.name
  description = "Bucket name for landing_vistex_bucket in dev env"
}

output "delta_bs_vistex_bucket" {
  value       = module.delta_bs_vistex_bucket.name
  description = "Bucket name for delta_bs_vistex_bucket in dev env"
}


output "landing_turtl_bucket" {
  value       = module.landing_turtl_bucket.name
  description = "Bucket name for landing_turtl_bucket in dev env"
}

output "delta_bs_turtl_bucket" {
  value       = module.delta_bs_turtl_bucket.name
  description = "Bucket name for delta_bs_turtl_bucket in dev env"
}

output "landing_dwa_bucket" {
  value       = module.landing_dwa_bucket.name
  description = "Bucket name for landing_dwa_bucket in dev env"
}

output "delta_bs_dwa_bucket" {
  value       = module.delta_bs_dwa_bucket.name
  description = "Bucket name for delta_bs_dwa_bucket in dev env"
}


output "landing_eloqua_bucket" {
  value       = module.landing_eloqua_bucket.name
  description = "Bucket name for landing_eloqua_bucket in dev env"
}


output "delta_bs_eloqua_bucket" {
  value       = module.delta_bs_eloqua_bucket.name
  description = "Bucket name for delta_bs_eloqua_bucket in dev env"
}

output "landing_qualtrics_bucket" {
  value       = module.landing_qualtrics_bucket.name
  description = "Bucket name for landing_qualtrics_bucket in dev env"
}

output "delta_bs_qualtrics_bucket" {
  value       = module.delta_bs_qualtrics_bucket.name
  description = "Bucket name for delta_bs_qualtrics_bucket in dev env"
}

output "landing_demandbase_bucket" {
  value       = module.landing_demandbase_bucket.name
  description = "Bucket name for landing_demandbase_bucket in dev env"
}

output "delta_bs_demandbase_bucket" {
  value       = module.delta_bs_demandbase_bucket.name
  description = "Bucket name for delta_bs_demandbase_bucket in dev env"
}

output "landing_evergage_bucket" {
  value       = module.landing_evergage_bucket.name
  description = "Bucket name for landing_evergage_bucket in dev env"
}

output "delta_bs_evergage_bucket" {
  value       = module.delta_bs_evergage_bucket.name
  description = "Bucket name for delta_bs_evergage_bucket in dev env"
}

output "landing_m360_bucket" {
  value       = module.landing_m360_bucket.name
  description = "Bucket name for landing_m360_bucket in dev env"
}

output "delta_bs_m360_bucket" {
  value       = module.delta_bs_m360_bucket.name
  description = "Bucket name for delta_bs_m360_bucket in dev env"
}
