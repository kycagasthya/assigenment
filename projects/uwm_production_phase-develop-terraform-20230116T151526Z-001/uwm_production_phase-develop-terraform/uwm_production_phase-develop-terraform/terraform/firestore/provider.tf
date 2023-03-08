provider "google" {
  project     = var.project_id
  credentials = file(var.credentials_file_path)
 }