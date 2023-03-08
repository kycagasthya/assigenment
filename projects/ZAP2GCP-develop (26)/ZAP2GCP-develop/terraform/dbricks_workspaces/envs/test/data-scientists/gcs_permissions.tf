/************************** GCS BUCKETS PERMISSIONS ********************************************************************

# TEST Environment :- its-managed-dbx-ds-01-t
# Permissions:  
    Manage  : "roles/storage.objectAdmin" 
    Reader  : "roles/storage.objectViewer" 
    Create  : "roles/storage.objectCreator" 


## Service Accounts:

sa-gke-gcs-ds-object-admin@its-managed-dbx-ds-01-t.iam.gserviceaccount.com - CBV	
sa-glo-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com - R
sa-gke-gcs-ds-object-admin@its-managed-dbx-ds-01-t.iam.gserviceaccount.com - M

************************************************************************************************************************/

resource "google_storage_bucket_iam_member" "databricks_2348922014507522_bucket_admin" {
  bucket = data.google_storage_bucket.databricks_2348922014507522.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
     "serviceAccount:sa-gke-gcs-ds-object-admin@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "databricks_2348922014507522_bucket_reader" {
  bucket = data.google_storage_bucket.databricks_2348922014507522.name
  role = "roles/storage.objectViewer"
  for_each = toset([
     "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
      "group:gcds-its-zap-glo-ds-developers@zebra.com",
      "group:gcds-its-zap-goas-ds-developers@zebra.com",
      "group:gcds-its-zap-mktg-ds-developers@zebra.com",
      "serviceAccount:sa-gke-dbx-glo-d@za-global-service-accounts-p.iam.gserviceaccount.com",	
      "serviceAccount:sa-gke-dbx-goas-d@za-global-service-accounts-p.iam.gserviceaccount.com",	
      "serviceAccount:sa-gke-dbx-marketing-d@za-global-service-accounts-p.iam.gserviceaccount.com"
     ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "databricks_2348922014507522_system_admin" {
  bucket = data.google_storage_bucket.databricks_2348922014507522_system.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
     "serviceAccount:sa-gke-gcs-ds-object-admin@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "databricks_2348922014507522_system_reader" {
  bucket = data.google_storage_bucket.databricks_2348922014507522_system.name
  role = "roles/storage.objectViewer"
  for_each = toset([
     "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
      "group:gcds-its-zap-glo-ds-developers@zebra.com",
      "group:gcds-its-zap-goas-ds-developers@zebra.com",
      "group:gcds-its-zap-mktg-ds-developers@zebra.com",
      "serviceAccount:sa-gke-dbx-glo-d@za-global-service-accounts-p.iam.gserviceaccount.com",	
      "serviceAccount:sa-gke-dbx-goas-d@za-global-service-accounts-p.iam.gserviceaccount.com",	
      "serviceAccount:sa-gke-dbx-marketing-d@za-global-service-accounts-p.iam.gserviceaccount.com"
     ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "glo_workarea_bucket_admin" {
  bucket = data.google_storage_bucket.glo_workarea.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
     "serviceAccount:sa-gke-gcs-ds-object-admin@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
     "serviceAccount:sa-dbx-glo-de-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
     "serviceAccount:sa-dbx-glo-ds-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "glo_workarea_bucket_reader" {
  bucket = data.google_storage_bucket.glo_workarea.name
  role = "roles/storage.objectViewer"
  for_each = toset([
     "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
      "group:gcds-its-zap-glo-engineers@zebra.com",
      "group:gcds-its-zap-glo-analysts@zebra.com",
      "group:gcds-its-zap-glo-scientists@zebra.com"
     ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "goas_finance_bucket_admin" {
  bucket = data.google_storage_bucket.goas_finance.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
     "serviceAccount:sa-gke-gcs-ds-object-admin@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "goas_finance_bucket_reader" {
  bucket = data.google_storage_bucket.goas_finance.name
  role = "roles/storage.objectViewer"
  for_each = toset([
     "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
      "group:gcds-its-zap-glo-ds-developers@zebra.com",
      "group:gcds-its-zap-goas-ds-developers@zebra.com",
      "group:gcds-its-zap-mktg-ds-developers@zebra.com"
     ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "goas_workarea_bucket_admin" {
  bucket = data.google_storage_bucket.goas_workarea.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
     "serviceAccount:sa-gke-gcs-ds-object-admin@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
     "serviceAccount:sa-dbx-goas-de-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
     "serviceAccount:sa-dbx-goas-ds-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "goas_workarea_bucket_reader" {
  bucket = data.google_storage_bucket.goas_workarea.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
    "group:gcds-its-zap-goas-scientists@zebra.com",
    "group:gcds-its-zap-goas-enginners@zebra.com",
    "group:gcds-its-zap-goas-analysts@zebra.com",
    "serviceAccount:sa-dbx-goas-da-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"
     ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "mktg_workarea_bucket_admin" {
  bucket = data.google_storage_bucket.mktg_workarea.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
     "serviceAccount:sa-gke-gcs-ds-object-admin@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"

	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "mktg_workarea_bucket_reader" {
  bucket = data.google_storage_bucket.mktg_workarea.name
  role = "roles/storage.objectViewer"
  for_each = toset([
     "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
     "group:gcds-its-zap-glo-ds-developers@zebra.com",
      "group:gcds-its-zap-goas-ds-developers@zebra.com",
      "group:gcds-its-zap-mktg-ds-developers@zebra.com"
     ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "pipeline_code_bucket_admin" {
  bucket = data.google_storage_bucket.pipeline_code.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
     "serviceAccount:sa-gke-gcs-ds-object-admin@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "pipeline_code_bucket_reader" {
  bucket = data.google_storage_bucket.pipeline_code.name
  role = "roles/storage.objectViewer"
  for_each = toset([
     "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
     "group:gcds-its-zap-glo-ds-developers@zebra.com",
      "group:gcds-its-zap-goas-ds-developers@zebra.com",
      "group:gcds-its-zap-mktg-ds-developers@zebra.com"
     ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "user_work_area_bucket_admin" {
  bucket = data.google_storage_bucket.user_work_area.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-gke-gcs-ds-object-admin@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goassecfin-de-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goassecfin-ds-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-glo-de-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-glo-ds-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-de-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-ds-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-fin-de-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-fin-ds-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "user_work_area_bucket_reader" {
  bucket = data.google_storage_bucket.user_work_area.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
    "group:gcds-its-zap-goas-ds-sec-fin-engineers@zebra.com",
    "group:gcds-its-zap-goas-ds-sec-fin-scientists@zebra.com",
    "group:gcds-its-zap-goas-ds-sec-fin-analysts@zebra.com",
    "group:gcds-its-zap-glo-engineers@zebra.com",
    "group:gcds-its-zap-glo-analysts@zebra.com",
    "group:gcds-its-zap-glo-scientists@zebra.com",
    "group:gcds-its-zap-goas-scientists@zebra.com",
    "group:gcds-its-zap-goas-enginners@zebra.com",
    "group:gcds-its-zap-goas-analysts@zebra.com",
    "group:gcds-its-zap-fin-scientists@zebra.com",
    "group:gcds-its-zap-fin-enginners@zebra.com",
    "group:gcds-its-zap-fin-analysts@zebra.com",
    "group:gcds-its-zap-edi-ops@zebra.com",
    "serviceAccount:sa-dbx-goassecfin-da-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-glo-da-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-da-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-fin-da-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"
     ])
  member = each.value
}
