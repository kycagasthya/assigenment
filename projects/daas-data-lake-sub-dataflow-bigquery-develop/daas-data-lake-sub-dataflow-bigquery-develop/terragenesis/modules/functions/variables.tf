variable "project" {

}

variable "region" {

}

variable "app_name" {

}

variable "description" {

}

variable "source_dir" {

}

variable "runtime" {

}

variable "entrypoint" {

}

variable "artifacts_bucket" {

}

variable "service_account_email" {

}

variable "env_vars" {
  type        = map(string)
  description = "A map of environment variables for a Cloud Function"
}

variable "timeout_seconds" {
  type        = number
  description = "Cloud Function execution timeout in seconds"
  default     = 180
}
