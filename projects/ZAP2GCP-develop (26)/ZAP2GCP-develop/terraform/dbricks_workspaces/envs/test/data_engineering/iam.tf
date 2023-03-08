
/******************************************************
  Project IAM Bindings
*******************************************************/
resource "google_project_iam_member" "cluster_sa_log_writer" {
  count   = length(local.service_account_email)
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = local.service_account_email[count.index]
}

resource "google_project_iam_member" "cluster_sa_metric_writer" {
  count   = length(local.service_account_email)
  project = var.project_id
  role    = "roles/monitoring.metricWriter"
  member  = local.service_account_email[count.index]
}

resource "google_project_iam_member" "cluster_sa_metric_viewer" {
  count   = length(local.service_account_email)
  project = var.project_id
  role    = "roles/monitoring.viewer"
  member  = local.service_account_email[count.index]
}

resource "google_project_iam_member" "cluster_sa_metadata_writer" {
  count   = length(local.service_account_email)
  project = var.project_id
  role    = "roles/stackdriver.resourceMetadata.writer"
  member  = local.service_account_email[count.index]
}

resource "google_project_iam_member" "cluster_sa_storage_admin" {
  project = var.project_id
  role    = "roles/storage.objectAdmin"
  member  = "serviceAccount:${google_service_account.test_gcs_admin_sa.email}"
}

resource "google_project_iam_member" "cluster_sa_storage_viewer" {
  project = var.project_id
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${google_service_account.test_gcs_reader_sa.email}"
}

resource "google_storage_bucket_iam_member" "binding_bucket_landing_grdf_bucket" {
  bucket = module.landing_grdf_bucket.name
  role = "roles/storage.objectCreator"
  for_each = toset([
    "serviceAccount:sa-edi-data-upload-t@za-global-service-accounts-p.iam.gserviceaccount.com",
    "serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
  ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "binding_bucket_delta_bs_glo_bucket" {
  bucket = module.delta_bs_glo_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"
  ])
  member = each.value
}


resource "google_storage_bucket_iam_member" "binding_bucket_landing_goas_user_data_bucket" {
  bucket = module.landing_goas_user_data_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
    "group:gcds-its-zap-de-developers@zebra.com"
  ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "binding_bucket_delta_bs_goas_bucket" {
  bucket = module.delta_bs_goas_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
    "group:gcds-its-zap-de-developers@zebra.com"
  ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "binding_admin_landing_finance_bucket" {
  bucket = module.landing_finance_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
    "group:gcds-its-zap-de-fin-developers@zebra.com"
  ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "binding_viewer_landing_finance_bucket" {
  bucket = module.landing_finance_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "serviceAccount:sa-fin-gke-dbx@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
  ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "binding_admin_delta_bs_finance_bucket" {
  bucket = module.delta_bs_finance_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
    "group:gcds-its-zap-de-fin-developers@zebra.com"
  ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "binding_viewer_delta_bs_finance_bucket" {
  bucket = module.delta_bs_finance_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "serviceAccount:sa-fin-gke-dbx@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
  ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "binding_admin_delta_gold_finance_bucket" {
  bucket = module.delta_gold_finance_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
    "group:gcds-its-zap-de-fin-developers@zebra.com"
  ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "binding_viewer_delta_gold_finance_bucket" {
  bucket = module.delta_gold_finance_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "serviceAccount:sa-fin-gke-dbx@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
  ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "binding_delta_bs_planisware_bucket" {
  bucket = module.delta_bs_planisware_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
  ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "binding_landing_planisware_bucket" {
  bucket = module.landing_planisware_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
    "serviceAccount:sa-edi-data-upload-t@za-global-service-accounts-p.iam.gserviceaccount.com"
  ])
  member = each.value
}



/******************************************************
  Databricks Cluster Service Account
******************************************************/
resource "google_service_account" "test_gcs_admin_sa" {
  project      = var.project_id
  account_id   = "sa-gke-gcs-object-admin-t"
  display_name = "Test Databricks Cluster service account for object admins"
}

resource "google_service_account" "test_gcs_reader_sa" {
  project      = var.project_id
  account_id   = "sa-gke-gcs-object-reader-t"
  display_name = "Test Databricks Cluster service account for object readers"
}

#/******************************************************
#   EDI data upload Service Account
#******************************************************/
#resource "google_service_account" "edi_data_upload_gcs_sa" {
#  project      = var.project_id
#  account_id   = "sa-edi-data-upload"
#  display_name = "EDI data upload Service Account"
#}


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