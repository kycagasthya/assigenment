data "archive_file" "source" {
  type        = "zip"
  source_dir  = var.source_dir
  output_path = "/tmp/${var.app_name}.zip"
}

resource "google_storage_bucket_object" "archive" {
  source       = data.archive_file.source.output_path
  content_type = "application/zip"
  name         = "${var.app_name}/${substr(data.archive_file.source.output_sha, 0, 10)}.zip"
  bucket       = var.artifacts_bucket
}

# resource "google_cloudfunctions_function" "function" {
#   name        = var.app_name
#   description = var.description
#   region      = var.region
#   runtime     = var.runtime

#   environment_variables = {
#     GCP_PROJECT = var.project
#   }

#   source_archive_bucket = var.artifacts_bucket
#   source_archive_object = google_storage_bucket_object.archive.name
#   trigger_http          = true
#   entry_point           = var.entrypoint
#   service_account_email = var.service_account_email
# }

resource "google_cloudfunctions2_function" "function" {
  name        = "${var.app_name}-gen2"
  location    = var.region
  description = var.description

  build_config {
    runtime     = var.runtime
    entry_point = var.entrypoint
    source {
      storage_source {
        bucket = var.artifacts_bucket
        object = google_storage_bucket_object.archive.name
      }
    }
  }
  service_config {
    max_instance_count    = 1
    available_memory      = "512M"
    timeout_seconds       = var.timeout_seconds
    environment_variables = var.env_vars
    service_account_email = var.service_account_email
  }
}
