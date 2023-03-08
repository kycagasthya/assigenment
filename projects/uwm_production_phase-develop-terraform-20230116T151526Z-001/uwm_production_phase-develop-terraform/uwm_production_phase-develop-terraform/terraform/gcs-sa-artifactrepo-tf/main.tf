module "docker_artifact_registry" {
  source     = "./modules/artifact-registry"
  project_id = var.project_id
  location   = var.location
  format     = "DOCKER"
  repository_name  = "myregistry"
    labels = {
        env      = "dev"
        billable = "true"
      }
}

module "service-account1" {
  source            = "./modules/iam-service-account"
  project_id        = var.project_id
  account_id        = "test-terraform"
  display_name      = "test-terraform"
}

module "bucket" {
  source     = "./modules/gcs"
  project_id = var.project_id
  prefix     = "test"
  name       = "my-bucket"
  location   = "US"
}
