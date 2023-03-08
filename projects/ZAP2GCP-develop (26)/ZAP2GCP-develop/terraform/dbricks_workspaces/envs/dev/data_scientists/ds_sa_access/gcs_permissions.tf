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
# New Service Accounts and Group
/************************************************************************************************************************
"serviceAccount:sa-dbx-goassecfin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"  
"serviceAccount:sa-dbx-goassecfin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com" 
"serviceAccount:sa-dbx-goassecfin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"  
"serviceAccount:sa-dbx-glo-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com" 
"serviceAccount:sa-dbx-glo-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com" 
"serviceAccount:sa-dbx-glo-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"  
"serviceAccount:sa-dbx-goas-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com" 
"serviceAccount:sa-dbx-goas-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com" 
"serviceAccount:sa-dbx-goas-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"  
"serviceAccount:sa-dbx-fin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com" 
"serviceAccount:sa-dbx-fin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com" 
"serviceAccount:sa-dbx-fin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"

sa-sql-endpoint-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com" 

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
"group:gcds-its-zap-fin-analysts@zebra.com"

************************************************************************************************************************/

module "glo_engineers_workarea_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-glo-engineers-workarea"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
}

module "glo_analysts_workarea_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-glo-analysts-workarea"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
}

module "glo_scientists_workarea_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-glo-scientists-workarea"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
}

module "goas_scientists_workarea_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-goas-scientists-workarea"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
}

module "goas_enginners_workarea_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-goas-enginners-workarea"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
}

module "goas_analysts_workarea_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-goas-analysts-workarea"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
}


module "fin_scientists_workarea_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-fin-scientists-workarea"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
}

module "fin_enginners_workarea_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-fin-enginners-workarea"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
}

module "fin_analysts_workarea_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-fin-analysts-workarea"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
}

module "goas_fin_engineers_workarea_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-goas-ds-sec-fin-engineers-workarea"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
}

module "goas_fin_scientists_workarea_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-goas-ds-sec-fin-scientists-workarea"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
}

module "goas_fin_analysts_workarea_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-goas-ds-sec-fin-analysts-workarea"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
}

#########################################################################################################
# sa-sql-endpoint-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com

resource "google_service_account" "sql_endpoint_ds_dev_sa" {
  project      = var.project_id
  account_id   = "sa-sql-endpoint-ds-d" #Prod service account id name for object reader access
  display_name = "Data Science DEV Service Account for SQL Endpoint"
}

resource "google_project_iam_member" "sql_endpoint_ds_dev_sa_admin" {
  project = var.project_id
  role    = "roles/storage.objectAdmin"
  member  = "serviceAccount:sa-sql-endpoint-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
  depends_on = [
    google_service_account.sql_endpoint_ds_dev_sa
  ]
}

resource "google_project_iam_member" "sql_endpoint_ds_dev_de_sa_admin" {
  project = "its-managed-dbx-zap-d"
  role    = "roles/storage.objectAdmin"
  member  = "serviceAccount:sa-sql-endpoint-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
  depends_on = [
    google_service_account.sql_endpoint_ds_dev_sa
  ]
}

resource "google_storage_bucket_iam_member" "databricks_2945417879364985_bucket_adm" {
  bucket = data.google_storage_bucket.databricks_2945417879364985.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
     "serviceAccount:sa-gke-gcs-ds-object-admin@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
     "serviceAccount:sa-dbx-goassecfin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
     "serviceAccount:sa-dbx-goassecfin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
     "serviceAccount:sa-dbx-goassecfin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",  
     "serviceAccount:sa-dbx-glo-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
     "serviceAccount:sa-dbx-glo-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
     "serviceAccount:sa-dbx-glo-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",  
     "serviceAccount:sa-dbx-goas-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
     "serviceAccount:sa-dbx-goas-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
     "serviceAccount:sa-dbx-goas-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",  
     "serviceAccount:sa-dbx-fin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
     "serviceAccount:sa-dbx-fin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
     "serviceAccount:sa-dbx-fin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "databricks_2945417879364985_bucket_read" {
  bucket = data.google_storage_bucket.databricks_2945417879364985.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-glo-ds-developers@zebra.com",
      "group:gcds-its-zap-goas-ds-developers@zebra.com",
      "group:gcds-its-zap-mktg-ds-developers@zebra.com",
      "serviceAccount:sa-gke-dbx-glo-d@za-global-service-accounts-p.iam.gserviceaccount.com",	
      "serviceAccount:sa-gke-dbx-goas-d@za-global-service-accounts-p.iam.gserviceaccount.com",	
      "serviceAccount:sa-gke-dbx-marketing-d@za-global-service-accounts-p.iam.gserviceaccount.com",
      "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
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
      "group:gcds-its-zap-fin-analysts@zebra.com"
     ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "databricks_2945417879364985_system_adm" {
  bucket = data.google_storage_bucket.databricks_2945417879364985_system.name
  role = "roles/storage.objectAdmin"
  for_each = toset([     
     "serviceAccount:sa-gke-gcs-ds-object-admin@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
     "serviceAccount:sa-dbx-goassecfin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
     "serviceAccount:sa-dbx-goassecfin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
     "serviceAccount:sa-dbx-goassecfin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",  
     "serviceAccount:sa-dbx-glo-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
     "serviceAccount:sa-dbx-glo-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
     "serviceAccount:sa-dbx-glo-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",  
     "serviceAccount:sa-dbx-goas-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
     "serviceAccount:sa-dbx-goas-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
     "serviceAccount:sa-dbx-goas-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",  
     "serviceAccount:sa-dbx-fin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
     "serviceAccount:sa-dbx-fin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
     "serviceAccount:sa-dbx-fin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "databricks_2945417879364985_system_read" {
  bucket = data.google_storage_bucket.databricks_2945417879364985_system.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-glo-ds-developers@zebra.com",
      "group:gcds-its-zap-goas-ds-developers@zebra.com",
      "group:gcds-its-zap-mktg-ds-developers@zebra.com",
      "serviceAccount:sa-gke-dbx-glo-d@za-global-service-accounts-p.iam.gserviceaccount.com",	
      "serviceAccount:sa-gke-dbx-goas-d@za-global-service-accounts-p.iam.gserviceaccount.com",	
      "serviceAccount:sa-gke-dbx-marketing-d@za-global-service-accounts-p.iam.gserviceaccount.com",
      "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
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
      "group:gcds-its-zap-fin-analysts@zebra.com"
     ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "pipeline_code_bucket_admin" {
  bucket = data.google_storage_bucket.pipeline_code.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
     "serviceAccount:sa-gke-gcs-ds-object-admin@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
     "serviceAccount:sa-gke-gcs-ds-object-admin@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
     "serviceAccount:sa-dbx-goassecfin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
     "serviceAccount:sa-dbx-goassecfin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
     "serviceAccount:sa-dbx-goassecfin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",  
     "serviceAccount:sa-dbx-glo-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
     "serviceAccount:sa-dbx-glo-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
     "serviceAccount:sa-dbx-glo-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",  
     "serviceAccount:sa-dbx-goas-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
     "serviceAccount:sa-dbx-goas-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
     "serviceAccount:sa-dbx-goas-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",  
     "serviceAccount:sa-dbx-fin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
     "serviceAccount:sa-dbx-fin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
     "serviceAccount:sa-dbx-fin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "pipeline_code_bucket_reader" {
  bucket = data.google_storage_bucket.pipeline_code.name
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
      "group:gcds-its-zap-fin-analysts@zebra.com"
     ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "glo_engineers_bucket_admin" {
  bucket = data.google_storage_bucket.glo_engineers_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
     "serviceAccount:sa-dbx-glo-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
     "group:gcds-its-zap-glo-engineers@zebra.com"
    ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "glo_scientists_bucket_admin" {
  bucket = data.google_storage_bucket.glo_scientists_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
     "serviceAccount:sa-dbx-glo-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
     "group:gcds-its-zap-glo-scientists@zebra.com"
    ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "glo_analysts_bucket_admin" {
  bucket = data.google_storage_bucket.glo_analysts_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
     "serviceAccount:sa-dbx-glo-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
     "group:gcds-its-zap-glo-analysts@zebra.com"
    ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "goas_enginners_bucket_admin" {
  bucket = data.google_storage_bucket.goas_enginners_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
     "serviceAccount:sa-dbx-goas-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
     "group:gcds-its-zap-goas-enginners@zebra.com"
    ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "goas_scientists_bucket_admin" {
  bucket = data.google_storage_bucket.goas_scientists_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
     "serviceAccount:sa-dbx-goas-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
     "group:gcds-its-zap-goas-scientists@zebra.com"
    ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "goas_analysts_bucket_admin" {
  bucket = data.google_storage_bucket.goas_analysts_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
     "serviceAccount:sa-dbx-goas-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
     "group:gcds-its-zap-goas-analysts@zebra.com"
    ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "fin_scientists_bucket_admin" {
  bucket = data.google_storage_bucket.fin_scientists_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
     "serviceAccount:sa-dbx-fin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
     "group:gcds-its-zap-fin-scientists@zebra.com"
    ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "fin_enginners_bucket_admin" {
  bucket = data.google_storage_bucket.fin_enginners_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
     "serviceAccount:sa-dbx-fin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
     "group:gcds-its-zap-fin-enginners@zebra.com"
    ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "fin_analysts_bucket_admin" {
  bucket = data.google_storage_bucket.fin_analysts_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
     "serviceAccount:sa-dbx-fin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
     "group:gcds-its-zap-fin-analysts@zebra.com"
    ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "sec_fin_engineers_bucket_admin" {
  bucket = data.google_storage_bucket.sec_fin_engineers_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
     "serviceAccount:sa-dbx-goassecfin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
     "group:gcds-its-zap-goas-ds-sec-fin-engineers@zebra.com"
    ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "sec_fin_scientists_bucket_admin" {
  bucket = data.google_storage_bucket.sec_fin_scientists_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
     "serviceAccount:sa-dbx-goassecfin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
     "group:gcds-its-zap-goas-ds-sec-fin-scientists@zebra.com"
    ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "sec_fin_analysts_bucket_admin" {
  bucket = data.google_storage_bucket.sec_fin_analysts_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
     "serviceAccount:sa-dbx-goassecfin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
     "group:gcds-its-zap-goas-ds-sec-fin-analysts@zebra.com"
    ])
  member = each.value
}
##
resource "google_storage_bucket_iam_member" "delta_bs_eol_ds_access_bucket_read" {
  bucket = data.google_storage_bucket.delta_bs_eol_ds_access.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "serviceAccount:sa-dbx-goassecfin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",  
    "serviceAccount:sa-dbx-goassecfin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goassecfin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "group:gcds-its-zap-goas-ds-sec-fin-engineers@zebra.com",	
    "group:gcds-its-zap-goas-ds-sec-fin-scientists@zebra.com",	
    "group:gcds-its-zap-goas-ds-sec-fin-analysts@zebra.com",
    "serviceAccount:sa-dbx-goas-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goas-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goas-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "group:gcds-its-zap-goas-scientists@zebra.com",	
    "group:gcds-its-zap-goas-enginners@zebra.com",	
    "group:gcds-its-zap-goas-analysts@zebra.com"
    ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "delta_bs_glo_ds_access_bucket_read" {
  bucket = data.google_storage_bucket.delta_bs_glo_ds_access.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "serviceAccount:sa-dbx-glo-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-glo-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-glo-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "group:gcds-its-zap-glo-engineers@zebra.com",	
    "group:gcds-its-zap-glo-analysts@zebra.com",
    "group:gcds-its-zap-glo-scientists@zebra.com"
    ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "delta_bs_grdf_ds_access_bucket_read" {
  bucket = data.google_storage_bucket.delta_bs_grdf_ds_access.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "serviceAccount:sa-dbx-goassecfin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",  
    "serviceAccount:sa-dbx-goassecfin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goassecfin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "group:gcds-its-zap-goas-ds-sec-fin-engineers@zebra.com",	
    "group:gcds-its-zap-goas-ds-sec-fin-scientists@zebra.com",	
    "group:gcds-its-zap-goas-ds-sec-fin-analysts@zebra.com",
    "serviceAccount:sa-dbx-goas-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goas-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goas-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "group:gcds-its-zap-goas-scientists@zebra.com",	
    "group:gcds-its-zap-goas-enginners@zebra.com",	
    "group:gcds-its-zap-goas-analysts@zebra.com"
    ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "delta_bs_gst_access_bucket_read" {
  bucket = data.google_storage_bucket.delta_bs_gst_ds_access.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "serviceAccount:sa-dbx-goassecfin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",  
    "serviceAccount:sa-dbx-goassecfin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goassecfin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "group:gcds-its-zap-goas-ds-sec-fin-engineers@zebra.com",	
    "group:gcds-its-zap-goas-ds-sec-fin-scientists@zebra.com",	
    "group:gcds-its-zap-goas-ds-sec-fin-analysts@zebra.com",
    "serviceAccount:sa-dbx-goas-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goas-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goas-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "group:gcds-its-zap-goas-scientists@zebra.com",	
    "group:gcds-its-zap-goas-enginners@zebra.com",	
    "group:gcds-its-zap-goas-analysts@zebra.com",
    "serviceAccount:sa-dbx-fin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-fin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-fin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "group:gcds-its-zap-fin-scientists@zebra.com",	
    "group:gcds-its-zap-fin-enginners@zebra.com",	
    "group:gcds-its-zap-fin-analysts@zebra.com"
    ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "delta_bs_planib_access_bucket_read" {
  bucket = data.google_storage_bucket.delta_bs_planib_ds_access.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "serviceAccount:sa-dbx-goassecfin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",  
    "serviceAccount:sa-dbx-goassecfin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goassecfin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "group:gcds-its-zap-goas-ds-sec-fin-engineers@zebra.com",	
    "group:gcds-its-zap-goas-ds-sec-fin-scientists@zebra.com",	
    "group:gcds-its-zap-goas-ds-sec-fin-analysts@zebra.com",
    "serviceAccount:sa-dbx-goas-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goas-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goas-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "group:gcds-its-zap-goas-scientists@zebra.com",	
    "group:gcds-its-zap-goas-enginners@zebra.com",	
    "group:gcds-its-zap-goas-analysts@zebra.com"
    ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "delta_bs_rma_access_bucket_read" {
  bucket = data.google_storage_bucket.delta_bs_rma_ds_access.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "serviceAccount:sa-dbx-goassecfin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",  
    "serviceAccount:sa-dbx-goassecfin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goassecfin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "group:gcds-its-zap-goas-ds-sec-fin-engineers@zebra.com",	
    "group:gcds-its-zap-goas-ds-sec-fin-scientists@zebra.com",	
    "group:gcds-its-zap-goas-ds-sec-fin-analysts@zebra.com",
    "serviceAccount:sa-dbx-goas-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goas-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goas-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "group:gcds-its-zap-goas-scientists@zebra.com",	
    "group:gcds-its-zap-goas-enginners@zebra.com",	
    "group:gcds-its-zap-goas-analysts@zebra.com"
    ])
  member = each.value
}


resource "google_storage_bucket_iam_member" "delta_bs_sfdc_access_bucket_read" {
  bucket = data.google_storage_bucket.delta_bs_sfdc_ds_access.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "serviceAccount:sa-dbx-goassecfin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",  
    "serviceAccount:sa-dbx-goassecfin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goassecfin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "group:gcds-its-zap-goas-ds-sec-fin-engineers@zebra.com",	
    "group:gcds-its-zap-goas-ds-sec-fin-scientists@zebra.com",	
    "group:gcds-its-zap-goas-ds-sec-fin-analysts@zebra.com",
    "serviceAccount:sa-dbx-goas-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goas-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goas-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "group:gcds-its-zap-goas-scientists@zebra.com",	
    "group:gcds-its-zap-goas-enginners@zebra.com",	
    "group:gcds-its-zap-goas-analysts@zebra.com",
    "serviceAccount:sa-dbx-fin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-fin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-fin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "group:gcds-its-zap-fin-scientists@zebra.com",	
    "group:gcds-its-zap-fin-enginners@zebra.com",	
    "group:gcds-its-zap-fin-analysts@zebra.com"
    ])
  member = each.value
}


resource "google_storage_bucket_iam_member" "delta_gold_grdf_access_bucket_read" {
  bucket = data.google_storage_bucket.delta_bs_gold_grdf_access.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "serviceAccount:sa-dbx-goassecfin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",  
    "serviceAccount:sa-dbx-goassecfin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goassecfin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "group:gcds-its-zap-goas-ds-sec-fin-engineers@zebra.com",	
    "group:gcds-its-zap-goas-ds-sec-fin-scientists@zebra.com",	
    "group:gcds-its-zap-goas-ds-sec-fin-analysts@zebra.com",
    "serviceAccount:sa-dbx-goas-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goas-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goas-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "group:gcds-its-zap-goas-scientists@zebra.com",	
    "group:gcds-its-zap-goas-enginners@zebra.com",	
    "group:gcds-its-zap-goas-analysts@zebra.com"
    ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "delta_bs_goas_access_bucket_read" {
  bucket = data.google_storage_bucket.delta_bs_goas_access.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "serviceAccount:sa-dbx-goassecfin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",  
    "serviceAccount:sa-dbx-goassecfin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goassecfin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "group:gcds-its-zap-goas-ds-sec-fin-engineers@zebra.com",	
    "group:gcds-its-zap-goas-ds-sec-fin-scientists@zebra.com",	
    "group:gcds-its-zap-goas-ds-sec-fin-analysts@zebra.com",
    "serviceAccount:sa-dbx-goas-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goas-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goas-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "group:gcds-its-zap-goas-scientists@zebra.com",	
    "group:gcds-its-zap-goas-enginners@zebra.com",	
    "group:gcds-its-zap-goas-analysts@zebra.com"
    ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "delta_bs_finance_access_bucket_read" {
  bucket = data.google_storage_bucket.delta_bs_finance_ds_access.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "serviceAccount:sa-dbx-fin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-fin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-fin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "group:gcds-its-zap-fin-scientists@zebra.com",	
    "group:gcds-its-zap-fin-enginners@zebra.com",	
    "group:gcds-its-zap-fin-analysts@zebra.com"
    ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "delta_bs_ihs_access_bucket_read" {
  bucket = data.google_storage_bucket.delta_bs_ihs_ds_access.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "serviceAccount:sa-dbx-goassecfin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",  
    "serviceAccount:sa-dbx-goassecfin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goassecfin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "group:gcds-its-zap-goas-ds-sec-fin-engineers@zebra.com",	
    "group:gcds-its-zap-goas-ds-sec-fin-scientists@zebra.com",	
    "group:gcds-its-zap-goas-ds-sec-fin-analysts@zebra.com",
    "serviceAccount:sa-dbx-goas-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goas-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goas-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "group:gcds-its-zap-goas-scientists@zebra.com",	
    "group:gcds-its-zap-goas-enginners@zebra.com",	
    "group:gcds-its-zap-goas-analysts@zebra.com",
    "serviceAccount:sa-dbx-fin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-fin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-fin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "group:gcds-its-zap-fin-scientists@zebra.com",	
    "group:gcds-its-zap-fin-enginners@zebra.com",	
    "group:gcds-its-zap-fin-analysts@zebra.com"
    ])
  member = each.value
}