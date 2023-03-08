variable "project" {
  type        = string
  description = "The name of the GCP project to create the resources in."
}

variable "region" {
  type        = string
  description = "Google Cloud region to deploy the stack."
  default     = "us-east1"
}

variable "zone" {
  type        = string
  description = "Google Cloud zone to deploy the stack."
  default     = "us-east1-b"
}

variable "pubsub_topic_name" {
  type        = string
  description = "Pub/Sub topic unique name."
}

variable "labels" {
  type        = map(string)
  description = "Input variable for labels."
}
