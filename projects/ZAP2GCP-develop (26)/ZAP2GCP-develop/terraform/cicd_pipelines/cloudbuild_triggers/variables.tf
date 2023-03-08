variable "project_id" {
  description = "The GCP project ID."
  type        = string
}

variable "terraform_sa_email" {
  description = "Terraform service account email id."
  type        = string
}

variable "cloud_build_sa" {
  description = "Cloud Build Terraform service account email id."
  type        = string
}

variable "storage_bucket_labels" {
  description = "A map of key/value label pairs to assign to the logsinks GCS bucket."
  type        = map(string)
}
