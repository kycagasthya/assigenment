variable "project" {
  type        = string
  description = "The name of the GCP project to create the resources in"
}

variable "region" {
  type        = string
  description = "Google Cloud Region to deploy the stack"
  default     = "us-east1"
}

variable "zone" {
  type        = string
  description = "Google Cloud Zone to deploy the stack"
  default     = "us-east1-b"
}

variable "dataset_id" {
  type        = string
  description = "BigQuery dataset ID"
}

variable "table_id" {
  type        = string
  description = "BigQuery dataset table ID"
}

variable "description" {
  type        = string
  description = "BigQuery table short description"
}

variable "table_schema" {
  type        = string
  description = "BigQuery table schema definition"
}

# It is recommended to not set it to false in production or until you're ready to destroy.
variable "protected" {
  type        = bool
  description = "If BigQuery table protected from deletion or not."
  default     = true
}

variable "labels" {
  type        = map(string)
  description = "Input variable for labels"
}
