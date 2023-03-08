
/******************************************************
  Project IAM Bindings
*******************************************************/
resource "google_project_iam_member" "cluster_sa_log_writer" {
  count   = length(local.service_account_email)
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.test_gcs_admin_sa.email}"
}

resource "google_project_iam_member" "cluster_sa_metric_writer" {
  count   = length(local.service_account_email)
  project = var.project_id
  role    = "roles/monitoring.metricWriter"
  member  = "serviceAccount:${google_service_account.test_gcs_admin_sa.email}"
}

resource "google_project_iam_member" "cluster_sa_metric_viewer" {
  count   = length(local.service_account_email)
  project = var.project_id
  role    = "roles/monitoring.viewer"
  member  = "serviceAccount:${google_service_account.test_gcs_admin_sa.email}"
}

resource "google_project_iam_member" "cluster_sa_metadata_writer" {
  count   = length(local.service_account_email)
  project = var.project_id
  role    = "roles/stackdriver.resourceMetadata.writer"
  member  = "serviceAccount:${google_service_account.test_gcs_admin_sa.email}"
}

resource "google_project_iam_member" "cluster_sa_storage_admin" {
  project = var.project_id
  role    = "roles/storage.objectAdmin"
  member  = "serviceAccount:${google_service_account.test_gcs_admin_sa.email}"
}

resource "google_project_iam_member" "cluster_sa_storage_viewer" {
  project = var.test_project_id
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${google_service_account.test_gcs_admin_sa.email}"
}

/******************************************************
  Databricks Cluster Service Account
******************************************************/
resource "google_service_account" "test_gcs_admin_sa" {
  project      = var.project_id
  account_id   = "sa-gke-gcs-ds-object-admin"
  display_name = "Dev Databricks DS Cluster service account for object admins"
}

/******************************************************
  FInance bucket service Account
******************************************************/
resource "google_service_account" "fin-gke-dbx-sa" {
  project      = var.project_id
  account_id   = "sa-fin-gke-dbx"
  display_name = "Finance bucket service account"
}



#logs writer
resource "google_project_iam_member" "cluster_sa_log_writer_dbx_p" {
  count   = length(local.sa_email_access)
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = local.sa_email_access[count.index]
}

#logs Viewer
resource "google_project_iam_member" "cluster_sa_log_viewer_dbx_p" {
  count   = length(local.group_access)
  project = var.project_id
  role    = "roles/logging.viewer"
  member  = local.group_access[count.index]
}

#monitoring metric writer
resource "google_project_iam_member" "cluster_sa_metric_writer_dbx_p" {
  count   = length(local.sa_email_access)
  project = var.project_id
  role    = "roles/monitoring.metricWriter"
  member  = local.sa_email_access[count.index]
}

# monitoring viewer
resource "google_project_iam_member" "cluster_sa_metric_viewer_dbx_p" {
  count   = length(local.group_and_sa_email_access)
  project = var.project_id
  role    = "roles/monitoring.viewer"
  member  = local.group_and_sa_email_access[count.index]
}

#stackdriver resource metdata writer
resource "google_project_iam_member" "cluster_sa_metadata_writer_dbx_p" {
  count   = length(local.sa_email_access)
  project = var.project_id
  role    = "roles/stackdriver.resourceMetadata.writer"
  member  = local.sa_email_access[count.index]
}

#Security reviewer
resource "google_project_iam_member" "sa_security_reviewer_P" {
  count   = length(local.group_access)
  project = var.project_id
  role    = "roles/iam.securityReviewer"
  member  = local.group_access[count.index]
}

#Compute Viewer
resource "google_project_iam_member" "compute_viewer_p" {
  count   = length(local.group_access)
  project = var.project_id
  role    = "roles/compute.viewer"
  member  = local.group_access[count.index]
}

#Compute Network Viewer
resource "google_project_iam_member" "compute_network_viewer_p" {
  count   = length(local.group_access)
  project = var.project_id
  role    = "roles/compute.networkViewer"
  member  = local.group_access[count.index]
}

#Kubernetes Engine Cluster Viewer
resource "google_project_iam_member" "gke_engine_cluster_viewer_p" {
  count   = length(local.group_access)
  project = var.project_id
  role    = "roles/container.clusterViewer"
  member  = local.group_access[count.index]
}