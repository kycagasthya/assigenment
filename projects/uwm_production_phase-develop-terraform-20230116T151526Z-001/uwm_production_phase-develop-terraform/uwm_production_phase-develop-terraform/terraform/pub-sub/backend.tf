terraform {
  required_version = ">= 0.12"

  backend "gcs" {
    bucket = "teraform-tamplate-store"
    prefix = "uwm/pubsub"
  }

  required_providers {
    google      = "3.9.0"
    google-beta = "3.9.0"
  }
}

