variable "project_id" {
  description = "The project ID to deploy to"
}


variable "region" {
  type        = string
  description = "The Compute Region to deploy to"
}
variable "region_s" {
  type        = string
  description = "The Compute Region to deploy to"
}
variable "zone" {
  type        = string
  description = "The Compute Zone to deploy to"
}


variable "deployment_name" {
  type        = string
  description = "The name of this particular deployment, will get added as a prefix to most resources."
  default     = "three-tier-app"
}


variable "labels" {
  type        = map(string)
  description = "A map of labels to apply to contained resources."
  default     = { "three-tier-app" = true }
}

variable "enable_apis" {
  type        = string
  description = "Whether or not to enable underlying apis in this solution. ."
  default     = true
}
