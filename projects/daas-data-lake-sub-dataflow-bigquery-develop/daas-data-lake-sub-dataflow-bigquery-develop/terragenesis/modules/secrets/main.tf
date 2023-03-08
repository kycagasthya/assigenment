resource "google_secret_manager_secret" "secret_object" {
  secret_id = var.secret_name

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "secret_value" {
  secret      = google_secret_manager_secret.secret_object.id
  secret_data = var.secret_value
}
