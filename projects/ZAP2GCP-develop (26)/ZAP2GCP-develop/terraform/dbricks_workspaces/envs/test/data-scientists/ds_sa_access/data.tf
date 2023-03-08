data "google_storage_bucket" "databricks_2348922014507522" {
  name = "databricks-2348922014507522"
}

data "google_storage_bucket" "databricks_2348922014507522_system" {
  name = "databricks-2348922014507522-system"
}

data "google_storage_bucket" "pipeline_code" {
  name = "its-managed-dbx-ds-01-t-pipeline-code"
}

## DS WS WorkArea Buckets

data "google_storage_bucket" "glo_engineers_bucket" {
  name = "its-managed-dbx-ds-01-t-glo-engineers-workarea"
  depends_on = [
    module.glo_engineers_workarea_bucket
  ]
}

data "google_storage_bucket" "glo_analysts_bucket" {
  name = "its-managed-dbx-ds-01-t-glo-analysts-workarea"
  depends_on = [
    module.glo_analysts_workarea_bucket
  ]
}

data "google_storage_bucket" "glo_scientists_bucket" {
  name = "its-managed-dbx-ds-01-t-glo-scientists-workarea"
  depends_on = [
    module.glo_analysts_workarea_bucket
  ]
}

data "google_storage_bucket" "goas_enginners_bucket" {
  name = "its-managed-dbx-ds-01-t-goas-enginners-workarea"
  depends_on = [
    module.goas_enginners_workarea_bucket
  ]
}

data "google_storage_bucket" "goas_scientists_bucket" {
  name = "its-managed-dbx-ds-01-t-goas-scientists-workarea"
  depends_on = [
    module.goas_scientists_workarea_bucket
  ]
}

data "google_storage_bucket" "goas_analysts_bucket" {
  name = "its-managed-dbx-ds-01-t-goas-analysts-workarea"
  depends_on = [
    module.goas_analysts_workarea_bucket
  ]
}

data "google_storage_bucket" "fin_scientists_bucket" {
  name = "its-managed-dbx-ds-01-t-fin-scientists-workarea"
  depends_on = [
    module.fin_scientists_workarea_bucket
  ]
}

data "google_storage_bucket" "fin_enginners_bucket" {
  name = "its-managed-dbx-ds-01-t-fin-enginners-workarea"
  depends_on = [
    module.fin_enginners_workarea_bucket
  ]
}

data "google_storage_bucket" "fin_analysts_bucket" {
  name = "its-managed-dbx-ds-01-t-fin-analysts-workarea"
  depends_on = [
    module.fin_analysts_workarea_bucket
  ]
}

data "google_storage_bucket" "sec_fin_engineers_bucket" {
  name = "its-managed-dbx-ds-01-t-goas-ds-sec-fin-engineers-workarea"
  depends_on = [
    module.goas_fin_engineers_workarea_bucket
  ]
}

data "google_storage_bucket" "sec_fin_scientists_bucket" {
  name = "its-managed-dbx-ds-01-t-goas-ds-sec-fin-scientists-workarea"
  depends_on = [
    module.goas_scientists_workarea_bucket
  ]
}

data "google_storage_bucket" "sec_fin_analysts_bucket" {
  name = "its-managed-dbx-ds-01-t-goas-ds-sec-fin-analysts-workarea"
  depends_on = [
    module.goas_analysts_workarea_bucket
  ]
}

## DE DEV Buckets

data "google_storage_bucket" "delta_bs_eol_ds_access" {
  name = "its-managed-dbx-de-01-t-delta-bs-eol"
}

data "google_storage_bucket" "delta_bs_glo_ds_access" {
  name = "its-managed-dbx-de-01-t-delta-bs-glo"
}

data "google_storage_bucket" "delta_bs_grdf_ds_access" {
  name = "its-managed-dbx-de-01-t-delta-bs-grdf"
}

data "google_storage_bucket" "delta_bs_gst_ds_access" {
  name = "its-managed-dbx-de-01-t-delta-bs-gst"
}

data "google_storage_bucket" "delta_bs_planib_ds_access" {
  name = "its-managed-dbx-de-01-t-delta-bs-planib"
}

# data "google_storage_bucket" "delta_bs_rma_ds_access" {
#   name = "its-managed-dbx-de-01-t-delta-bs-rma"
# }

data "google_storage_bucket" "delta_bs_sfdc_ds_access" {
  name = "its-managed-dbx-de-01-t-delta-bs-sfdc"
}

data "google_storage_bucket" "delta_bs_gold_grdf_access" {
  name = "its-managed-dbx-de-01-t-delta-gold-grdf"
}

data "google_storage_bucket" "delta_bs_goas_access" {
  name = "its-managed-dbx-de-01-t-delta-bs-goas"
}

data "google_storage_bucket" "delta_bs_finance_ds_access" {
  name = "its-managed-dbx-de-01-t-delta-bs-finance"
}

data "google_storage_bucket" "delta_bs_ihs_ds_access" {
  name = "its-managed-dbx-de-01-t-delta-bs-ihs"
}

