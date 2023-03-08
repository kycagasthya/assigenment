/******************************************************
  Composer Environment creation
******************************************************/
module "composer_environment" {
  source                           = "github.com/terraform-google-modules/terraform-google-composer//modules/create_environment?ref=v2.0.0"
  project_id                       = var.project_id
  composer_env_name                = var.composer_env_name
  region                           = var.region
  labels                           = var.composer_labels
  node_count                       = var.node_count
  machine_type                     = var.composer_machine_type
  network                          = var.orchestrator_network_name
  subnetwork                       = var.orchestrator_subnetwork_name
  composer_service_account         = google_service_account.composer.email
  disk_size                        = var.composer_disk_size
  tags                             = var.composer_tags
  use_ip_aliases                   = true
  pod_ip_allocation_range_name     = var.orchestrator_pod_range_name
  service_ip_allocation_range_name = var.orchestrator_svc_range_name
  enable_private_endpoint          = true
  master_ipv4_cidr                 = var.orchestrator_gke_master_ip_range
  web_server_ipv4_cidr             = var.web_server_ipv4_cidr
  cloud_sql_ipv4_cidr              = var.cloud_sql_ipv4_cidr
  python_version                   = var.python_version
  image_version                    = var.image_version
  airflow_config_overrides         = var.airflow_config_overrides
  pypi_packages                    = var.pypi_packages
  env_variables                    = var.env_variables

  depends_on = [
    google_service_account_iam_member.tf_sa_access,
  ]
}

/******************************************************
  Composer Cluster Service Account
******************************************************/
resource "google_service_account" "composer" {
  project      = var.project_id
  account_id   = "sa-composer"
  display_name = "Composer service account"
}

resource "google_project_iam_member" "cluster_sa_log_writer" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.composer.email}"
}

resource "google_project_iam_member" "cluster_sa_metric_writer" {
  project = var.project_id
  role    = "roles/monitoring.metricWriter"
  member  = "serviceAccount:${google_service_account.composer.email}"
}

resource "google_project_iam_member" "cluster_sa_metadata_writer" {
  project = var.project_id
  role    = "roles/stackdriver.resourceMetadata.writer"
  member  = "serviceAccount:${google_service_account.composer.email}"
}

resource "google_project_iam_member" "composer_worker" {
  project = var.project_id
  role    = "roles/composer.worker"
  member  = "serviceAccount:${google_service_account.composer.email}"
}

resource "google_service_account_iam_member" "sa_user" {
  service_account_id = google_service_account.composer.name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${google_service_account.composer.email}"
}

resource "google_service_account_iam_member" "tf_composer_sa_access" {
  service_account_id = google_service_account.composer.name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${var.terraform_sa_email}"
}

#resource "google_service_account_iam_member" "tf_composer_secret_access" {
#  service_account_id = google_service_account.composer.name
#  role               = "roles/secretmanager.secretAccessor"
#  member             = "serviceAccount:${var.terraform_sa_email}"
#}
