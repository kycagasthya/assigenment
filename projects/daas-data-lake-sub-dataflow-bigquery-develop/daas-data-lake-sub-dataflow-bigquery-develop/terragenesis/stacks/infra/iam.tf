locals {
  dataflow_publisher_roles = [
    "roles/pubsub.publisher",
    "roles/bigquery.metadataViewer"
  ]
  pubsub_service_roles = [
    "roles/bigquery.dataEditor",
    "roles/bigquery.metadataViewer"
  ]
}

module "dataflow_custom_iam" {
  source                      = "../../modules/iam"
  project                     = var.project
  service_account_id          = "datalake-df-job"
  service_account_description = "Dataflow custom service account"
  iam_roles = [
    "roles/bigquery.dataEditor",
    "roles/dataflow.worker",
    "roles/dataflow.viewer",
    "roles/pubsub.subscriber",
    "roles/pubsub.viewer",
    "roles/storage.admin"
  ]
}

# # Smth to clarify
# resource "google_project_iam_member" "tkf_wings_pubsub_subscr" {
#   project = "takeoff-wings"
#   member  = "serviceAccount:${module.dataflow_custom_iam.service_account_email}"
#   role    = "roles/pubsub.subscriber"
# }

# External access from publisher project
resource "google_project_iam_member" "ext_publisher_iam_config" {
  for_each = toset(local.dataflow_publisher_roles)
  project  = var.project
  member   = "serviceAccount:datalake-df-job@${var.publisher_project_id}.iam.gserviceaccount.com"
  role     = each.value
}

module "functions_custom_iam" {
  source                      = "../../modules/iam"
  project                     = var.project
  service_account_id          = "datalake-availability"
  service_account_description = "Datalake availability function service account"
  iam_roles = [
    "roles/bigquery.metadataViewer",
    "roles/monitoring.metricWriter",
    "roles/pubsub.viewer",
    "roles/secretmanager.secretAccessor"
  ]
}
module "completeness_function_custom_iam" {
  source                      = "../../modules/iam"
  project                     = var.project
  service_account_id          = "datalake-completeness"
  service_account_description = "Datalake Completeness function service account"
  iam_roles = [
    "roles/bigquery.metadataViewer",
    "roles/bigquery.dataViewer",
    "roles/bigquery.jobUser",
    "roles/monitoring.metricWriter",
  ]
}

module "scheduler_custom_iam" {
  source                      = "../../modules/iam"
  project                     = var.project
  service_account_id          = "cloud-scheduler-sa"
  service_account_description = "Cloud Scheduler service account"
  iam_roles = [
    "roles/cloudfunctions.invoker",
    "roles/run.invoker"
  ]
}

resource "google_project_iam_member" "pubsub_svc_iam" {
  for_each = toset(local.pubsub_service_roles)
  project  = var.project
  member   = "serviceAccount:service-${data.google_project.project.number}@gcp-sa-pubsub.iam.gserviceaccount.com"
  role     = each.value
}
