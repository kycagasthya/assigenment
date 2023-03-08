/*********************************************************
          IAM Access to Buckets
*********************************************************/
resource "google_storage_bucket_iam_member" "cb_sa_storage_admin" {
  bucket = module.cb_log_bucket.name
  role   = "roles/storage.admin"
  member = "serviceAccount:${var.cloud_build_sa}"
}

resource "google_storage_bucket_iam_member" "tf_sa_storage_admin" {
  bucket = module.cb_log_bucket.name
  role   = "roles/storage.admin"
  member = "serviceAccount:${var.terraform_sa_email}"
}

resource "google_storage_bucket_iam_member" "dev_pipeline_sa_storage_admin" {
  bucket = data.google_storage_bucket.dev_data_engg_pipeline.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${var.cloud_build_sa}"
}

resource "google_storage_bucket_iam_member" "test_pipeline_sa_storage_admin" {
  bucket = data.google_storage_bucket.test_data_engg_pipeline.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${var.cloud_build_sa}"
}     

resource "google_storage_bucket_iam_member" "composer_sa_storage_admin" {
  bucket = data.google_storage_bucket.dev_cc_bucket.name
  role   = "roles/storage.admin"
  member = "serviceAccount:${var.cloud_build_sa}"
}

/*********************************************************
          Log Bucket
*********************************************************/
module "cb_log_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-log-bucket"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}
