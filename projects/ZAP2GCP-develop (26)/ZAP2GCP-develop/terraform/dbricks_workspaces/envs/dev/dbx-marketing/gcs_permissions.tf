/************************** GCS BUCKETS PERMISSIONS ********************************************************************

# DEV Environment :- its-managed-dbx-mktg-01-d
# Permissions: 
      Manage  : "roles/storage.objectAdmin"
      Reader  : "roles/storage.objectViewer"
      Create  : "roles/storage.objectCreator" 

# Groups: 

gcds-its-zap-mktg-ds-developers@zebra.com 

## Service Accounts:

sa-gke-dbx-marketing-d@za-global-service-accounts-p.iam.gserviceaccount.com	
sa-mktg-dev-gke-gcs-object-adm@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com 

************************************************************************************************************************/
#New Service Accounts and Groups
/************************************************************************************************************************
Project: its-managed-dbx-zap-d
sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com 
sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com 

Project: its-managed-dbx-ds-01-d
@its-managed-dbx-zap-d.iam.gserviceaccount.com
sa-dbx-goassecfin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com  
sa-dbx-goassecfin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com 
sa-dbx-goassecfin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com  
sa-dbx-glo-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com 
sa-dbx-glo-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com 
sa-dbx-glo-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com  
sa-dbx-goas-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com 
sa-dbx-goas-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com 
sa-dbx-goas-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com  
sa-dbx-fin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com 
sa-dbx-fin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com 
sa-dbx-fin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com 

Project: its-managed-dbx-mktg-01-d
sa-dbx-sales-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com 
sa-dbx-sales-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com  
sa-dbx-sales-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com   
sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com  
sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com  
sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com  

Project: za-global-service-accounts-p
sa-rpa-dbx-glo-p@za-global-service-accounts-p.iam.gserviceaccount.com

************************************************************************************************************/



resource "google_storage_bucket_iam_binding" "datascientist_workarea_admin" {
  bucket = data.google_storage_bucket.datascientist_workarea.name
  role = "roles/storage.objectAdmin"
  members = [
    "group:gcds-its-zap-mktg-ds-scientists@zebra.com",
    "group:gcds-its-zap-mktg-ds-engineers@zebra.com",
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	]
}

resource "google_storage_bucket_iam_binding" "dataanalyst_workarea_admin" {
  bucket = data.google_storage_bucket.dataanalyst_workarea.name
  role = "roles/storage.objectAdmin"
  members = [
    "group:gcds-its-zap-mktg-ds-analysts@zebra.com",
    "group:gcds-its-zap-mktg-ds-engineers@zebra.com",
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	]
}

resource "google_storage_bucket_iam_binding" "dataengg_workarea_admin" {
  bucket = data.google_storage_bucket.dataengg_workarea.name
  role = "roles/storage.objectAdmin"
  members = [
    "group:gcds-its-zap-mktg-ds-engineers@zebra.com",
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	]
}


resource "google_storage_bucket_iam_binding" "databricks_389646803545106_admin" {
  bucket = data.google_storage_bucket.databricks_389646803545106.name
  role = "roles/storage.objectAdmin"
  members = [
    "group:gcds-its-zap-mktg-ds-developers@zebra.com",
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
	  "serviceAccount:sa-gke-dbx-marketing-d@za-global-service-accounts-p.iam.gserviceaccount.com",
    "serviceAccount:sa-mktg-dev-gke-gcs-object-adm@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	]
}

resource "google_storage_bucket_iam_binding" "databricks_389646803545106_system_admin" {
  bucket = data.google_storage_bucket.databricks_389646803545106_system.name
  role = "roles/storage.objectAdmin"
  members = [
    "group:gcds-its-zap-mktg-ds-developers@zebra.com",
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
	  "serviceAccount:sa-gke-dbx-marketing-d@za-global-service-accounts-p.iam.gserviceaccount.com",
    "serviceAccount:sa-mktg-dev-gke-gcs-object-adm@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	]
}

resource "google_storage_bucket_iam_binding" "gold_adobe_admin" {
  bucket = data.google_storage_bucket.gold_adobe.name
  role = "roles/storage.objectAdmin"
  members = [
    "group:gcds-its-zap-mktg-ds-developers@zebra.com",
	"serviceAccount:sa-gke-dbx-marketing-d@za-global-service-accounts-p.iam.gserviceaccount.com",
    "serviceAccount:sa-mktg-dev-gke-gcs-object-adm@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	]
}

resource "google_storage_bucket_iam_binding" "gold_demandbase_admin" {
  bucket = data.google_storage_bucket.gold_demandbase.name
  role = "roles/storage.objectAdmin"
  members = [
    "group:gcds-its-zap-mktg-ds-developers@zebra.com",
	"serviceAccount:sa-gke-dbx-marketing-d@za-global-service-accounts-p.iam.gserviceaccount.com",
    "serviceAccount:sa-mktg-dev-gke-gcs-object-adm@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	]
}

resource "google_storage_bucket_iam_binding" "gold_dwa_admin" {
  bucket = data.google_storage_bucket.gold_dwa.name
  role = "roles/storage.objectAdmin"
  members = [
    "group:gcds-its-zap-mktg-ds-developers@zebra.com",
	"serviceAccount:sa-gke-dbx-marketing-d@za-global-service-accounts-p.iam.gserviceaccount.com",
    "serviceAccount:sa-mktg-dev-gke-gcs-object-adm@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	]
}

resource "google_storage_bucket_iam_binding" "gold_eloqua_admin" {
  bucket = data.google_storage_bucket.gold_eloqua.name
  role = "roles/storage.objectAdmin"
  members = [
    "group:gcds-its-zap-mktg-ds-developers@zebra.com",
	"serviceAccount:sa-gke-dbx-marketing-d@za-global-service-accounts-p.iam.gserviceaccount.com",
    "serviceAccount:sa-mktg-dev-gke-gcs-object-adm@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	]
}

resource "google_storage_bucket_iam_binding" "gold_evergage_admin" {
  bucket = data.google_storage_bucket.gold_evergage.name
  role = "roles/storage.objectAdmin"
  members = [
    "group:gcds-its-zap-mktg-ds-developers@zebra.com",
	"serviceAccount:sa-gke-dbx-marketing-d@za-global-service-accounts-p.iam.gserviceaccount.com",
    "serviceAccount:sa-mktg-dev-gke-gcs-object-adm@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	]
}

resource "google_storage_bucket_iam_binding" "gold_gst_admin" {
  bucket = data.google_storage_bucket.gold_gst.name
  role = "roles/storage.objectAdmin"
  members = [
    "group:gcds-its-zap-mktg-ds-developers@zebra.com",
	"serviceAccount:sa-gke-dbx-marketing-d@za-global-service-accounts-p.iam.gserviceaccount.com",
    "serviceAccount:sa-mktg-dev-gke-gcs-object-adm@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	]
}

resource "google_storage_bucket_iam_binding" "gold_m360_admin" {
  bucket = data.google_storage_bucket.gold_m360.name
  role = "roles/storage.objectAdmin"
  members = [
    "group:gcds-its-zap-mktg-ds-developers@zebra.com",
	"serviceAccount:sa-gke-dbx-marketing-d@za-global-service-accounts-p.iam.gserviceaccount.com",
    "serviceAccount:sa-mktg-dev-gke-gcs-object-adm@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	]
}

resource "google_storage_bucket_iam_binding" "gold_partnerprofile_admin" {
  bucket = data.google_storage_bucket.gold_partnerprofile.name
  role = "roles/storage.objectAdmin"
  members = [
    "group:gcds-its-zap-mktg-ds-developers@zebra.com",
	"serviceAccount:sa-gke-dbx-marketing-d@za-global-service-accounts-p.iam.gserviceaccount.com",
    "serviceAccount:sa-mktg-dev-gke-gcs-object-adm@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	]
}

resource "google_storage_bucket_iam_binding" "gold_qualtrics_admin" {
  bucket = data.google_storage_bucket.gold_qualtrics.name
  role = "roles/storage.objectAdmin"
  members = [
    "group:gcds-its-zap-mktg-ds-developers@zebra.com",
	"serviceAccount:sa-gke-dbx-marketing-d@za-global-service-accounts-p.iam.gserviceaccount.com",
    "serviceAccount:sa-mktg-dev-gke-gcs-object-adm@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	]
}

resource "google_storage_bucket_iam_binding" "gold_sfdc_admin" {
  bucket = data.google_storage_bucket.gold_sfdc.name
  role = "roles/storage.objectAdmin"
  members = [
    "group:gcds-its-zap-mktg-ds-developers@zebra.com",
	"serviceAccount:sa-gke-dbx-marketing-d@za-global-service-accounts-p.iam.gserviceaccount.com",
    "serviceAccount:sa-mktg-dev-gke-gcs-object-adm@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	]
}

resource "google_storage_bucket_iam_binding" "gold_turtl_admin" {
  bucket = data.google_storage_bucket.gold_turtl.name
  role = "roles/storage.objectAdmin"
  members = [
    "group:gcds-its-zap-mktg-ds-developers@zebra.com",
	"serviceAccount:sa-gke-dbx-marketing-d@za-global-service-accounts-p.iam.gserviceaccount.com",
    "serviceAccount:sa-mktg-dev-gke-gcs-object-adm@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	]
}

resource "google_storage_bucket_iam_binding" "gold_vistex_admin" {
  bucket = data.google_storage_bucket.gold_vistex.name
  role = "roles/storage.objectAdmin"
  members = [
    "group:gcds-its-zap-mktg-ds-developers@zebra.com",
	"serviceAccount:sa-gke-dbx-marketing-d@za-global-service-accounts-p.iam.gserviceaccount.com",
    "serviceAccount:sa-mktg-dev-gke-gcs-object-adm@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	]
}

resource "google_storage_bucket_iam_binding" "landing_dwa_admin" {
  bucket = data.google_storage_bucket.landing_dwa.name
  role = "roles/storage.objectAdmin"
  members = [
    "group:gcds-its-zap-mktg-ds-developers@zebra.com",
	"serviceAccount:sa-gke-dbx-marketing-d@za-global-service-accounts-p.iam.gserviceaccount.com",
    "serviceAccount:sa-mktg-dev-gke-gcs-object-adm@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	]
}

resource "google_storage_bucket_iam_binding" "pipeline_code_admin" {
  bucket = data.google_storage_bucket.pipeline_code.name
  role = "roles/storage.objectAdmin"
  members = [
    "group:gcds-its-zap-mktg-ds-developers@zebra.com",
	"serviceAccount:sa-gke-dbx-marketing-d@za-global-service-accounts-p.iam.gserviceaccount.com",
    "serviceAccount:sa-mktg-dev-gke-gcs-object-adm@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	]
}
