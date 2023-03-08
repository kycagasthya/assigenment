variable "project_id" {
  description = "The ID of the Google Cloud project"
}

variable "network" {
  type        = string
  description = "The name of the Shared network "
}

variable "subnetwork" {
  type        = string
  description = "The name of the Shared subnetwork "
}

variable "ip_range_pods" {
  type        = string
  description = "The name of the gke pod ip range "
}

variable "ip_range_services" {
  type        = string
  description = "The name of the gke Service ip range "
}

variable "nodepool_service_account" {
  type        = string
  description = "The name of nodepool service account "
}

variable "host-project-id" {
  type        = string
  description = "The name of host project "
}
