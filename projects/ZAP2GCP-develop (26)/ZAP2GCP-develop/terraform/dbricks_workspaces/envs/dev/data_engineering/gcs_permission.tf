
/************************** GCS BUCKETS PERMISSIONS ********************************************************************

# DEV Environment :- its-managed-dbx-zap-d
# Permissions: 
      Manage  : "roles/storage.objectAdmin"
      Reader  : "roles/storage.objectViewer"
      Create  : "roles/storage.objectCreator" 

# Groups: 
gcds-its-managed-dbx-zap-d-cloud-functions-developer@zebra.com	
gcds-its-zap-de-ops@zebra.com	
gcds-its-zap-de-developers@zebra.com	
gcds-its-zap-glo-ds-developers@zebra.com	
gcds-its-zap-goas-ds-developers@zebra.com	
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
sa-edi-data-upload@its-managed-dbx-zap-d.iam.gserviceaccount.com	
sa-glo-gke-dbx@its-managed-dbx-ds-01-d.iam.gserviceaccount.com	
sa-goas-gke-dbx@its-managed-dbx-ds-01-d.iam.gserviceaccount.com	 
sa-edi-data-upload-t@za-global-service-accounts-p.iam.gserviceaccount.com	
sa-rpa-dbx-glo-p@za-global-service-accounts-p.iam.gserviceaccount.com

************************************************************************************************************************/
#New Service Accounts and Groups
/************************************************************************************************************************
Project: its-managed-dbx-zap-d

sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com 
sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com 

Project: its-managed-dbx-ds-01-d

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
### Bucket Name: azuretogcptest
resource "google_storage_bucket_iam_member" "azuretogcptest_bucket_admin" {
  bucket = data.google_storage_bucket.azuretogcptest.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-developers@zebra.com", 
    "group:gcds-its-zap-de-ops@zebra.com",
	  "serviceAccount:sa-gke-gcs-object-admin@its-managed-dbx-zap-d.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "azuretogcptest_bucket_reader" {
  bucket = data.google_storage_bucket.azuretogcptest.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "serviceAccount:sa-gke-gcs-object-reader@its-managed-dbx-zap-d.iam.gserviceaccount.com"
     ])
  member = each.value
}

### Bucket Name: databricks-1235921161438059
resource "google_storage_bucket_iam_member" "databricks_1235921161438059_bucket_admin" {
  bucket = data.google_storage_bucket.databricks_1235921161438059.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-developers@zebra.com", 
    "group:gcds-its-zap-de-ops@zebra.com",
	"serviceAccount:sa-gke-gcs-object-admin@its-managed-dbx-zap-d.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "databricks_1235921161438059_bucket_reader" {
  bucket = data.google_storage_bucket.databricks_1235921161438059.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "serviceAccount:sa-gke-gcs-object-reader@its-managed-dbx-zap-d.iam.gserviceaccount.com"
     ])
  member = each.value
}

### Bucket Name: databricks-1235921161438059-system
resource "google_storage_bucket_iam_member" "databricks_1235921161438059_system_admin" {
  bucket = data.google_storage_bucket.databricks_1235921161438059_system.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-developers@zebra.com", 
    "group:gcds-its-zap-de-ops@zebra.com",
	"serviceAccount:sa-gke-gcs-object-admin@its-managed-dbx-zap-d.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "databricks_1235921161438059_system_reader" {
  bucket = data.google_storage_bucket.databricks_1235921161438059_system.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "serviceAccount:sa-gke-gcs-object-reader@its-managed-dbx-zap-d.iam.gserviceaccount.com"
     ])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-delta-bs-adobe
resource "google_storage_bucket_iam_member" "delta_bs_adobe_admin" {
  bucket = data.google_storage_bucket.delta_bs_adobe.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_bs_adobe_reader" {
  bucket = data.google_storage_bucket.delta_bs_adobe.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "group:gcds-its-zap-mktg-ds-analysts@zebra.com",
    "group:gcds-its-zap-mktg-ds-engineers@zebra.com",
    "group:gcds-its-zap-mktg-ds-scientists@zebra.com",
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"   
     ])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-delta-bs-glo
resource "google_storage_bucket_iam_member" "delta_bs_glo_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_glo.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"

	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_bs_glo_bucket_reader" {
  bucket =  data.google_storage_bucket.delta_bs_glo.name
  role = "roles/storage.objectViewer"
  for_each = toset([
	"group:gcds-its-zap-de-admin@zebra.com",
  "group:gcds-its-zap-de-ops@zebra.com",
  "group:gcds-its-zap-de-developers@zebra.com",
  "group:gcds-its-zap-glo-engineers@zebra.com",
  "group:gcds-its-zap-glo-analysts@zebra.com",
  "group:gcds-its-zap-glo-scientists@zebra.com",
  "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-goassecfin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-goassecfin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-goassecfin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
  
     ])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-delta-bs-rma
resource "google_storage_bucket_iam_member" "delta_bs_rma_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_rma.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"

	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_bs_rma_bucket_reader" {
  bucket =  data.google_storage_bucket.delta_bs_rma.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "group:gcds-its-zap-goas-ds-sec-fin-engineers@zebra.com",
    "group:gcds-its-zap-goas-ds-sec-fin-scientists@zebra.com",
    "group:gcds-its-zap-goas-ds-sec-fin-analysts@zebra.com",
    "group:gcds-its-zap-goas-scientists@zebra.com",
    "group:gcds-its-zap-goas-enginners@zebra.com",
    "group:gcds-its-zap-goas-analysts@zebra.com",
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goassecfin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goassecfin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goassecfin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"

     ])
  member = each.value
}

/*****************************************************************************************************/

### Buckets Provisioned by Terraform
### Bucket Name: its-managed-dbx-zap-d-delta_bs_demandbase
resource "google_storage_bucket_iam_member" "delta_bs_demandbase_admin" {
  bucket = module.delta_bs_demandbase_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_bs_demandbase_read" {
  bucket = module.delta_bs_demandbase_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "group:gcds-its-zap-mktg-ds-analysts@zebra.com",
    "group:gcds-its-zap-mktg-ds-engineers@zebra.com",
    "group:gcds-its-zap-mktg-ds-scientists@zebra.com",
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com" 
     ])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-delta-bs-dwa
resource "google_storage_bucket_iam_member" "delta_bs_dwa_bucket_admin" {
  bucket = module.delta_bs_dwa_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"

	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_bs_dwa_bucket_reader" {
  bucket = module.delta_bs_dwa_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "group:gcds-its-zap-mktg-ds-analysts@zebra.com",
    "group:gcds-its-zap-mktg-ds-engineers@zebra.com",
    "group:gcds-its-zap-mktg-ds-scientists@zebra.com",
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"

     ])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-delta-bs-eloqua
resource "google_storage_bucket_iam_member" "delta_bs_eloqua_bucket_admin" {
  bucket = module.delta_bs_eloqua_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"

	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_bs_eloqua_bucket_reader" {
  bucket =  module.delta_bs_eloqua_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "group:gcds-its-zap-mktg-ds-analysts@zebra.com",
    "group:gcds-its-zap-mktg-ds-engineers@zebra.com",
    "group:gcds-its-zap-mktg-ds-scientists@zebra.com",
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
   
    ])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-delta-bs-eol 
resource "google_storage_bucket_iam_member" "delta_bs_eol_admin" {
  bucket = module.nc_dev_delta_eol_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"

	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_bs_eol_reader" {
  bucket = module.nc_dev_delta_eol_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "group:gcds-its-zap-goas-ds-sec-fin-engineers@zebra.com",
    "group:gcds-its-zap-goas-ds-sec-fin-scientists@zebra.com",
    "group:gcds-its-zap-goas-ds-sec-fin-analysts@zebra.com",
    "group:gcds-its-zap-goas-scientists@zebra.com",
    "group:gcds-its-zap-goas-enginners@zebra.com",
    "group:gcds-its-zap-goas-analysts@zebra.com",
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"

     ])
  member = each.value
}


### Bucket Name: its-managed-dbx-zap-d-delta-bs-evergage
resource "google_storage_bucket_iam_member" "delta_bs_evergage_bucket_admin" {
  bucket = module.delta_bs_evergage_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"

	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_bs_evergage_bucket_reader" {
  bucket =  module.delta_bs_evergage_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "group:gcds-its-zap-mktg-ds-analysts@zebra.com",
    "group:gcds-its-zap-mktg-ds-engineers@zebra.com",
    "group:gcds-its-zap-mktg-ds-scientists@zebra.com",
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
  
     ])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-delta-bs-grdf
resource "google_storage_bucket_iam_member" "delta_bs_grdf_bucket_admin" {
  bucket = module.delta_bs_grdf_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"

	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_bs_grdf_bucket_reader" {
  bucket =  module.delta_bs_grdf_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "group:gcds-its-zap-goas-ds-sec-fin-engineers@zebra.com",
    "group:gcds-its-zap-goas-ds-sec-fin-scientists@zebra.com",
    "group:gcds-its-zap-goas-ds-sec-fin-analysts@zebra.com",
    "group:gcds-its-zap-goas-scientists@zebra.com",
    "group:gcds-its-zap-goas-enginners@zebra.com",
    "group:gcds-its-zap-goas-analysts@zebra.com",
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goassecfin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goassecfin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goassecfin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"

     ])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-delta-bs-gst
resource "google_storage_bucket_iam_member" "delta_bs_gst_bucket_admin" {
  bucket = module.delta_bs_gst_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-fin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-sales-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"

	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_bs_gst_bucket_reader" {
  bucket =  module.delta_bs_gst_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "group:gcds-its-zap-goas-ds-sec-fin-engineers@zebra.com",
    "group:gcds-its-zap-goas-ds-sec-fin-scientists@zebra.com",
    "group:gcds-its-zap-goas-ds-sec-fin-analysts@zebra.com",
    "group:gcds-its-zap-mktg-ds-analysts@zebra.com",
    "group:gcds-its-zap-mktg-ds-engineers@zebra.com",
    "group:gcds-its-zap-mktg-ds-scientists@zebra.com",
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
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goassecfin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goassecfin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goassecfin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-fin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-fin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-sales-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-sales-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"

     ])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-delta-bs-m360
resource "google_storage_bucket_iam_member" "delta_bs_m360_bucket_admin" {
  bucket = module.delta_bs_m360_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"

	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_bs_m360_bucket_reader" {
  bucket =  module.delta_bs_m360_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "group:gcds-its-zap-mktg-ds-analysts@zebra.com",
    "group:gcds-its-zap-mktg-ds-engineers@zebra.com",
    "group:gcds-its-zap-mktg-ds-scientists@zebra.com",
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"

     ])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-delta-bs-planib
resource "google_storage_bucket_iam_member" "delta_bs_planib_bucket_admin" {
  bucket = module.nc_dev_delta_bs_planib_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"

	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_bs_planib_bucket_reader" {
  bucket =  module.nc_dev_delta_bs_planib_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "group:gcds-its-zap-goas-ds-sec-fin-engineers@zebra.com",
    "group:gcds-its-zap-goas-ds-sec-fin-scientists@zebra.com",
    "group:gcds-its-zap-goas-ds-sec-fin-analysts@zebra.com",
    "group:gcds-its-zap-goas-scientists@zebra.com",
    "group:gcds-its-zap-goas-enginners@zebra.com",
    "group:gcds-its-zap-goas-analysts@zebra.com",
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goassecfin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goassecfin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goassecfin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
  
     ])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-delta-bs-qualtrics
resource "google_storage_bucket_iam_member" "delta_bs_qualtrics_bucket_admin" {
  bucket = module.delta_bs_qualtrics_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"

	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_bs_qualtrics_bucket_reader" {
  bucket =  module.delta_bs_qualtrics_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
  "group:gcds-its-zap-de-admin@zebra.com",
  "group:gcds-its-zap-de-ops@zebra.com",
  "group:gcds-its-zap-de-developers@zebra.com",
  "group:gcds-its-zap-mktg-ds-analysts@zebra.com",
  "group:gcds-its-zap-mktg-ds-engineers@zebra.com",
  "group:gcds-its-zap-mktg-ds-scientists@zebra.com",
  "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
  "serviceAccount:sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
 
     ])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-delta-bs-sfdc
resource "google_storage_bucket_iam_member" "delta_bs_sfdc_bucket_admin" {
  bucket = module.nc_dev_delta_sfdc_bucket.name
  role = "roles/storage.objectAdmin"
    for_each = toset([
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-fin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-sales-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"

	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_bs_sfdc_bucket_reader" {
  bucket =  module.nc_dev_delta_sfdc_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "group:gcds-its-zap-goas-ds-sec-fin-engineers@zebra.com",
    "group:gcds-its-zap-goas-ds-sec-fin-scientists@zebra.com",
    "group:gcds-its-zap-goas-ds-sec-fin-analysts@zebra.com",
    "group:gcds-its-zap-mktg-ds-analysts@zebra.com",
    "group:gcds-its-zap-mktg-ds-engineers@zebra.com",
    "group:gcds-its-zap-mktg-ds-scientists@zebra.com",
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
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goassecfin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goassecfin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goassecfin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-fin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-fin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-sales-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-sales-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"

     ])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-delta-bs-turtl
resource "google_storage_bucket_iam_member" "delta_bs_turtl_bucket_admin" {
  bucket = module.delta_bs_turtl_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_bs_turtl_bucket_reader" {
  bucket =  module.delta_bs_turtl_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "group:gcds-its-zap-mktg-ds-analysts@zebra.com",
    "group:gcds-its-zap-mktg-ds-engineers@zebra.com",
    "group:gcds-its-zap-mktg-ds-scientists@zebra.com",
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
     ])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-delta-bs-vistex
resource "google_storage_bucket_iam_member" "delta_bs_vistex_bucket_admin" {
  bucket = module.delta_bs_vistex_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_bs_vistex_bucket_reader" {
  bucket =  module.delta_bs_vistex_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "group:gcds-its-zap-mktg-ds-analysts@zebra.com",
    "group:gcds-its-zap-mktg-ds-engineers@zebra.com",
    "group:gcds-its-zap-mktg-ds-scientists@zebra.com",
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"

     ])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-delta-gold-grdf
resource "google_storage_bucket_iam_member" "delta_gold_grdf_bucket_admin" {
  bucket = module.delta_gold_grdf_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_gold_grdf_bucket_reader" {
  bucket =  module.delta_gold_grdf_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "group:gcds-its-zap-goas-ds-sec-fin-engineers@zebra.com",
    "group:gcds-its-zap-goas-ds-sec-fin-scientists@zebra.com",
    "group:gcds-its-zap-goas-ds-sec-fin-analysts@zebra.com",
    "group:gcds-its-zap-goas-scientists@zebra.com",
    "group:gcds-its-zap-goas-enginners@zebra.com",
    "group:gcds-its-zap-goas-analysts@zebra.com",
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goassecfin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goassecfin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goassecfin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"

     ])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-history-azure
resource "google_storage_bucket_iam_member" "history_azure_bucket_admin" {
  bucket = data.google_storage_bucket.history_azure.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"

	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "history_azure_bucket_reader" {
  bucket = data.google_storage_bucket.history_azure.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "group:gcds-its-zap-mktg-ds-analysts@zebra.com",
    "group:gcds-its-zap-mktg-ds-engineers@zebra.com",
    "group:gcds-its-zap-mktg-ds-scientists@zebra.com",
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"

    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "history_azure_bucket_create" {
  bucket = data.google_storage_bucket.history_azure.name
  role = "roles/storage.objectCreator"
  for_each = toset([
	  	"serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}


### Bucket Name: its-managed-dbx-zap-d-landing-adobe
resource "google_storage_bucket_iam_member" "landing_adobe_bucket_admin" {
  bucket = data.google_storage_bucket.landing_adobe.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_adobe_bucket_reader" {
  bucket =  data.google_storage_bucket.landing_adobe.name
  role = "roles/storage.objectViewer"
  for_each = toset([
	"serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_adobe_bucket_create" {
  bucket = data.google_storage_bucket.landing_adobe.name
  role = "roles/storage.objectCreator"
  for_each = toset([
	"serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-landing-demandbase
resource "google_storage_bucket_iam_member" "landing_demandbase_bucket_admin" {
  bucket = module.landing_demandbase_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_demandbase_bucket_reader" {
  bucket =  module.landing_demandbase_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
	"serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_demandbase_bucket_create" {
  bucket = module.landing_demandbase_bucket.name
  role = "roles/storage.objectCreator"
  for_each = toset([
	"serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-landing-digst
resource "google_storage_bucket_iam_member" "landing_digst_bucket_admin" {
  bucket = data.google_storage_bucket.landing_digst.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_digst_bucket_reader" {
  bucket =  data.google_storage_bucket.landing_digst.name
  role = "roles/storage.objectViewer"
  for_each = toset([
	"serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_digst_bucket_create" {
  bucket = data.google_storage_bucket.landing_digst.name
  role = "roles/storage.objectCreator"
  for_each = toset([
	"serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-landing-disfdc
resource "google_storage_bucket_iam_member" "landing_disfdc_bucket_admin" {
  bucket = data.google_storage_bucket.landing_disfdc.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_disfdc_bucket_reader" {
  bucket =  data.google_storage_bucket.landing_disfdc.name
  role = "roles/storage.objectViewer"
  for_each = toset([
	"serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_disfdc_bucket_create" {
  bucket = data.google_storage_bucket.landing_disfdc.name
  role = "roles/storage.objectCreator"
  for_each = toset([
	"serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-landing-dsfdc
resource "google_storage_bucket_iam_member" "landing_dsfdc_bucket_admin" {
  bucket = data.google_storage_bucket.landing_dsfdc.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_dsfdc_bucket_reader" {
  bucket =  data.google_storage_bucket.landing_dsfdc.name
  role = "roles/storage.objectViewer"
  for_each = toset([

	"serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_dsfdc_bucket_create" {
  bucket = data.google_storage_bucket.landing_dsfdc.name
  role = "roles/storage.objectCreator"
  for_each = toset([
	"serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}


### Bucket Name: its-managed-dbx-zap-d-landing-dwa
resource "google_storage_bucket_iam_member" "landing_dwa_bucket_admin" {
  bucket = module.landing_dwa_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_dwa_bucket_reader" {
  bucket =  module.landing_dwa_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
	"serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_dwa_bucket_create" {
  bucket = module.landing_dwa_bucket.name
  role = "roles/storage.objectCreator"
  for_each = toset([
	"serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-landing-eloqua
resource "google_storage_bucket_iam_member" "landing_eloqua_bucket_admin" {
  bucket = module.landing_eloqua_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_eloqua_bucket_reader" {
  bucket =  module.landing_eloqua_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
	"serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_eloqua_bucket_create" {
  bucket = module.landing_eloqua_bucket.name
  role = "roles/storage.objectCreator"
  for_each = toset([

	"serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-landing-eol
resource "google_storage_bucket_iam_member" "landing_eol_bucket_admin" {
  bucket = module.nc_dev_landing_eol_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_eol_bucket_reader" {
  bucket =  module.nc_dev_landing_eol_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
	"serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_eol_bucket_create" {
  bucket = module.nc_dev_landing_eol_bucket.name
  role = "roles/storage.objectCreator"
  for_each = toset([
	"serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-landing-evergage
resource "google_storage_bucket_iam_member" "landing_evergage_bucket_admin" {
  bucket = module.landing_evergage_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_evergage_bucket_reader" {
  bucket =  module.landing_evergage_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([

	"serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_evergage_bucket_create" {
  bucket = module.landing_evergage_bucket.name
  role = "roles/storage.objectCreator"
  for_each = toset([
	"serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-landing-glo
resource "google_storage_bucket_iam_member" "landing_glo_bucket_admin" {
  bucket = data.google_storage_bucket.landing_glo.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_glo_bucket_reader" {
  bucket =  data.google_storage_bucket.landing_glo.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "group:gcds-its-zap-glo-engineers@zebra.com",
    "group:gcds-its-zap-glo-analysts@zebra.com",
    "group:gcds-its-zap-glo-scientists@zebra.com",
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-glo-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-glo-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-glo-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"

    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_glo_bucket_create" {
  bucket = data.google_storage_bucket.landing_glo.name
  role = "roles/storage.objectCreator"
  for_each = toset([
	"serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-rpa-dbx-glo-p@za-global-service-accounts-p.iam.gserviceaccount.com"

	])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-landing-grdf
resource "google_storage_bucket_iam_member" "landing_grdf_bucket_admin" {
  bucket = module.landing_grdf_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "group:gcds-its-zap-edi-ops@zebra.com",
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_grdf_bucket_reader" {
  bucket =  module.landing_grdf_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
	"serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_grdf_bucket_create" {
  bucket = module.landing_grdf_bucket.name
  role = "roles/storage.objectCreator"
  for_each = toset([
    "serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-edi-data-upload-t@za-global-service-accounts-p.iam.gserviceaccount.com",
    "serviceAccount:sa-edi-data-upload-p@za-global-service-accounts-p.iam.gserviceaccount.com"

  	])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-landing-gst
resource "google_storage_bucket_iam_member" "landing_gst_bucket_admin" {
  bucket = data.google_storage_bucket.landing_gst.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_gst_bucket_reader" {
  bucket =  data.google_storage_bucket.landing_gst.name
  role = "roles/storage.objectViewer"
  for_each = toset([
	"serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_gst_bucket_create" {
  bucket = data.google_storage_bucket.landing_gst.name
  role = "roles/storage.objectCreator"
  for_each = toset([
	"serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}


### Bucket Name: its-managed-dbx-zap-d-landing-m360
resource "google_storage_bucket_iam_member" "landing_m360_bucket_admin" {
  bucket = module.landing_m360_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_m360_bucket_reader" {
  bucket =  module.landing_m360_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_m360_bucket_create" {
  bucket = module.landing_m360_bucket.name
  role = "roles/storage.objectCreator"
  for_each = toset([
	    "serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}


### Bucket Name: its-managed-dbx-zap-d-landing-planib
resource "google_storage_bucket_iam_member" "landing_planib_bucket_admin" {
  bucket = module.nc_dev_landing_planib_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_planib_bucket_reader" {
  bucket =  module.nc_dev_landing_planib_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_planib_bucket_create" {
  bucket = module.nc_dev_landing_planib_bucket.name
  role = "roles/storage.objectCreator"
  for_each = toset([
	"serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-landing-qualtrics
resource "google_storage_bucket_iam_member" "landing_qualtrics_bucket_admin" {
  bucket = module.landing_qualtrics_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_qualtrics_bucket_reader" {
  bucket =  module.landing_qualtrics_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"

    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_qualtrics_bucket_create" {
  bucket = module.landing_qualtrics_bucket.name
  role = "roles/storage.objectCreator"
  for_each = toset([
	"serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-landing-rma
resource "google_storage_bucket_iam_member" "landing_rma_bucket_admin" {
  bucket = data.google_storage_bucket.landing_rma.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"

	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_rma_bucket_reader" {
  bucket =  data.google_storage_bucket.landing_rma.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"

    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_rma_bucket_create" {
  bucket = data.google_storage_bucket.landing_rma.name
  role = "roles/storage.objectCreator"
  for_each = toset([
	  "serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-landing-sfdc
resource "google_storage_bucket_iam_member" "landing_sfdc_bucket_admin" {
  bucket = data.google_storage_bucket.landing_sfdc.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_sfdc_bucket_reader" {
  bucket =  data.google_storage_bucket.landing_sfdc.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_sfdc_bucket_create" {
  bucket = data.google_storage_bucket.landing_sfdc.name
  role = "roles/storage.objectCreator"
  for_each = toset([
	  "serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-zap-d.iam.gserviceaccount.com"

	])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-landing-turtl
resource "google_storage_bucket_iam_member" "landing_turtl_bucket_admin" {
  bucket = module.landing_turtl_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"

	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_turtl_bucket_reader" {
  bucket =  module.landing_turtl_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_turtl_bucket_create" {
  bucket = module.landing_turtl_bucket.name
  role = "roles/storage.objectCreator"
  for_each = toset([
	   "serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-landing-vistex
resource "google_storage_bucket_iam_member" "landing_vistex_bucket_admin" {
  bucket = module.landing_vistex_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"

	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_vistex_bucket_reader" {
  bucket =  module.landing_vistex_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_vistex_bucket_create" {
  bucket = module.landing_vistex_bucket.name
  role = "roles/storage.objectCreator"
  for_each = toset([
	  "serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-pipeline-code
resource "google_storage_bucket_iam_member" "pipeline_code_bucket_admin" {
  bucket = module.dev_pipeline_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com" 
	])
  member = each.value
}
# resource "google_storage_bucket_iam_member" "pipeline_code_bucket_reader" {
#   bucket =  module.dev_pipeline_bucket.name
#   role = "roles/storage.objectViewer"
#   for_each = toset([
#     "serviceAccount:sa-gke-dbx-glo-d@za-global-service-accounts-p.iam.gserviceaccount.com",
#     "serviceAccount:sa-gke-dbx-goas-d@za-global-service-accounts-p.iam.gserviceaccount.com",
#     "serviceAccount:sa-gke-gcs-object-admin@its-managed-dbx-zap-d.iam.gserviceaccount.com",
#"serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
#     "serviceAccount:sa-gke-gcs-object-reader@its-managed-dbx-zap-d.iam.gserviceaccount.com",
#     "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"    
#     ])
# }


### Bucket Name: test_read
resource "google_storage_bucket_iam_member" "test_read_bucket_admin" {
  bucket = data.google_storage_bucket.test_read.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-developers@zebra.com",                   
    "group:gcds-its-zap-de-ops@zebra.com",
    "serviceAccount:sa-gke-gcs-object-admin@its-managed-dbx-zap-d.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	  
	])
  member = each.value
}
resource "google_storage_bucket_iam_member" "test_read_bucket_reader" {
  bucket =  data.google_storage_bucket.test_read.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "serviceAccount:sa-gke-gcs-object-reader@its-managed-dbx-zap-d.iam.gserviceaccount.com"
    ])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-landing-goas-user-data
resource "google_storage_bucket_iam_member" "landing_goas_user_data_bucket_admin" {
  bucket = module.landing_goas_user_data_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
  	])
  member = each.value
}

resource "google_storage_bucket_iam_member" "landing_goas_user_data_bucket_reader" {
  bucket = module.landing_goas_user_data_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
	"serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
  	])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-delta-bs-goas
resource "google_storage_bucket_iam_member" "delta_bs_goas_bucket_admin" {
  bucket = module.delta_bs_goas_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"

	])
  member = each.value
}

resource "google_storage_bucket_iam_member" "delta_bs_goas_bucket_reader" {
  bucket = module.delta_bs_goas_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "group:gcds-its-zap-goas-ds-sec-fin-engineers@zebra.com",
    "group:gcds-its-zap-goas-ds-sec-fin-scientists@zebra.com",
    "group:gcds-its-zap-goas-ds-sec-fin-analysts@zebra.com",
    "group:gcds-its-zap-goas-scientists@zebra.com",
    "group:gcds-its-zap-goas-enginners@zebra.com",
    "group:gcds-its-zap-goas-analysts@zebra.com",
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goassecfin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goassecfin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goassecfin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
	])
  member = each.value
}


### Bucket Name: its-managed-dbx-zap-d-delta-bs-landing-finance
resource "google_storage_bucket_iam_member" "landing_finance_bucket_admin" {
  bucket = module.landing_finance_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"

  ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_finance_bucket_reader" {
  bucket = module.landing_finance_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"

  ])
  member = each.value
}


### Bucket Name: its-managed-dbx-zap-d-delta-bs-finance
resource "google_storage_bucket_iam_member" "binding_admin_delta_bs_finance_bucket" {
  bucket = module.delta_bs_finance_bucket1.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-fin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"

  ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "binding_viewer_delta_bs_finance_bucket" {
  bucket = module.delta_bs_finance_bucket1.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "group:gcds-its-zap-fin-scientists@zebra.com",
    "group:gcds-its-zap-fin-enginners@zebra.com",
    "group:gcds-its-zap-fin-analysts@zebra.com",
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-fin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-fin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"

  ])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-delta-gold-finance
resource "google_storage_bucket_iam_member" "binding_admin_delta_gold_finance_bucket" {
  bucket = module.delta_gold_finance_bucket1.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
  ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "binding_viewer_delta_gold_finance_bucket" {
  bucket = module.delta_gold_finance_bucket1.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"

  ])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-delta-bs-ihs
resource "google_storage_bucket_iam_member" "binding_admin_delta_bs_ihs_bucket" {
  bucket = module.delta_bs_ihs_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "serviceAccount:sa-gke-gcs-object-admin@its-managed-dbx-zap-d.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
  ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "binding_viewer_delta_bs_ihs_bucket" {
  bucket = module.delta_bs_ihs_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "group:gcds-its-zap-goas-ds-sec-fin-engineers@zebra.com",
    "group:gcds-its-zap-goas-ds-sec-fin-scientists@zebra.com",
    "group:gcds-its-zap-goas-ds-sec-fin-analysts@zebra.com",
    "group:gcds-its-zap-mktg-ds-analysts@zebra.com",
    "group:gcds-its-zap-mktg-ds-engineers@zebra.com",
    "group:gcds-its-zap-mktg-ds-scientists@zebra.com",
    "group:gcds-its-zap-goas-scientists@zebra.com",
    "group:gcds-its-zap-goas-enginners@zebra.com",	
    "group:gcds-its-zap-goas-analysts@zebra.com",
    "group:gcds-its-zap-fin-scientists@zebra.com",
    "group:gcds-its-zap-fin-enginners@zebra.com",
    "group:gcds-its-zap-fin-analysts@zebra.com",
    "group:gcds-its-zap-sales-scientists@zebra.com",
    "group:gcds-its-zap-sales-enginners@zebra.com",
    "group:gcds-its-zap-sales-analysts@zebra.com",
    "serviceAccount:sa-dbx-goassecfin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goassecfin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goassecfin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",  
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",  
    "serviceAccount:sa-dbx-fin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-fin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-fin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-sales-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-sales-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",  
    "serviceAccount:sa-dbx-sales-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",   
    "serviceAccount:sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",  
    "serviceAccount:sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"   
  ])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-landing-ihs
resource "google_storage_bucket_iam_member" "binding_admin_landing_ihs_bucket" {
  bucket = module.landing_ihs_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-de-ops@zebra.com",
    "group:gcds-its-zap-de-developers@zebra.com",
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-gke-gcs-object-admin@its-managed-dbx-zap-d.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
  ])
  member = each.value
}

resource "google_storage_bucket_iam_member" "binding_viewer_landing_ihs_bucket" {
  bucket = module.landing_ihs_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-ds-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",  
    "serviceAccount:sa-dbx-mktg-da-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com"
  ])
  member = each.value
}

    
### Bucket Name: its-managed-dbx-zap-d-landing-erp
resource "google_storage_bucket_iam_member" "landing_erp_bucket_admin" {
  bucket = data.google_storage_bucket.landing_erp.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-developers@zebra.com", 
    "group:gcds-its-zap-de-ops@zebra.com",
	  "serviceAccount:sa-gke-gcs-object-admin@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-zap-d-delta-bs-erp
resource "google_storage_bucket_iam_member" "delta_bs_erp_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_erp.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-developers@zebra.com", 
    "group:gcds-its-zap-de-ops@zebra.com",
	  "serviceAccount:sa-gke-gcs-object-admin@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-zap-d.iam.gserviceaccount.com"
	])
  member = each.value
}