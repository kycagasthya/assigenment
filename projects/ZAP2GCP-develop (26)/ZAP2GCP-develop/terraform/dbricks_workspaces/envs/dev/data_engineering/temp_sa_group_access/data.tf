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

data "google_storage_bucket" "delta_bs_demandbase" {
  name = "its-managed-dbx-zap-d-delta-bs-demandbase"
}
#module.delta_bs_demandbase_bucket.name
#data.google_storage_bucket.delta_bs_demandbase.name

data "google_storage_bucket" "delta_bs_dwa" {
  name = "its-managed-dbx-zap-d-delta-bs-dwa"
}
#module.delta_bs_dwa_bucket.name
#data.google_storage_bucket.delta_bs_dwa.name


data "google_storage_bucket" "delta_bs_eloqua" {
  name = "its-managed-dbx-zap-d-delta-bs-eloqua"
}
#module.delta_bs_eloqua_bucket.name
#data.google_storage_bucket.delta_bs_eloqua.name

data "google_storage_bucket" "delta_bs_eol" {
  name = "its-managed-dbx-zap-d-delta-bs-eol"
}
#module.nc_dev_delta_eol_bucket.name
#data.google_storage_bucket.delta_bs_eol.name

data "google_storage_bucket" "delta_bs_evergage" {
  name = "its-managed-dbx-zap-d-delta-bs-evergage"
}
#module.delta_bs_evergage_bucket.name
#data.google_storage_bucket.delta_bs_evergage.name

data "google_storage_bucket" "delta_bs_grdf" {
  name = "its-managed-dbx-zap-d-delta-bs-grdf"
}
#module.delta_bs_grdf_bucket.name
#data.google_storage_bucket.delta_bs_grdf.name

data "google_storage_bucket" "delta_bs_gst" {
  name = "its-managed-dbx-zap-d-delta-bs-gst"
}
#module.delta_bs_gst_bucket.name
#data.google_storage_bucket.delta_bs_gst.name

data "google_storage_bucket" "delta_bs_m360" {
  name = "its-managed-dbx-zap-d-delta-bs-m360"
}
#module.delta_bs_m360_bucket.name
#data.google_storage_bucket.delta_bs_m360.name

data "google_storage_bucket" "delta_bs_planib" {
  name = "its-managed-dbx-zap-d-delta-bs-planib"
}
#module.nc_dev_delta_bs_planib_bucket.name
#data.google_storage_bucket.delta_bs_planib.name

data "google_storage_bucket" "delta_bs_qualtrics" {
  name = "its-managed-dbx-zap-d-delta-bs-qualtrics"
}
#module.delta_bs_qualtrics_bucket.name
#data.google_storage_bucket.delta_bs_qualtrics.name

data "google_storage_bucket" "delta_bs_sfdc" {
  name = "its-managed-dbx-zap-d-delta-bs-sfdc"
}
#module.nc_dev_delta_sfdc_bucket.name
#data.google_storage_bucket.delta_bs_sfdc.name

data "google_storage_bucket" "delta_bs_turtl" {
  name = "its-managed-dbx-zap-d-delta-bs-turtl"
}
#module.delta_bs_turtl_bucket.name
#data.google_storage_bucket.delta_bs_turtl.name

data "google_storage_bucket" "delta_bs_vistex" {
  name = "its-managed-dbx-zap-d-delta-bs-vistex"
}
#module.delta_bs_vistex_bucket.name
#data.google_storage_bucket.delta_bs_vistex.name

data "google_storage_bucket" "delta_gold_grdf" {
  name = "its-managed-dbx-zap-d-delta-gold-grdf"
}
#module.delta_gold_grdf_bucket.name
#data.google_storage_bucket.delta_gold_grdf.name
##

data "google_storage_bucket" "landing_evergage" {
  name = "its-managed-dbx-zap-d-landing-evergage"
}
#module.landing_evergage_bucket.name
#data.google_storage_bucket.landing_evergage.name

data "google_storage_bucket" "landing_demandbase" {
  name = "its-managed-dbx-zap-d-landing-demandbase"
}
#module.landing_demandbase_bucket.name
#data.google_storage_bucket.landing_demandbase.name

data "google_storage_bucket" "landing_dwa" {
  name = "its-managed-dbx-zap-d-landing-dwa"
}
#module.landing_dwa_bucket.name
#data.google_storage_bucket.landing_dwa.name


data "google_storage_bucket" "landing_eloqua" {
  name = "its-managed-dbx-zap-d-landing-eloqua"
}
#module.landing_eloqua_bucket.name
#data.google_storage_bucket.landing_eloqua.name


data "google_storage_bucket" "landing_eol" {
  name = "its-managed-dbx-zap-d-landing-eol"
}
#module.nc_dev_landing_eol_bucket.name
#data.google_storage_bucket.landing_eol.name

data "google_storage_bucket" "landing_grdf" {
  name = "its-managed-dbx-zap-d-landing-grdf"
}
#module.landing_grdf_bucket.name
#data.google_storage_bucket.landing_grdf.name

data "google_storage_bucket" "landing_m360" {
  name = "its-managed-dbx-zap-d-landing-m360"
}
#module.landing_m360_bucket.name
#data.google_storage_bucket.landing_m360.name

data "google_storage_bucket" "landing_planib" {
  name = "its-managed-dbx-zap-d-landing-planib"
}
#module.nc_dev_landing_planib_bucket.name
#data.google_storage_bucket.landing_planib.name

data "google_storage_bucket" "landing_qualtrics" {
  name = "its-managed-dbx-zap-d-landing-qualtrics"
}
#module.landing_qualtrics_bucket.name
#data.google_storage_bucket.landing_qualtrics.name

data "google_storage_bucket" "landing_turtl" {
  name = "its-managed-dbx-zap-d-landing-turtl"
}
#module.landing_turtl_bucket.name
#data.google_storage_bucket.landing_turtl.name

data "google_storage_bucket" "landing_vistex" {
  name = "its-managed-dbx-zap-d-landing-vistex"
}
#module.landing_vistex_bucket.name
#data.google_storage_bucket.landing_vistex.name

data "google_storage_bucket" "pipeline_code" {
  name = "its-managed-dbx-zap-d-pipeline-code"
}
#module.dev_pipeline_bucket.name
#data.google_storage_bucket.pipeline_code.name

data "google_storage_bucket" "goas_user_data" {
  name = "its-managed-dbx-zap-d-landing-goas-user-data"
}
#module.landing_goas_user_data_bucket.name
#data.google_storage_bucket.goas_user_data.name

data "google_storage_bucket" "delta_bs_goas" {
  name = "its-managed-dbx-zap-d-delta-bs-goas"
}
#module.delta_bs_goas_bucket.name
#data.google_storage_bucket.delta_bs_goas.name

data "google_storage_bucket" "landing_ihs" {
  name = "its-managed-dbx-zap-d-landing-ihs"
}
#module.landing_ihs.name
#data.google_storage_bucket.landing_ihs.name

data "google_storage_bucket" "delta_bs_ihs" {
  name = "its-managed-dbx-zap-d-delta-bs-ihs"
}

data "google_storage_bucket" "landing_planisware" {
  name = "its-managed-dbx-zap-d-landing-planisware"
}

#module.delta_bs_ihs.name
#data.google_storage_bucket.delta_bs_ihs.name



/***********************************************
Data block for Service account and groups
************************************************/
/*
data "google_service_account" "cluster_de_admin_sa" {
  account_id = "sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
}

data "google_service_account" "cluster_de_read_sa" {
  account_id = "sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
}

data "google_service_account" "cluster_de_readerite_sa" {
  account_id = "sa-dbx-de-readwrite-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
}

data "google_service_account" "dbx_goassecfin_de_sa" {
  account_id = "sa-dbx-goassecfin-de-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
}

data "google_service_account" "dbx_goassecfin_ds_sa" {
  account_id = "sa-dbx-goassecfin-ds-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
}

data "google_service_account" "dbx_goassecfin_da_sa" {
  account_id = "sa-dbx-goassecfin-da-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
}

data "google_service_account" "dbx_glo_de_sa" {
  account_id = "sa-dbx-glo-de-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
}

data "google_service_account" "dbx_glo_ds_sa" {
  account_id = "sa-dbx-glo-ds-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
}

data "google_service_account" "dbx_glo_da_sa" {
  account_id = "sa-dbx-glo-da-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
}

data "google_service_account" "dbx_goas_de_sa" {
  account_id = "sa-dbx-goas-de-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
}

data "google_service_account" "dbx_goas_ds_sa" {
  account_id = "sa-dbx-goas-ds-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
}

data "google_service_account" "dbx_goas_da_sa" {
  account_id = "sa-dbx-goas-da-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
}

data "google_service_account" "dbx_fin_de_sa" {
  account_id = "sa-dbx-fin-de-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
}

data "google_service_account" "dbx_fin_ds_sa" {
  account_id = "sa-dbx-fin-ds-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
}

data "google_service_account" "dbx_fin_da_sa" {
  account_id = "sa-dbx-fin-da-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
}

data "google_service_account" "dbx_sales_de_sa" {
  account_id = "sa-dbx-sales-de-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
}

data "google_service_account" "dbx_sales_ds_sa" {
  account_id = "sa-dbx-sales-ds-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
}

data "google_service_account" "dbx_sales_da_sa" {
  account_id = "sa-dbx-sales-da-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
}

data "google_service_account" "dbx_mktg_de_sa" {
  account_id = "sa-dbx-mktg-de-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
}

data "google_service_account" "dbx_mktg_ds_sa" {
  account_id = "sa-dbx-mktg-ds-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
}

data "google_service_account" "dbx_mktg_da_sa" {
  account_id = "sa-dbx-mktg-da-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
}

data "google_service_account" "iics_objectcreate_sa" {
  account_id = "sa-iics-gcs-object-create-view@its-managed-dbx-zap-d.iam.gserviceaccount.com"
}

data "google_service_account" "edi_data_upload_t_sa" {
  account_id = "sa-edi-data-upload-t@za-global-service-accounts-p.iam.gserviceaccount.com"
}

data "google_service_account" "edi_data_upload_sa" {
  account_id = "sa-edi-data-upload@its-managed-dbx-zap-d.iam.gserviceaccount.com"
}

data "google_service_account" "rpa_dbx_glo_sa" {
  account_id = "sa-rpa-dbx-glo-p@za-global-service-accounts.iam.gserviceaccount.com"
}
*/

