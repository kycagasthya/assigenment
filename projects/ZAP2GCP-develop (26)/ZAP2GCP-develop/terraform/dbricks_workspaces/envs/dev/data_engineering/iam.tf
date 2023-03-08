
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

/******************************************************
  Databricks Cluster Service Account
******************************************************/
resource "google_service_account" "dev_gcs_admin_sa" {
  project      = var.project_id
  account_id   = "sa-gke-gcs-object-admin"
  display_name = "Dev Databricks Cluster service account for object admins"
}

resource "google_service_account" "dev_gcs_reader_sa" {
  project      = var.project_id
  account_id   = "sa-gke-gcs-object-reader"
  display_name = "Dev Databricks Cluster service account for object readers"
}

resource "google_service_account" "bigquery_api_sa" {
  project      = var.project_id
  account_id   = "sa-cloudrun-bigquery-api"
  display_name = "Bigquery API service account to export data"
}

resource "google_project_iam_member" "bigqueri_api_serviceaccount_user" {
  project = var.project_id
  role    = "roles/iam.serviceAccountUser"
  member  = "serviceAccount:sa-cloudrun-bigquery-api@its-managed-dbx-zap-d.iam.gserviceaccount.com"
  depends_on = [
    google_service_account.bigquery_api_sa
  ]
}

resource "google_project_iam_member" "bigqueri_api_cloudrun_dev" {
  project = var.project_id
  role    = "roles/run.admin"
  member  = "serviceAccount:sa-cloudrun-bigquery-api@its-managed-dbx-zap-d.iam.gserviceaccount.com"
  depends_on = [
    google_service_account.bigquery_api_sa
  ]
}

resource "google_project_iam_member" "bigqueri_api_bq_user" {
  project = var.project_id
  role    = "roles/bigquery.user"
  member  = "serviceAccount:sa-cloudrun-bigquery-api@its-managed-dbx-zap-d.iam.gserviceaccount.com"
  depends_on = [
    google_service_account.bigquery_api_sa
  ]
}
resource "google_service_account_iam_member" "admin-account-iam" {
  service_account_id = google_service_account.bigquery_api_sa.name
  role               = "roles/iam.serviceAccountUser"
  member             = "group:gcds-its-zap-de-developers@zebra.com"
}

resource "google_service_account_iam_member" "registry-iam" {
  service_account_id = google_service_account.bigquery_api_sa.name
  role               = "roles/artifactregistry.writer"
  member             = "group:gcds-its-zap-de-developers@zebra.com"
}

resource "google_project_iam_member" "bigqueri_api_artifact_access" {
  project = var.project_id
  role    = "roles/artifactregistry.writer"
  member  = "serviceAccount:sa-cloudrun-bigquery-api@its-managed-dbx-zap-d.iam.gserviceaccount.com"
  depends_on = [
    google_service_account.bigquery_api_sa
  ]
}



/******************************************************
   EDI data upload Service Account
******************************************************/
#resource "google_service_account" "edi_data_upload_gcs_sa" {
#  project      = var.project_id
#  account_id   = "sa-edi-data-upload"
#  display_name = "EDI data upload Service Account"
#}


/******************************************************
   IAM permissions for Service account and Groups
******************************************************/

# #Custom Storage bucket viewer
# resource "google_project_iam_member" "custom_object_viewer" {
#   count   = length(local.custom_bucket_viewer_sa_email)
#   project = var.project_id
#   role    = "roles/organizations/463373134989/roles/CustomRole85"
#   member  = local.custom_bucket_viewer_sa_email[count.index]
# }

#logs writer
resource "google_project_iam_member" "cluster_sa_log_writer_dbx" {
  count   = length(local.log_writer_dbx_sa_email)
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = local.log_writer_dbx_sa_email[count.index]
}

#monitoring metric writer
resource "google_project_iam_member" "cluster_sa_metric_writer_dbx" {
  count   = length(local.log_writer_dbx_sa_email)
  project = var.project_id
  role    = "roles/monitoring.metricWriter"
  member  = local.log_writer_dbx_sa_email[count.index]
}

# monitoring viewer
resource "google_project_iam_member" "cluster_sa_metric_viewer_dbx" {
  count   = length(local.log_writer_dbx_sa_email)
  project = var.project_id
  role    = "roles/monitoring.viewer"
  member  = local.log_writer_dbx_sa_email[count.index]
}

#stackdriver resource metdata writer
resource "google_project_iam_member" "cluster_sa_metadata_writer_dbx" {
  count   = length(local.log_writer_dbx_sa_email)
  project = var.project_id
  role    = "roles/stackdriver.resourceMetadata.writer"
  member  = local.log_writer_dbx_sa_email[count.index]
}

#Security reviewer
resource "google_project_iam_member" "sa_security_reviewer" {
  count   = length(local.sa_security_reviewer_email)
  project = var.project_id
  role    = "roles/iam.securityReviewer"
  member  = local.sa_security_reviewer_email[count.index]
}

#Bigquery Job User
resource "google_project_iam_member" "bigquery_job_user" {
  project = var.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
}

#BigQuery Read Session User
resource "google_project_iam_member" "bigquery_read_session_user" {
  project = var.project_id
  role    = "roles/bigquery.readSessionUser"
  member  = "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
}

#Secret Manager Secret Accessor
resource "google_project_iam_member" "secret_manager_accessor" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
}

# #Storage Object Admin
# resource "google_project_iam_member" "storage_admin" {
#   project = var.project_id
#   role    = "roles/storage.objectAdmin"
#   member  = [
#     ""
  
#    ]
# }

# #Storage Object Viewer
# resource "google_project_iam_member" "storage_viewer" {
#   project = var.project_id
#   role    = "roles/storage.objectViewer"
#   member  = [
#     ""
#    ]
# }
