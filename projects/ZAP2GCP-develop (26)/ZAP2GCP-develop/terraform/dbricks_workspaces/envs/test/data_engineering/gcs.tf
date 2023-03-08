/******************************************
  Cloud Storage Buckets for test env
 *****************************************/
module "test_landing_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-landing-sfdc"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = true
  force_destroy = false
  labels        = var.storage_bucket_labels
}

module "test_delta_sfdc_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-delta-bs-sfdc"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}

module "test_landing_eol_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-landing-eol"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = true
  force_destroy = false
  labels        = var.storage_bucket_labels
}

module "test_delta_eol_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-delta-bs-eol"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}

module "test_landing_planib_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-landing-planib"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = true
  force_destroy = false
  labels        = var.storage_bucket_labels
}

module "test_delta_bs_planib_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-delta-bs-planib"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}

module "test_pipeline_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-pipeline-code"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}

module "test_landing_evergage_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-landing-evergage"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}


module "test_delta_bs_evergage_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-delta-bs-evergage"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}

module "landing_grdf_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-landing-grdf"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}

module "delta_bs_grdf_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-delta-bs-grdf"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}

module "delta_gold_grdf_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-delta-gold-grdf"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}

module "delta_bs_glo_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-delta-bs-glo"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}


module "landing_goas_user_data_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-landing-goas-user-data"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}

module "delta_bs_goas_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-delta-bs-goas"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}

module "landing_finance_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-landing-finance"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}

module "delta_bs_finance_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-delta-bs-finance"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}

module "delta_gold_finance_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-delta-gold-finance"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}

module "delta_bs_planisware_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-delta-bs-planisware"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}

module "landing_planisware_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-landing-planisware"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}

module "landing_ihs_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-landing-ihs"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}

module "delta_bs_ihs_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-delta-bs-ihs"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}

# Work Area buckets for DE, DS and DA
module "datascientist_workarea_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-datascientist-workarea"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}

module "dataengg_workarea_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-dataengg-workarea"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}

module "dataanalyst_workarea_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-dataanalyst-workarea"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}


module "landing_onclusive_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-landing-onclusive"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}

module "delta_bs_onclusive_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-delta-bs-onclusive"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}

module "landing_erp_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-landing-erp"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}

module "delta_bs_erp_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-delta-bs-erp"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}