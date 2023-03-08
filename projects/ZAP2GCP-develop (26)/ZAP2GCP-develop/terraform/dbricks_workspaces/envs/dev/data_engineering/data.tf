data "google_storage_bucket" "azuretogcptest" {
  name = "azuretogcptest"
}

data "google_storage_bucket" "databricks_1235921161438059" {
  name = "databricks-1235921161438059"
}

data "google_storage_bucket" "databricks_1235921161438059_system" {
  name = "databricks-1235921161438059-system"
}

data "google_storage_bucket" "delta_bs_adobe" {
  name = "its-managed-dbx-zap-d-delta-bs-adobe"
}

data "google_storage_bucket" "delta_bs_rma" {
  name = "its-managed-dbx-zap-d-delta-bs-rma"
}

data "google_storage_bucket" "history_azure" {
  name = "its-managed-dbx-zap-d-history-azure"
}

data "google_storage_bucket" "landing_adobe" {
  name = "its-managed-dbx-zap-d-landing-adobe"
}

data "google_storage_bucket" "landing_digst" {
  name = "its-managed-dbx-zap-d-landing-digst"
}

data "google_storage_bucket" "landing_disfdc" {
  name = "its-managed-dbx-zap-d-landing-disfdc"
}

data "google_storage_bucket" "landing_dsfdc" {
  name = "its-managed-dbx-zap-d-landing-dsfdc"
}

data "google_storage_bucket" "landing_glo" {
  name = "its-managed-dbx-zap-d-landing-glo"
}

data "google_storage_bucket" "landing_gst" {
  name = "its-managed-dbx-zap-d-landing-gst"
}

data "google_storage_bucket" "landing_rma" {
  name = "its-managed-dbx-zap-d-landing-rma"
}

data "google_storage_bucket" "landing_sfdc" {
  name = "its-managed-dbx-zap-d-landing-sfdc"
}

data "google_storage_bucket" "test_read" {
  name = "test_read"
}

data "google_storage_bucket" "delta_bs_glo" {
  name = "its-managed-dbx-zap-d-delta-bs-glo"
}

data "google_storage_bucket" "landing_erp" {
  name = "its-managed-dbx-zap-d-landing-erp"
  depends_on = [module.landing_erp_bucket]
}

data "google_storage_bucket" "delta_bs_erp" {
  name = "its-managed-dbx-zap-d-delta-bs-erp"
  depends_on = [module.delta_bs_erp_bucket]
}