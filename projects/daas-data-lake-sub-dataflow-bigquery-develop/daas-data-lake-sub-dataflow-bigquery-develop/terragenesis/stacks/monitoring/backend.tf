terraform {
  backend "gcs" {
    prefix = "monitoring/state"
  }
}
