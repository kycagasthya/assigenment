terraform {
  required_version = ">= 0.13.0"

  backend "gcs" {
    bucket = "uwm-platform-api-testing"
    prefix = "uwm/statefiles"
  }

}