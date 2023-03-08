/************************** GCS BUCKETS PERMISSIONS ********************************************************************

# DEV Environment :- its-managed-dbx-zap-d
# Permissions: 
      Manage  : "roles/storage.objectAdmin"
      Reader  : "roles/storage.objectViewer"
      Create  : "roles/storage.objectCreator" 

# Groups: 
gcds-its-managed-dbx-zap-d-cloud-functions-developer@zebra.com	
gcds-its-zap-de-ops@zebra.com	gcds-its-zap-de-developers@zebra.com	
gcds-its-zap-glo-ds-developers@zebra.com	gcds-its-zap-goas-ds-developers@zebra.com	
gcds-its-zap-mktg-ds-developers@zebra.com	

## Service Accounts:
sa-gke-dbx-glo-d@za-global-service-accounts-p.iam.gserviceaccount.com	
sa-gke-dbx-goas-d@za-global-service-accounts-p.iam.gserviceaccount.com	
sa-gke-dbx-marketing-d@za-global-service-accounts-p.iam.gserviceaccount.com	
sa-gke-gcs-ds-object-admin@its-managed-dbx-ds-01-d.iam.gserviceaccount.com	
sa-gke-gcs-object-admin@its-managed-dbx-zap-d.iam.gserviceaccount.com	
sa-gke-gcs-object-reader@its-managed-dbx-zap-d.iam.gserviceaccount.com	
sa-iics-gcs-object-create-view@its-managed-dbx-zap-d.iam.gserviceaccount.com	
sa-mktg-dev-gke-gcs-object-adm@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com	
sa-composer@its-managed-dbx-edlops-t.iam.gserviceaccount.com 	
sa-edi-data-upload-p@za-global-service-accounts-p.iam.gserviceaccount.com	
sa-glo-gke-dbx@its-managed-dbx-ds-01-d.iam.gserviceaccount.com	
sa-gke-dbx-goas-d@za-global-service-accounts-p.iam.gserviceaccount.com	 
sa-edi-data-upload-t@za-global-service-accounts-p.iam.gserviceaccount.com	
sa-rpa-dbx-glo-p@za-global-service-accounts-p.iam.gserviceaccount.com

# Marketing Service Accounts

sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com  
sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com  
sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com
gcds-its-zap-mktg-ds-analysts@zebra.com	
gcds-its-zap-mktg-ds-engineers@zebra.com	
gcds-its-zap-mktg-ds-scientists@zebra.com

************************************************************************************************************************/
### Bucket Name: its-managed-dbx-zap-d-logs
resource "google_storage_bucket_iam_member" "dev_logs_bucket_admin" {
  bucket = data.google_storage_bucket.dev_logs_bucket.name
  for_each = toset([
    "group:gcds-its-zap-de-ops@zebra.com",
    "serviceAccount:sa-composer@its-managed-dbx-edlops-t.iam.gserviceaccount.com",
    "serviceAccount:sa-gke-gcs-object-admin@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "group:gcds-its-zap-de-developers@zebra.com"
  ])
  role = "roles/storage.objectAdmin"
  member = each.value
}



### Bucket Name: its-managed-dbx-zap-d-delta-bs-eloqua
resource "google_storage_bucket_iam_member" "delta_bs_eloqua_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_eloqua.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
	"serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}

resource "google_storage_bucket_iam_member" "delta_bs_eloqua_bucket_read" {
  bucket = data.google_storage_bucket.delta_bs_eloqua.name
  role = "roles/storage.objectViewer"
  for_each = toset([
	"group:gcds-its-zap-mktg-ds-analysts@zebra.com",
	"group:gcds-its-zap-mktg-ds-engineers@zebra.com",
	"group:gcds-its-zap-mktg-ds-scientists@zebra.com",
	"serviceAccount:sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
	"serviceAccount:sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-delta-bs-dwa
resource "google_storage_bucket_iam_member" "delta_bs_dwa_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_dwa.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}

resource "google_storage_bucket_iam_member" "delta_bs_dwa_bucket_read" {
  bucket = data.google_storage_bucket.delta_bs_dwa.name
  role = "roles/storage.objectViewer"
  for_each = toset([
	"group:gcds-its-zap-mktg-ds-analysts@zebra.com",
	"group:gcds-its-zap-mktg-ds-engineers@zebra.com",
	"group:gcds-its-zap-mktg-ds-scientists@zebra.com",
	"serviceAccount:sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
	"serviceAccount:sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-delta-bs-demandbase
resource "google_storage_bucket_iam_member" "delta_bs_demandbase_admin" {
  bucket = data.google_storage_bucket.delta_bs_demandbase.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}

resource "google_storage_bucket_iam_member" "delta_bs_demandbase_read" {
  bucket = data.google_storage_bucket.delta_bs_demandbase.name
  role = "roles/storage.objectViewer"
  for_each = toset([
 	"group:gcds-its-zap-mktg-ds-analysts@zebra.com",
	"group:gcds-its-zap-mktg-ds-engineers@zebra.com",
	"group:gcds-its-zap-mktg-ds-scientists@zebra.com",
	"serviceAccount:sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
	"serviceAccount:sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-delta-bs-adobe
resource "google_storage_bucket_iam_member" "delta_bs_adobe_admin" {
  bucket = data.google_storage_bucket.delta_bs_adobe.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}

resource "google_storage_bucket_iam_member" "delta_bs_adobe_read" {
  bucket = data.google_storage_bucket.delta_bs_adobe.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "group:gcds-its-zap-mktg-ds-analysts@zebra.com",
	"group:gcds-its-zap-mktg-ds-engineers@zebra.com",
	"group:gcds-its-zap-mktg-ds-scientists@zebra.com",
	"serviceAccount:sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
	"serviceAccount:sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-delta-bs-ihs
resource "google_storage_bucket_iam_member" "binding_admin_delta_bs_ihs_admin" {
  bucket = data.google_storage_bucket.delta_bs_ihs.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
  ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "binding_admin_delta_bs_ihs_read" {
  bucket = data.google_storage_bucket.delta_bs_ihs.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "group:gcds-its-zap-mktg-ds-analysts@zebra.com",
	"group:gcds-its-zap-mktg-ds-engineers@zebra.com",
	"group:gcds-its-zap-mktg-ds-scientists@zebra.com",
	"serviceAccount:sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
	"serviceAccount:sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
  ])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-delta-bs-evergage
resource "google_storage_bucket_iam_member" "delta_bs_evergage_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_evergage.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
	"serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}

resource "google_storage_bucket_iam_member" "delta_bs_evergage_bucket_read" {
  bucket = data.google_storage_bucket.delta_bs_evergage.name
  role = "roles/storage.objectViewer"
  for_each = toset([
	"group:gcds-its-zap-mktg-ds-analysts@zebra.com",
	"group:gcds-its-zap-mktg-ds-engineers@zebra.com",
	"group:gcds-its-zap-mktg-ds-scientists@zebra.com",
	"serviceAccount:sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
	"serviceAccount:sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-delta-bs-m360
resource "google_storage_bucket_iam_member" "delta_bs_m360_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_m360.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}

resource "google_storage_bucket_iam_member" "delta_bs_m360_bucket_read" {
  bucket = data.google_storage_bucket.delta_bs_m360.name
  role = "roles/storage.objectViewer"
  for_each = toset([
	"group:gcds-its-zap-mktg-ds-analysts@zebra.com",
	"group:gcds-its-zap-mktg-ds-engineers@zebra.com",
	"group:gcds-its-zap-mktg-ds-scientists@zebra.com",
	"serviceAccount:sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
	"serviceAccount:sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-delta-bs-gst
resource "google_storage_bucket_iam_member" "delta_bs_gst_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_gst.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-fin-gke-dbx@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}

resource "google_storage_bucket_iam_member" "delta_bs_gst_bucket_read" {
  bucket = data.google_storage_bucket.delta_bs_gst.name
  role = "roles/storage.objectViewer"
  for_each = toset([
	"group:gcds-its-zap-mktg-ds-analysts@zebra.com",
	"group:gcds-its-zap-mktg-ds-engineers@zebra.com",
	"group:gcds-its-zap-mktg-ds-scientists@zebra.com",
	"serviceAccount:sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
	"serviceAccount:sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-delta-bs-qualtrics
resource "google_storage_bucket_iam_member" "delta_bs_qualtrics_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_qualtrics.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}

resource "google_storage_bucket_iam_member" "delta_bs_qualtrics_bucket_read" {
  bucket = data.google_storage_bucket.delta_bs_qualtrics.name
  role = "roles/storage.objectViewer"
  for_each = toset([
	"group:gcds-its-zap-mktg-ds-analysts@zebra.com",
	"group:gcds-its-zap-mktg-ds-engineers@zebra.com",
	"group:gcds-its-zap-mktg-ds-scientists@zebra.com",
	"serviceAccount:sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
	"serviceAccount:sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-delta-bs-vistex
resource "google_storage_bucket_iam_member" "delta_bs_vistex_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_vistex.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}

resource "google_storage_bucket_iam_member" "delta_bs_vistex_bucket_read" {
  bucket = data.google_storage_bucket.delta_bs_vistex.name
  role = "roles/storage.objectViewer"
  for_each = toset([
	"group:gcds-its-zap-mktg-ds-analysts@zebra.com",
	"group:gcds-its-zap-mktg-ds-engineers@zebra.com",
	"group:gcds-its-zap-mktg-ds-scientists@zebra.com",
	"serviceAccount:sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
	"serviceAccount:sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-delta-bs-turtl
resource "google_storage_bucket_iam_member" "delta_bs_turtl_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_turtl.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}

resource "google_storage_bucket_iam_member" "delta_bs_turtl_bucket_read" {
  bucket = data.google_storage_bucket.delta_bs_turtl.name
  role = "roles/storage.objectViewer"
  for_each = toset([
	"group:gcds-its-zap-mktg-ds-analysts@zebra.com",
	"group:gcds-its-zap-mktg-ds-engineers@zebra.com",
	"group:gcds-its-zap-mktg-ds-scientists@zebra.com",
	"serviceAccount:sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
	"serviceAccount:sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-delta-bs-sfdc
resource "google_storage_bucket_iam_member" "delta_bs_sfdc_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_sfdc.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}

resource "google_storage_bucket_iam_member" "delta_bs_sfdc_bucket_read" {
  bucket = data.google_storage_bucket.delta_bs_sfdc.name
  role = "roles/storage.objectViewer"
  for_each = toset([
	"group:gcds-its-zap-mktg-ds-analysts@zebra.com",
	"group:gcds-its-zap-mktg-ds-engineers@zebra.com",
	"group:gcds-its-zap-mktg-ds-scientists@zebra.com",
	"serviceAccount:sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
	"serviceAccount:sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-history-azure
resource "google_storage_bucket_iam_member" "history_azure_bucket_admin" {
  bucket = data.google_storage_bucket.history_azure.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}

resource "google_storage_bucket_iam_member" "history_azure_bucket_read" {
  bucket = data.google_storage_bucket.history_azure.name
  role = "roles/storage.objectViewer"
  for_each = toset([
	"group:gcds-its-zap-mktg-ds-analysts@zebra.com",
	"group:gcds-its-zap-mktg-ds-engineers@zebra.com",
	"group:gcds-its-zap-mktg-ds-scientists@zebra.com",
	"serviceAccount:sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
	"serviceAccount:sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-landing-ihs
resource "google_storage_bucket_iam_member" "binding_admin_landing_ihs_bucket" {
  bucket = data.google_storage_bucket.landing_ihs.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
  ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "binding_admin_landing_ihs_read" {
  bucket = data.google_storage_bucket.landing_ihs.name
  role = "roles/storage.objectViewer"
  for_each = toset([
	"group:gcds-its-zap-mktg-ds-analysts@zebra.com",
	"group:gcds-its-zap-mktg-ds-engineers@zebra.com",
	"group:gcds-its-zap-mktg-ds-scientists@zebra.com",
	"serviceAccount:sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
	"serviceAccount:sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
  ])
  member = each.value
}