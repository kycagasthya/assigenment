/******************************************************
  Airflow Maitenance GCE Service Account
******************************************************/
resource "google_service_account" "airflow_maintenance" {
  project      = var.project_id
  account_id   = "sa-airflow-maint"
  display_name = "Airflow cluster maintenance Compute Engine Service Account"
}

resource "google_project_iam_member" "maint_composer_admin" {
  count = var.deploy_maint_gce ? 1 : 0

  project = var.project_id
  role    = "roles/composer.admin"
  member  = "serviceAccount:${google_service_account.airflow_maintenance.email}"
}

resource "google_project_iam_member" "maint_log_writer" {
  count = var.deploy_maint_gce ? 1 : 0

  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.airflow_maintenance.email}"
}

resource "google_project_iam_member" "maint_metric_writer" {
  count = var.deploy_maint_gce ? 1 : 0

  project = var.project_id
  role    = "roles/monitoring.metricWriter"
  member  = "serviceAccount:${google_service_account.airflow_maintenance.email}"
}

resource "google_project_iam_member" "maint_composer_worker" {
  count = var.deploy_maint_gce ? 1 : 0

  project = var.project_id
  role    = "roles/composer.worker"
  member  = "serviceAccount:${google_service_account.airflow_maintenance.email}"
}

resource "google_service_account_iam_member" "tf_airflow_sa_access" {
  service_account_id = google_service_account.airflow_maintenance.name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${var.terraform_sa_email}"
}


/******************************************************
 Compute Engine to maintain Airflow RBAC
******************************************************/

resource "google_compute_instance" "airflow_maintenance" {
  count = var.deploy_maint_gce ? 1 : 0

  project             = var.project_id
  name                = var.airflow_maint_instance_name
  machine_type        = "e2-micro"
  zone                = "${var.region}-a"
  labels              = var.airflow_maint_labels
  description         = "Airflow cluster maintenance compute instance for RBAC"
  deletion_protection = false

  boot_disk {
    initialize_params {
      image = "rhel-cloud/rhel-8-v20210916"
      size = 20
      type = "pd-standard"
    }
  }

  network_interface {
    subnetwork = var.orchestrator_subnetwork_name
  }
  metadata_startup_script = "sudo yum install kubectl -y"

  tags = ["non-prod", "allow-iap-ssh"]

  service_account {
    email  = google_service_account.airflow_maintenance.email
    scopes = ["cloud-platform"]
  }
}