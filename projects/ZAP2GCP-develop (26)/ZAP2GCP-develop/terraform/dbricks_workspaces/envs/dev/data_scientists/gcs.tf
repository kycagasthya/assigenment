/******************************************
  Cloud Storage Buckets
 *****************************************/
module "user_work_area_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-user-work-area"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}

module "dev_pipeline_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-pipeline-code"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}

module "fin_workarea_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-fin-workarea"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}
/*module "landing_grdf_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-landing-grdf"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}*/

/* module "delta_bs_grdf_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-delta-bs-grdf"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
} */

/* module "delta_gold_grdf_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-delta-gold-grdff"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
} */

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
