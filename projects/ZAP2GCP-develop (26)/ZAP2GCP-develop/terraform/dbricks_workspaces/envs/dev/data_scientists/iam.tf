
/******************************************************
  Project IAM Bindings
*******************************************************/
resource "google_project_iam_member" "cluster_sa_log_writer" {
  count   = length(local.service_account_email)
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.dev_gcs_admin_sa.email}"
}

resource "google_project_iam_member" "cluster_sa_metric_writer" {
  count   = length(local.service_account_email)
  project = var.project_id
  role    = "roles/monitoring.metricWriter"
  member  = "serviceAccount:${google_service_account.dev_gcs_admin_sa.email}"
}

resource "google_project_iam_member" "cluster_sa_metric_viewer" {
  count   = length(local.service_account_email)
  project = var.project_id
  role    = "roles/monitoring.viewer"
  member  = "serviceAccount:${google_service_account.dev_gcs_admin_sa.email}"
}

resource "google_project_iam_member" "cluster_sa_metadata_writer" {
  count   = length(local.service_account_email)
  project = var.project_id
  role    = "roles/stackdriver.resourceMetadata.writer"
  member  = "serviceAccount:${google_service_account.dev_gcs_admin_sa.email}"
}

resource "google_project_iam_member" "cluster_sa_storage_admin" {
  project = var.project_id
  role    = "roles/storage.objectAdmin"
  member  = "serviceAccount:${google_service_account.dev_gcs_admin_sa.email}"
}

resource "google_project_iam_member" "cluster_sa_storage_viewer" {
  project = var.dev_project_id
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${google_service_account.dev_gcs_admin_sa.email}"
}
#------------------------------------------------------------------------------

# resource "google_storage_bucket_iam_binding" "binding_admin_fin_workarea_bucket" {
#   bucket = module.fin_workarea_bucket.name
#   role = "roles/storage.objectAdmin"
#   members = [
#     "serviceAccount:sa-fin-gke-dbx@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
#     "group:gcds-its-zap-ds-fin-developers@zebra.com",
#   ]
# }

#Permission for data upload service account to bucket
/* resource "google_storage_bucket_iam_binding" "binding_bucket_delta_bs_grdf" {
  bucket = module.delta_bs_grdf_bucket.name
  role = "roles/storage.objectAdmin"
  members = [
    "user:sa-edi-data-upload@its-managed-dbx-zap-d.iam.gserviceaccount.com",
  ]
} */

/* resource "google_storage_bucket_iam_binding" "binding_bucket_delta_gold_grdf" {
  bucket = module.delta_gold_grdf_bucket.name
  role = "roles/storage.objectAdmin"
  members = [
    "user:sa-edi-data-upload@its-managed-dbx-zap-d.iam.gserviceaccount.com",
  ]
} */

/******************************************************
  Databricks Cluster Service Account
******************************************************/
resource "google_service_account" "dev_gcs_admin_sa" {
  project      = var.project_id
  account_id   = "sa-gke-gcs-ds-object-admin"
  display_name = "Dev Databricks DS Cluster service account for object admins"
}

/* /******************************************************
   EDI data upload Service Account
**********************************************************
resource "google_service_account" "edi_data_upload_gcs_sa" {
  project      = var.project_id
  account_id   = "sa-edi-data-upload"
  display_name = "EDI data upload Service Account"
} */


/******************************************************
  FInance bucket service Account
******************************************************/
resource "google_service_account" "fin-gke-dbx-sa" {
  project      = var.project_id
  account_id   = "sa-fin-gke-dbx"
  display_name = "Finance bucket service account"
}



/******************************************************
   NEW Service Accounts
******************************************************/


# resource "google_service_account" "goassecfin_de_sa" {
#   project      = var.project_id
#   account_id   = "sa-dbx-goassecfin-de-d"
#   display_name = "GOASSECFIN DE service account"
# }

# resource "google_service_account" "goassecfin_ds_sa" {
#   project      = var.project_id
#   account_id   = "sa-dbx-goassecfin-ds-d"
#   display_name = "GOASSECFIN DS service account"
# }

# resource "google_service_account" "goassecfin_da_sa" {
#   project      = var.project_id
#   account_id   = "sa-dbx-goassecfin-da-d"
#   display_name = "GOASSECFIN DA service account"
# }

# resource "google_service_account" "glo_de_sa" {
#   project      = var.project_id
#   account_id   = "sa-dbx-glo-de-d"
#   display_name = "GLO DE service account"
# }

# resource "google_service_account" "glo_ds_sa" {
#   project      = var.project_id
#   account_id   = "sa-dbx-glo-ds-d"
#   display_name = "GLO DS service account"
# }

# resource "google_service_account" "glo_da_sa" {
#   project      = var.project_id
#   account_id   = "sa-dbx-glo-da-d"
#   display_name = "GLO DA service account"
# }


# resource "google_service_account" "goas_de_sa" {
#   project      = var.project_id
#   account_id   = "sa-dbx-goas-de-d"
#   display_name = "GOAS DE service account"
# }

# resource "google_service_account" "goas_ds_sa" {
#   project      = var.project_id
#   account_id   = "sa-dbx-goas-ds-d"
#   display_name = "GOAS DS service account"
# }

# resource "google_service_account" "goas_da_sa" {
#   project      = var.project_id
#   account_id   = "sa-dbx-goas-da-d"
#   display_name = "GOAS DA service account"
# }

# resource "google_service_account" "fin_de_sa" {
#   project      = var.project_id
#   account_id   = "sa-dbx-fin-de-d"
#   display_name = "FIN DE service account"
# }

# resource "google_service_account" "fin_ds_sa" {
#   project      = var.project_id
#   account_id   = "sa-dbx-fin-ds-d"
#   display_name = "FIN DS service account"
# }

# resource "google_service_account" "fin_da_sa" {
#   project      = var.project_id
#   account_id   = "sa-dbx-fin-da-d"
#   display_name = "FIN DA service account"
# }


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