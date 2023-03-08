resource "google_storage_bucket" "static-site" {
  name          = "uwm-teraform-template"
  project       = var.project_id
  location      = "US"
  force_destroy = true
}
 # uniform_bucket_level_access = true

