terraform {
  required_version = ">= 0.13"
  required_providers {
    google = {
      source = "hashicorp/google"
      # TODO: Check why this filter was breaking tests.
      # version = "~> 3.53, < 5.0"
    }
  }

  provider_meta "google" {
    module_name = "blueprints/terraform/terraform-google-three-tier-app/v0.1.1"
  }
}
