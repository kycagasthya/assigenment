variable "project" {
  type        = string
  description = "Google project ID the resource belongs to"
}

variable "service_account_id" {
  type        = string
  description = "IAM service account ID to be created"
  default     = ""
}

variable "service_account_description" {
  type        = string
  description = "IAM service account display name"
  default     = ""
}

# variable "service_account_email" {
#   type        = string
#   description = "Existing IAM service account email to be used"
#   default     = ""
# }

variable "iam_roles" {
  type        = list(string)
  description = "List of IAM roles to be applied to the service account"
  default     = []
}
