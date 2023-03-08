terraform {
  backend "gcs" {
    prefix = "infrastructure/state"
  }
}
