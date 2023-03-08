resource "google_storage_bucket" "df_bucket" {
  name          = "${var.project}-dataflow"
  location      = "US"
  project       = var.project
  force_destroy = true
}

resource "google_storage_bucket" "backup_bucket" {
  name          = "${var.project}-pubsub-backup"
  location      = "US"
  project       = var.project
  force_destroy = true

  lifecycle_rule {
    condition {
      age                   = 30
      matches_storage_class = ["STANDARD"]
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }

  lifecycle_rule {
    condition {
      age                   = 90
      matches_storage_class = ["NEARLINE"]
    }
    action {
      type          = "SetStorageClass"
      storage_class = "COLDLINE"
    }
  }

  lifecycle_rule {
    condition {
      age                   = 720
      matches_storage_class = ["COLDLINE"]
    }
    action {
      type          = "SetStorageClass"
      storage_class = "ARCHIVE"
    }
  }
}

resource "google_storage_bucket" "artifacts" {
  name          = "${var.project}-artifacts"
  location      = "US"
  project       = var.project
  force_destroy = true
}
