
/************************** GCS BUCKETS PERMISSIONS ********************************************************************

# DEV Environment :- its-managed-dbx-de-01-t
# Permissions: 
    Manage  : "roles/storage.objectAdmin"
    Reader  : "roles/storage.objectViewer"
    Create  : "roles/storage.objectCreator" 

# Groups: 
group:gcds-its-zap-de-ops@zebra.com	
group:gcds-its-zap-de-developers@zebra.com	
group:gcds-its-zap-glo-ds-developers@zebra.com

## Service Accounts:
serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com	
serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com	
serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-de-01-t.iam.gserviceaccount.com	
serviceAccount:sa-mktg-t-gke-gcs-object-adm@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com	
serviceAccount:sa-composer@its-managed-dbx-edlops-t.iam.gserviceaccount.com 	
serviceAccount:sa-edi-data-upload@its-managed-dbx-de-01-t.iam.gserviceaccount.com	
serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com	
serviceAccount:sa-rpa-dbx-glo-p@za-global-service-accounts-p.iam.gserviceaccount.com

************************************************************************************************************************/

### Bucket Name: databricks-188879976212547
resource "google_storage_bucket_iam_member" "databricks_188879976212547_bucket_admin" {
  bucket = data.google_storage_bucket.databricks_188879976212547.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "databricks_188879976212547_bucket_reader" {
  bucket = data.google_storage_bucket.databricks_188879976212547.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}

### Bucket Name: databricks-188879976212547-system
resource "google_storage_bucket_iam_member" "databricks_188879976212547_system_bucket_admin" {
  bucket = data.google_storage_bucket.databricks_188879976212547_system.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "databricks_188879976212547_system_bucket_reader" {
  bucket = data.google_storage_bucket.databricks_188879976212547_system.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}


### Bucket Name: its-managed-dbx-de-01-t-delta-bs-adobe
resource "google_storage_bucket_iam_member" "delta_bs_adobe_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_adobe.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_bs_adobe_bucket_reader" {
  bucket = data.google_storage_bucket.delta_bs_adobe.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-mktg-t-gke-gcs-object-adm@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-delta-bs-demandbase
resource "google_storage_bucket_iam_member" "delta_bs_demandbase_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_demandbase.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_bs_demandbase_bucket_reader" {
  bucket = data.google_storage_bucket.delta_bs_demandbase.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-mktg-t-gke-gcs-object-adm@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-delta-bs-dwa 
resource "google_storage_bucket_iam_member" "delta_bs_dwa_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_dwa.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_bs_dwa_bucket_reader" {
  bucket = data.google_storage_bucket.delta_bs_dwa.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-mktg-t-gke-gcs-object-adm@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-delta-bs-eloqua
resource "google_storage_bucket_iam_member" "delta_bs_eloqua_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_eloqua.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_bs_eloqua_bucket_reader" {
  bucket = data.google_storage_bucket.delta_bs_eloqua.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-mktg-t-gke-gcs-object-adm@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-delta-bs-eol
resource "google_storage_bucket_iam_member" "delta_bs_eol_bucket_admin" {
  bucket = module.test_delta_eol_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_bs_eol_bucket_reader" {
  bucket = module.test_delta_eol_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-mktg-t-gke-gcs-object-adm@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-delta-bs-everage
resource "google_storage_bucket_iam_member" "delta_bs_everage_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_everage.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_bs_everage_bucket_reader" {
  bucket = data.google_storage_bucket.delta_bs_everage.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-mktg-t-gke-gcs-object-adm@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-delta-bs-evergage
resource "google_storage_bucket_iam_member" "delta_bs_evergage_bucket_admin" {
  bucket = module.test_delta_bs_evergage_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_bs_evergage_bucket_reader" {
  bucket = module.test_delta_bs_evergage_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-mktg-t-gke-gcs-object-adm@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-delta-bs-grdf
resource "google_storage_bucket_iam_member" "delta_bs_grdf_bucket_admin" {
  bucket = module.delta_bs_grdf_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_bs_grdf_bucket_reader" {
  bucket = module.delta_bs_grdf_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-mktg-t-gke-gcs-object-adm@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-delta-bs-gst
resource "google_storage_bucket_iam_member" "delta_bs_gst_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_gst.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_bs_gst_bucket_reader" {
  bucket = data.google_storage_bucket.delta_bs_gst.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-mktg-t-gke-gcs-object-adm@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-fin-gke-dbx@its-managed-dbx-ds-01-p.iam.gserviceaccount.com",
      "serviceAccount:sa-fin-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-delta-bs-m360
resource "google_storage_bucket_iam_member" "delta_bs_m360_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_m360.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_bs_m360_bucket_reader" {
  bucket = data.google_storage_bucket.delta_bs_m360.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-mktg-t-gke-gcs-object-adm@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-delta-bs-planib
resource "google_storage_bucket_iam_member" "delta_bs_planib_bucket_admin" {
  bucket = module.test_delta_bs_planib_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_bs_planib_bucket_reader" {
  bucket = module.test_delta_bs_planib_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-mktg-t-gke-gcs-object-adm@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-delta-bs-qualtrics
resource "google_storage_bucket_iam_member" "delta_bs_qualtrics_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_qualtrics.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_bs_qualtrics_bucket_reader" {
  bucket = data.google_storage_bucket.delta_bs_qualtrics.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-mktg-t-gke-gcs-object-adm@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-delta-bs-sfdc
resource "google_storage_bucket_iam_member" "delta_bs_sfdc_bucket_admin" {
  bucket = module.test_delta_sfdc_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_bs_sfdc_bucket_reader" {
  bucket = module.test_delta_sfdc_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-mktg-t-gke-gcs-object-adm@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-fin-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-gke-gcs-ds-object-admin@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-delta-bs-turtl
resource "google_storage_bucket_iam_member" "delta_bs_turtl_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_turtl.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_bs_turtl_bucket_reader" {
  bucket = data.google_storage_bucket.delta_bs_turtl.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-mktg-t-gke-gcs-object-adm@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-delta-bs-vistex
resource "google_storage_bucket_iam_member" "delta_bs_vistex_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_vistex.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_bs_vistex_bucket_reader" {
  bucket = data.google_storage_bucket.delta_bs_vistex.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-mktg-t-gke-gcs-object-adm@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-delta-gold-grdf
resource "google_storage_bucket_iam_member" "delta_gold_grdf_bucket_admin" {
  bucket = module.delta_gold_grdf_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "delta_gold_grdf_bucket_reader" {
  bucket = module.delta_gold_grdf_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-mktg-t-gke-gcs-object-adm@its-managed-dbx-mktg-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-landing-adobe
resource "google_storage_bucket_iam_member" "landing_adobe_bucket_admin" {
  bucket = data.google_storage_bucket.landing_adobe.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_adobe_bucket_reader" {
  bucket = data.google_storage_bucket.landing_adobe.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_adobe_bucket_creator" {
  bucket = data.google_storage_bucket.landing_adobe.name
  role = "roles/storage.objectCreator"
  for_each = toset([
      "serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-landing-demandbase
resource "google_storage_bucket_iam_member" "landing_demandbase_bucket_admin" {
  bucket = data.google_storage_bucket.landing_demandbase.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
      "serviceAccount:project-308796510349@storage-transfer-service.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_demandbase_bucket_reader" {
  bucket = data.google_storage_bucket.landing_demandbase.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_demandbase_bucket_creator" {
  bucket = data.google_storage_bucket.landing_demandbase.name
  role = "roles/storage.objectCreator"
  for_each = toset([
      "serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-landing-dwa
resource "google_storage_bucket_iam_member" "landing_dwa_bucket_admin" {
  bucket = data.google_storage_bucket.landing_dwa.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-prod-gke-gcs-object-admin@its-managed-dbx-de-01-p.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_dwa_bucket_reader" {
  bucket = data.google_storage_bucket.landing_dwa.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_dwa_bucket_creator" {
  bucket = data.google_storage_bucket.landing_dwa.name
  role = "roles/storage.objectCreator"
  for_each = toset([
      "serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-landing-eloqua
resource "google_storage_bucket_iam_member" "landing_eloqua_bucket_admin" {
  bucket = data.google_storage_bucket.landing_eloqua.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_eloqua_bucket_reader" {
  bucket = data.google_storage_bucket.landing_eloqua.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_eloqua_bucket_creator" {
  bucket = data.google_storage_bucket.landing_eloqua.name
  role = "roles/storage.objectCreator"
  for_each = toset([
      "serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-landing-eol
resource "google_storage_bucket_iam_member" "landing_eol_bucket_admin" {
  bucket = module.test_landing_eol_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_eol_bucket_reader" {
  bucket = module.test_landing_eol_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_eol_bucket_creator" {
  bucket = module.test_landing_eol_bucket.name
  role = "roles/storage.objectCreator"
  for_each = toset([
      "serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-landing-everage
resource "google_storage_bucket_iam_member" "landing_everage_bucket_admin" {
  bucket = data.google_storage_bucket.landing_everage.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_everage_bucket_reader" {
  bucket = data.google_storage_bucket.landing_everage.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_everage_bucket_creator" {
  bucket = data.google_storage_bucket.landing_everage.name
  role = "roles/storage.objectCreator"
  for_each = toset([
      "serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-landing-evergage
resource "google_storage_bucket_iam_member" "landing_evergage_bucket_admin" {
  bucket = module.test_landing_evergage_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_evergage_bucket_reader" {
  bucket = module.test_landing_evergage_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_evergage_bucket_creator" {
  bucket = module.test_landing_evergage_bucket.name
  role = "roles/storage.objectCreator"
  for_each = toset([
      "serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-landing-glo
resource "google_storage_bucket_iam_member" "landing_glo_bucket_admin" {
  bucket = data.google_storage_bucket.landing_glo.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "group:gcds-its-zap-glo-ds-developers@zebra.com",
      "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_glo_bucket_reader" {
  bucket = data.google_storage_bucket.landing_glo.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_glo_bucket_creator" {
  bucket = data.google_storage_bucket.landing_glo.name
  role = "roles/storage.objectCreator"
  for_each = toset([
      "serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-rpa-dbx-glo-p@za-global-service-accounts-p.iam.gserviceaccount.com"
    ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-landing-grdf
resource "google_storage_bucket_iam_member" "landing_grdf_bucket_admin" {
  bucket = module.landing_grdf_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_grdf_bucket_reader" {
  bucket = module.landing_grdf_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "group:gcds-its-zap-edi-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-composer@its-managed-dbx-edlops-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_grdf_bucket_creator" {
  bucket = module.landing_grdf_bucket.name
  role = "roles/storage.objectCreator"
  for_each = toset([
      "serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-edi-data-upload-t@za-global-service-accounts-p.iam.gserviceaccount.com"
    ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-landing-gst
resource "google_storage_bucket_iam_member" "landing_gst_bucket_admin" {
  bucket = data.google_storage_bucket.landing_gst.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_gst_bucket_reader" {
  bucket = data.google_storage_bucket.landing_gst.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_gst_bucket_creator" {
  bucket = data.google_storage_bucket.landing_gst.name
  role = "roles/storage.objectCreator"
  for_each = toset([
      "serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
      ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-landing-m360
resource "google_storage_bucket_iam_member" "landing_m360_bucket_admin" {
  bucket = data.google_storage_bucket.landing_m360.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_m360_bucket_reader" {
  bucket = data.google_storage_bucket.landing_m360.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_m360_bucket_creator" {
  bucket = data.google_storage_bucket.landing_m360.name
  role = "roles/storage.objectCreator"
  for_each = toset([
      "serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
      ])
  member = each.value
}


### Bucket Name: its-managed-dbx-de-01-t-landing-planib
resource "google_storage_bucket_iam_member" "landing_planib_bucket_admin" {
  bucket = module.test_landing_planib_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_planib_bucket_reader" {
  bucket = module.test_landing_planib_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_planib_bucket_creator" {
  bucket = module.test_landing_planib_bucket.name
  role = "roles/storage.objectCreator"
  for_each = toset([
      "serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
      ])
  member = each.value
}


### Bucket Name: its-managed-dbx-de-01-t-landing-qualtrics
resource "google_storage_bucket_iam_member" "landing_qualtrics_bucket_admin" {
  bucket = data.google_storage_bucket.landing_qualtrics.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_qualtrics_bucket_reader" {
  bucket = data.google_storage_bucket.landing_qualtrics.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_qualtrics_bucket_creator" {
  bucket = data.google_storage_bucket.landing_qualtrics.name
  role = "roles/storage.objectCreator"
  for_each = toset([
      "serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
      ])
  member = each.value
}


### Bucket Name: its-managed-dbx-de-01-t-landing-sfdc
resource "google_storage_bucket_iam_member" "landing_sfdc_bucket_admin" {
  bucket = module.test_landing_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_sfdc_bucket_reader" {
  bucket = module.test_landing_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_sfdc_bucket_creator" {
  bucket = module.test_landing_bucket.name
  role = "roles/storage.objectCreator"
  for_each = toset([
      "serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
      ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-landing-turtl
resource "google_storage_bucket_iam_member" "landing_turtl_bucket_admin" {
  bucket = data.google_storage_bucket.landing_turtl.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_turtl_bucket_reader" {
  bucket = data.google_storage_bucket.landing_turtl.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_turtl_bucket_creator" {
  bucket = data.google_storage_bucket.landing_turtl.name
  role = "roles/storage.objectCreator"
  for_each = toset([
      "serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
      ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-landing-vistex
resource "google_storage_bucket_iam_member" "landing_vistex_bucket_admin" {
  bucket = data.google_storage_bucket.landing_vistex.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_vistex_bucket_reader" {
  bucket = data.google_storage_bucket.landing_vistex.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "landing_vistex_bucket_creator" {
  bucket = data.google_storage_bucket.landing_vistex.name
  role = "roles/storage.objectCreator"
  for_each = toset([
      "serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
      ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-pipeline-code
resource "google_storage_bucket_iam_member" "pipeline_code_bucket_admin" {
  bucket = module.test_pipeline_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-ops@zebra.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
      "serviceAccount:1018680839633@cloudbuild.gserviceaccount.com"
    ])
  member = each.value
}
resource "google_storage_bucket_iam_member" "pipeline_code_bucket_reader" {
  bucket = module.test_pipeline_bucket.name
  role = "roles/storage.objectViewer"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-gke-gcs-object-reader-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-delta-bs-glo
resource "google_storage_bucket_iam_member" "delta_bs_glo_bucket_admin" {
  bucket = module.delta_bs_glo_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "serviceAccount:sa-glo-gke-dbx@its-managed-dbx-ds-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-landing-goas-user-data
resource "google_storage_bucket_iam_member" "goas_user_data_bucket_admin" {
  bucket = module.landing_goas_user_data_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
"serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
      "group:gcds-its-zap-de-developers@zebra.com"
    ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-delta-bs-goas
resource "google_storage_bucket_iam_member" "delta_bs_goas_bucket_admin" {
  bucket = module.delta_bs_goas_bucket.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
      "group:gcds-its-zap-de-developers@zebra.com"
    ])
  member = each.value
}
    
### Bucket Name: its-managed-dbx-de-01-t-landing-planisware
resource "google_storage_bucket_iam_member" "landing_planisware_bucket_admin" {
  bucket = data.google_storage_bucket.landing_planisware.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "serviceAccount:sa-edi-data-upload-t@za-global-service-accounts-p.iam.gserviceaccount.com",
      "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
      "serviceAccount:sa-composer@its-managed-dbx-edlops-t.iam.gserviceaccount.com"
    ])
  member = each.value
}    

### Bucket Name: its-managed-dbx-de-01-t-delta-bs-ihs
resource "google_storage_bucket_iam_member" "delta_bs_ihs_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_ihs.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-landing-ihs
resource "google_storage_bucket_iam_member" "landing_ihs_bucket_admin" {
  bucket = data.google_storage_bucket.landing_ihs.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
      "group:gcds-its-zap-de-developers@zebra.com",
      "serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    ])
  member = each.value
}


### Bucket Name: its-managed-dbx-de-01-t-landing-erp
resource "google_storage_bucket_iam_member" "landing_erp_bucket_admin" {
  bucket = data.google_storage_bucket.landing_erp.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-developers@zebra.com", 
    "group:gcds-its-zap-de-ops@zebra.com",
	  "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
    "serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
	])
  member = each.value
}

### Bucket Name: its-managed-dbx-de-01-t-delta-bs-erp
resource "google_storage_bucket_iam_member" "delta_bs_erp_bucket_admin" {
  bucket = data.google_storage_bucket.delta_bs_erp.name
  role = "roles/storage.objectAdmin"
  for_each = toset([
    "group:gcds-its-zap-de-developers@zebra.com", 
    "group:gcds-its-zap-de-ops@zebra.com",
	  "serviceAccount:sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com",
    "serviceAccount:sa-iics-gcs-object-create-view@its-managed-dbx-de-01-t.iam.gserviceaccount.com"

	])
  member = each.value
}