provider "google" {
  region      = var.location
  project     = var.project_id
  credentials = file(var.credentials_file_path)
}
