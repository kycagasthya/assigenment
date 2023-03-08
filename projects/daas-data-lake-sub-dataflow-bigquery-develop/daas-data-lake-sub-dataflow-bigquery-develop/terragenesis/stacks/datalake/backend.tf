terraform {
  backend "gcs" {
    prefix = "snfk-to-gcp/state"
  }
}
