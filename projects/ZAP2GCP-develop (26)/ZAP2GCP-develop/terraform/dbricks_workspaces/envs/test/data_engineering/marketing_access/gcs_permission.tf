/************************** GCS BUCKETS PERMISSIONS ********************************************************************

# DEV Environment :- its-managed-dbx-de-01-t
# Permissions: 
      Manage  : "roles/storage.objectAdmin"
      Reader  : "roles/storage.objectViewer"
      Create  : "roles/storage.objectCreator" 

# Marketing Service Accounts

sa-dbx-mktg-de-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com  
sa-dbx-mktg-ds-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com  
sa-dbx-mktg-da-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com
gcds-its-zap-mktg-ds-analysts@zebra.com	
gcds-its-zap-mktg-ds-engineers@zebra.com	
gcds-its-zap-mktg-ds-scientists@zebra.com

************************************************************************************************************************/
### Bucket Name: its-managed-dbx-de-01-t-delta-bs-eloqua
resource "google_storage_bucket_iam_member" "delta_bs_eloqua_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_eloqua.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
	"serviceAccount:sa-dbx-mktg-de-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com"
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
	"serviceAccount:sa-dbx-mktg-ds-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
	"serviceAccount:sa-dbx-mktg-da-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-delta-bs-dwa
resource "google_storage_bucket_iam_member" "delta_bs_dwa_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_dwa.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-mktg-de-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com"
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
	"serviceAccount:sa-dbx-mktg-ds-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
	"serviceAccount:sa-dbx-mktg-da-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-delta-bs-demandbase
resource "google_storage_bucket_iam_member" "delta_bs_demandbase_admin" {
  bucket = data.google_storage_bucket.delta_bs_demandbase.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-mktg-de-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com"
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
	"serviceAccount:sa-dbx-mktg-ds-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
	"serviceAccount:sa-dbx-mktg-da-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-delta-bs-adobe
resource "google_storage_bucket_iam_member" "delta_bs_adobe_admin" {
  bucket = data.google_storage_bucket.delta_bs_adobe.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-mktg-de-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com"
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
	"serviceAccount:sa-dbx-mktg-ds-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
	"serviceAccount:sa-dbx-mktg-da-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-delta-bs-ihs
resource "google_storage_bucket_iam_member" "binding_admin_delta_bs_ihs_admin" {
  bucket = data.google_storage_bucket.delta_bs_ihs.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-mktg-de-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com"
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
	"serviceAccount:sa-dbx-mktg-ds-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
	"serviceAccount:sa-dbx-mktg-da-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
  "group:gcds-its-zap-fin-analysts@zebra.com",
  "group:gcds-its-zap-fin-enginners@zebra.com",
  "group:gcds-its-zap-fin-scientists@zebra.com",
  "group:gcds-its-zap-goas-analysts@zebra.com",
  "group:gcds-its-zap-goas-ds-sec-fin-analysts@zebra.com",
  "group:gcds-its-zap-goas-ds-sec-fin-engineers@zebra.com",
  "group:gcds-its-zap-goas-ds-sec-fin-scientists@zebra.com",
  "group:gcds-its-zap-goas-enginners@zebra.com",
  "group:gcds-its-zap-goas-scientists@zebra.com",
  "serviceAccount:sa-dbx-fin-da-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-fin-de-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-fin-ds-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-goas-da-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-goas-de-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-goas-ds-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-goassecfin-da-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-goassecfin-de-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-goassecfin-ds-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"
  ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-delta-bs-evergage
resource "google_storage_bucket_iam_member" "delta_bs_evergage_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_evergage.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
	"serviceAccount:sa-dbx-mktg-de-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com"
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
	"serviceAccount:sa-dbx-mktg-ds-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
	"serviceAccount:sa-dbx-mktg-da-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-delta-bs-m360
resource "google_storage_bucket_iam_member" "delta_bs_m360_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_m360.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-mktg-de-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com"
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
	"serviceAccount:sa-dbx-mktg-ds-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
	"serviceAccount:sa-dbx-mktg-da-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-delta-bs-gst
resource "google_storage_bucket_iam_member" "delta_bs_gst_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_gst.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-mktg-de-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com"
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
	"serviceAccount:sa-dbx-mktg-ds-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
	"serviceAccount:sa-dbx-mktg-da-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
  "group:gcds-its-zap-fin-analysts@zebra.com",
  "group:gcds-its-zap-fin-enginners@zebra.com",
  "group:gcds-its-zap-fin-scientists@zebra.com",
  "group:gcds-its-zap-goas-analysts@zebra.com",
  "group:gcds-its-zap-goas-ds-sec-fin-analysts@zebra.com",
  "group:gcds-its-zap-goas-ds-sec-fin-engineers@zebra.com",
  "group:gcds-its-zap-goas-ds-sec-fin-scientists@zebra.com",
  "group:gcds-its-zap-goas-enginners@zebra.com",
  "group:gcds-its-zap-goas-scientists@zebra.com",
  "serviceAccount:sa-dbx-fin-da-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-fin-de-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-fin-ds-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-goas-da-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-goas-de-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-goas-ds-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-goassecfin-da-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-goassecfin-de-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-goassecfin-ds-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-delta-bs-qualtrics
resource "google_storage_bucket_iam_member" "delta_bs_qualtrics_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_qualtrics.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-mktg-de-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com"
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
	"serviceAccount:sa-dbx-mktg-ds-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
	"serviceAccount:sa-dbx-mktg-da-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-delta-bs-vistex
resource "google_storage_bucket_iam_member" "delta_bs_vistex_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_vistex.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-mktg-de-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com"
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
	"serviceAccount:sa-dbx-mktg-ds-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
	"serviceAccount:sa-dbx-mktg-da-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-delta-bs-turtl
resource "google_storage_bucket_iam_member" "delta_bs_turtl_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_turtl.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-mktg-de-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com"
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
	"serviceAccount:sa-dbx-mktg-ds-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
	"serviceAccount:sa-dbx-mktg-da-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-delta-bs-sfdc
resource "google_storage_bucket_iam_member" "delta_bs_sfdc_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_sfdc.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-mktg-de-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com"
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
	"serviceAccount:sa-dbx-mktg-ds-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
	"serviceAccount:sa-dbx-mktg-da-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
  "group:gcds-its-zap-fin-analysts@zebra.com",
  "group:gcds-its-zap-fin-enginners@zebra.com",
  "group:gcds-its-zap-fin-scientists@zebra.com",
  "group:gcds-its-zap-goas-analysts@zebra.com",
  "group:gcds-its-zap-goas-ds-sec-fin-analysts@zebra.com",
  "group:gcds-its-zap-goas-ds-sec-fin-engineers@zebra.com",
  "group:gcds-its-zap-goas-ds-sec-fin-scientists@zebra.com",
  "group:gcds-its-zap-goas-enginners@zebra.com",
  "group:gcds-its-zap-goas-scientists@zebra.com",
  "serviceAccount:sa-dbx-fin-da-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-fin-de-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-fin-ds-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-goas-da-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-goas-de-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-goas-ds-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-goassecfin-da-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-goassecfin-de-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-goassecfin-ds-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-landing-ihs
resource "google_storage_bucket_iam_member" "binding_admin_landing_ihs_bucket" {
  bucket = data.google_storage_bucket.landing_ihs.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-mktg-de-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com"
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
	"serviceAccount:sa-dbx-mktg-ds-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
	"serviceAccount:sa-dbx-mktg-da-t@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
  "group:gcds-its-zap-fin-analysts@zebra.com",
  "group:gcds-its-zap-fin-enginners@zebra.com",
  "group:gcds-its-zap-fin-scientists@zebra.com",
  "group:gcds-its-zap-goas-analysts@zebra.com",
  "group:gcds-its-zap-goas-ds-sec-fin-analysts@zebra.com",
  "group:gcds-its-zap-goas-ds-sec-fin-engineers@zebra.com",
  "group:gcds-its-zap-goas-ds-sec-fin-scientists@zebra.com",
  "group:gcds-its-zap-goas-enginners@zebra.com",
  "group:gcds-its-zap-goas-scientists@zebra.com",
  "serviceAccount:sa-dbx-fin-da-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-fin-de-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-fin-ds-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-goas-da-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-goas-de-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-goas-ds-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-goassecfin-da-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-goassecfin-de-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-goassecfin-ds-t@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"
  ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-logs
resource "google_storage_bucket_iam_member" "test_logs_bucket_admin" {
  bucket = data.google_storage_bucket.test_logs_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
	"group:gcds-its-zap-de-ops@zebra.com",
  "serviceAccount:sa-composer-prod@its-managed-dbx-edlops-p.iam.gserviceaccount.com",
  "serviceAccount:sa-composer@its-managed-dbx-edlops-t.iam.gserviceaccount.com",
  "serviceAccount:sa-prod-gke-gcs-object-admin@its-managed-dbx-de-01-p.iam.gserviceaccount.com",
  "group:gcds-its-zap-de-developers@zebra.com"
	])
  member = each.value
}