module "datalake_availability" {
  source                = "../../modules/functions"
  project               = var.project
  region                = "us-east1"
  service_account_email = module.functions_custom_iam.service_account_email
  artifacts_bucket      = google_storage_bucket.artifacts.name
  app_name              = "datalake-availability"
  description           = "Datalake availability check"
  source_dir            = "../../src/functions/datalake-availability"
  runtime               = "python310"
  entrypoint            = "run"
  env_vars = {
    "GCP_PROJECT" = var.project
  }
}

resource "google_cloud_scheduler_job" "datalake_availability_check" {
  region           = "us-east1"
  name             = "datalake-availability"
  description      = "Datalake availability check"
  schedule         = "*/5 * * * *"
  time_zone        = "Europe/Kiev"
  attempt_deadline = "180s"

  retry_config {
    retry_count = 1
  }

  http_target {
    http_method = "POST"
    uri         = module.datalake_availability.function2_url
    body        = base64encode("{}")

    oidc_token {
      service_account_email = module.scheduler_custom_iam.service_account_email
    }
  }
}

module "datalake_data_completeness_check" {
  source                = "../../modules/functions"
  project               = var.project
  region                = "us-east1"
  service_account_email = module.completeness_function_custom_iam.service_account_email
  artifacts_bucket      = google_storage_bucket.artifacts.name
  app_name              = "data-completeness-check"
  description           = "Datalake Data Completeness Check"
  source_dir            = "../../../monitoring/data_completeness_check/src"
  runtime               = "python310"
  entrypoint            = "main"
  timeout_seconds       = 1800
  env_vars = {
    "GCP_PROJECT"                  = var.project
    "MISSED_RECORDS_BQ_DATASET"    = var.dataset_id
    "MISSED_RECORDS_BQ_TABLE_NAME" = var.missed_records_table_name
  }
}

resource "google_cloud_scheduler_job" "datalake_data_completeness_check_cron" {
  region           = "us-east1"
  name             = "data-completeness-check-cron"
  description      = "Datalake Data Completeness Check cron (scheduler)"
  schedule         = "0 */8 * * *"
  time_zone        = "Europe/Kiev"
  attempt_deadline = "1800s"

  retry_config {
    retry_count = 1
  }

  http_target {
    http_method = "POST"
    uri         = module.datalake_data_completeness_check.function2_url
    body        = base64encode("{}")

    oidc_token {
      service_account_email = module.scheduler_custom_iam.service_account_email
    }
  }
}