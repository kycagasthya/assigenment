/************************** GCS BUCKETS PERMISSIONS ********************************************************************

# DEV Environment :- its-managed-dbx-ds-01-d
# Permissions: 
      Manage  : "roles/storage.objectAdmin"
      Reader  : "roles/storage.objectViewer"
      Create  : "roles/storage.objectCreator" 

# Groups: 
gcds-its-zap-glo-ds-developers@zebra.com	
gcds-its-zap-goas-ds-developers@zebra.com	
gcds-its-zap-mktg-ds-developers@zebra.com

## Service Accounts:
	
sa-gke-dbx-glo-d@za-global-service-accounts-p.iam.gserviceaccount.com	
sa-gke-dbx-goas-d@za-global-service-accounts-p.iam.gserviceaccount.com	
sa-gke-dbx-marketing-d@za-global-service-accounts-p.iam.gserviceaccount.com	
sa-gke-gcs-ds-object-admin@its-managed-dbx-ds-01-d.iam.gserviceaccount.com	
sa-glo-gke-dbx@its-managed-dbx-ds-01-d.iam.gserviceaccount.com

************************************************************************************************************************/
resource "google_storage_bucket_iam_member" "databricks_2945417879364985_bucket_admin" {
  bucket = data.google_storage_bucket.databricks_2945417879364985.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
     "serviceAccount:sa-gke-gcs-ds-object-admin@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "databricks_2945417879364985_bucket_reader" {
  bucket = data.google_storage_bucket.databricks_2945417879364985.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-glo-ds-developers@zebra.com",
      "group:gcds-its-zap-goas-ds-developers@zebra.com",
      "group:gcds-its-zap-mktg-ds-developers@zebra.com",
      "serviceAccount:sa-gke-dbx-glo-d@za-global-service-accounts-p.iam.gserviceaccount.com",	
      "serviceAccount:sa-gke-dbx-goas-d@za-global-service-accounts-p.iam.gserviceaccount.com",	
      "serviceAccount:sa-gke-dbx-marketing-d@za-global-service-accounts-p.iam.gserviceaccount.com",
      "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
     ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "databricks_2945417879364985_system_admin" {
  bucket = data.google_storage_bucket.databricks_2945417879364985_system.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
     "serviceAccount:sa-gke-gcs-ds-object-admin@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "databricks_2945417879364985_system_reader" {
  bucket = data.google_storage_bucket.databricks_2945417879364985_system.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-glo-ds-developers@zebra.com",
      "group:gcds-its-zap-goas-ds-developers@zebra.com",
      "group:gcds-its-zap-mktg-ds-developers@zebra.com",
      "serviceAccount:sa-gke-dbx-glo-d@za-global-service-accounts-p.iam.gserviceaccount.com",	
      "serviceAccount:sa-gke-dbx-goas-d@za-global-service-accounts-p.iam.gserviceaccount.com",	
      "serviceAccount:sa-gke-dbx-marketing-d@za-global-service-accounts-p.iam.gserviceaccount.com",
      "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
     ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "fin_workarea_bucket_admin" {
  bucket = data.google_storage_bucket.fin_workarea.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
        "serviceAccount:sa-dbx-goassecfin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
        "serviceAccount:sa-dbx-goassecfin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
        "serviceAccount:sa-dbx-fin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
        "serviceAccount:sa-dbx-fin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "fin_workarea_bucket_reader" {
  bucket = data.google_storage_bucket.fin_workarea.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-goas-ds-sec-fin-engineers@zebra.com",
        "group:gcds-its-zap-goas-ds-sec-fin-scientists@zebra.com",
        "group:gcds-its-zap-goas-ds-sec-fin-analysts@zebra.com",
        "group:gcds-its-zap-fin-scientists@zebra.com",
        "group:gcds-its-zap-fin-enginners@zebra.com",
        "group:gcds-its-zap-fin-analysts@zebra.com",
        "serviceAccount:sa-dbx-goassecfin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
        "serviceAccount:sa-dbx-fin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
     ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "glo_workarea_bucket_admin" {
  bucket = data.google_storage_bucket.glo_workarea.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-glo-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-glo-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "glo_workarea_bucket_reader" {
  bucket = data.google_storage_bucket.glo_workarea.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-glo-engineers@zebra.com",
        "group:gcds-its-zap-glo-analysts@zebra.com",
        "group:gcds-its-zap-glo-scientists@zebra.com",
        "serviceAccount:sa-dbx-glo-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
     ])
  member = each.value
}

 resource "google_storage_bucket_iam_member" "goas_finance_bucket_admin" {
   bucket = data.google_storage_bucket.goas_finance.name
   role = "roles/storage.objectAdmin"
   for_each = toset([
     "serviceAccount:sa-gke-gcs-ds-object-admin@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
 	])
  member = each.value
 }
 resource "google_storage_bucket_iam_member" "goas_finance_bucket_reader" {
   bucket = data.google_storage_bucket.goas_finance.name
   role = "roles/storage.objectViewer"
   for_each = toset([
       "group:gcds-its-zap-glo-ds-developers@zebra.com",
       "group:gcds-its-zap-goas-ds-developers@zebra.com",
       "group:gcds-its-zap-mktg-ds-developers@zebra.com",
       "serviceAccount:sa-gke-dbx-glo-d@za-global-service-accounts-p.iam.gserviceaccount.com",	
       "serviceAccount:sa-gke-dbx-goas-d@za-global-service-accounts-p.iam.gserviceaccount.com",	
       "serviceAccount:sa-gke-dbx-marketing-d@za-global-service-accounts-p.iam.gserviceaccount.com",
       "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
      ])
  member = each.value
 }

resource "google_storage_bucket_iam_member" "goas_workarea_bucket_admin" {
  bucket = data.google_storage_bucket.goas_workarea.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-goas-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "goas_workarea_bucket_reader" {
  bucket = data.google_storage_bucket.goas_workarea.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "group:gcds-its-zap-goas-scientists@zebra.com",
    "group:gcds-its-zap-goas-enginners@zebra.com",
    "group:gcds-its-zap-goas-analysts@zebra.com",
    "serviceAccount:sa-dbx-goas-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
     ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "mktg_workarea_bucket_admin" {
  bucket = data.google_storage_bucket.mktg_workarea.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
     "serviceAccount:sa-gke-gcs-ds-object-admin@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "mktg_workarea_bucket_reader" {
  bucket = data.google_storage_bucket.mktg_workarea.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-glo-ds-developers@zebra.com",
      "group:gcds-its-zap-goas-ds-developers@zebra.com",
      "group:gcds-its-zap-mktg-ds-developers@zebra.com",
      "serviceAccount:sa-gke-dbx-glo-d@za-global-service-accounts-p.iam.gserviceaccount.com",	
      "serviceAccount:sa-gke-dbx-goas-d@za-global-service-accounts-p.iam.gserviceaccount.com",	
      "serviceAccount:sa-gke-dbx-marketing-d@za-global-service-accounts-p.iam.gserviceaccount.com",
      "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
     ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "pipeline_code_bucket_admin" {
  bucket = data.google_storage_bucket.pipeline_code.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
     "serviceAccount:sa-gke-gcs-ds-object-admin@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "pipeline_code_bucket_reader" {
  bucket = data.google_storage_bucket.pipeline_code.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-glo-ds-developers@zebra.com",
      "group:gcds-its-zap-goas-ds-developers@zebra.com",
      "group:gcds-its-zap-mktg-ds-developers@zebra.com",
      "serviceAccount:sa-gke-dbx-glo-d@za-global-service-accounts-p.iam.gserviceaccount.com",	
      "serviceAccount:sa-gke-dbx-goas-d@za-global-service-accounts-p.iam.gserviceaccount.com",	
      "serviceAccount:sa-gke-dbx-marketing-d@za-global-service-accounts-p.iam.gserviceaccount.com",
      "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
     ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "user_work_area_bucket_admin" {
  bucket = data.google_storage_bucket.user_work_area.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-goassecfin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goassecfin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-glo-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-glo-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-fin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-fin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "user_work_area_bucket_reader" {
  bucket = data.google_storage_bucket.user_work_area.name
  role = "roles/storage.objectViewer"
  for_each = toset([
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
    "group:gcds-its-zap-sales-scientists@zebra.com",
    "group:gcds-its-zap-sales-enginners@zebra.com",
    "group:gcds-its-zap-sales-analysts@zebra.com",
    "group:gcds-its-zap-edi-ops@zebra.com",
    "serviceAccount:sa-dbx-goassecfin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-glo-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-fin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
     ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "binding_admin_fin_workarea_bucket" {
  bucket = module.fin_workarea_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-fin-gke-dbx@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "group:gcds-its-zap-ds-fin-developers@zebra.com"
  ])
  member = each.value
}
