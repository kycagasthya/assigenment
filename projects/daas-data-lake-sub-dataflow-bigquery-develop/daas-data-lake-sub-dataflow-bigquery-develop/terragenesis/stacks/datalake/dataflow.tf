resource "google_dataflow_flex_template_job" "df_job" {
  provider                = google-beta
  name                    = "${var.client_id}-dl-ingest"
  project                 = var.project
  container_spec_gcs_path = var.template_path
  on_delete               = var.env == "production" ? "drain" : "cancel"
  parameters = {
    clients_config                = file("./client_config.json")
    subscriptions                 = join(",", values(module.google_pubsub)[*].ps_subscr_name)
    backup_location               = "gs://${data.terraform_remote_state.infrastructure.outputs.backup_bucket}/${var.client_id}"
    service_account_email         = data.terraform_remote_state.infrastructure.outputs.dataflow_service_account
    temp_location                 = "gs://${data.terraform_remote_state.infrastructure.outputs.dataflow_bucket}/${var.client_id}/temp"
    staging_location              = "gs://${data.terraform_remote_state.infrastructure.outputs.dataflow_bucket}/${var.client_id}/staging"
    max_num_workers               = 10
    machine_type                  = var.env == "production" ? "e2-standard-4" : "e2-standard-2"
    default_sdk_harness_log_level = var.env == "production" ? "WARNING" : "INFO"
  }
  depends_on = [
    module.google_pubsub,
    module.google_bigquery
  ]
}
