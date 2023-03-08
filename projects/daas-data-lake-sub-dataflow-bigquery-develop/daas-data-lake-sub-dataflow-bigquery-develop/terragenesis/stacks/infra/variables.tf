variable "project" {
  type        = string
  description = "The ID of the project in which the resource belongs."
}

variable "env" {
  type        = string
  description = "Describes a general deployment target."
}

variable "dataset_id" {
  type        = string
  description = "A unique ID for dataset, without the project name."
  validation {
    condition     = can(regex("^[a-z][a-z0-9_]{0,31}$", var.dataset_id))
    error_message = "The dataset_id value must not be longer than 32 characters, must start with a lowercase letter and only contain letters, numbers or underscores."
  }
  default = "dl_service"
}

variable "missed_records_table_name" {
  type        = string
  description = "BigQuery table name from missed records table"
  default     = "missed_records"
}

variable "tables" {
  type = map(object({
    table_id          = string
    description       = string
    table_schema_file = string
  }))
  validation {
    condition     = can([for k, v in var.tables : regex("^[a-zA-Z][a-zA-Z0-9_]{0,31}$", v.table_id)])
    error_message = "The table_id value must not be longer than 32 characters, must start with a letter and only contain letters, numbers or underscores."
  }
  description = "BigQuery table complex definition."
  default = {
    ingest_errors = {
      table_id          = "ingest_errors",
      description       = "BigQuery ingest errors table"
      table_schema_file = "ingest_errors.json"
    },
    missed_records = {
      table_id          = "missed_records",
      description       = "BigQuery table for staging of missed records"
      table_schema_file = "missed_records.json"
    }
  }
}

variable "labels" {
  type        = map(string)
  description = "The labels associated with resources. Used to organize and group different cloud resources."
  default = {
    platform = "google"
  }
}

variable "github_private_access_token" {
  type        = string
  description = "GitHub private access token"
}

variable "publisher_project_id" {
  type        = string
  description = "GitHub private access token"
}

variable "slack" {
  type = object({
    notification_channel = string
    auth_token           = string
  })
  validation {
    condition     = can(regex("^#[a-z0-9-]{0,63}$", var.slack["notification_channel"]))
    error_message = "The notification_channel value must not be longer than 64 characters, must start with a number sign and only contain lowercase letters, numbers or hyphens."
  }
}

variable "opsgenie_token" {
  type        = string
  description = "Opsgenie integration auth token"
  sensitive   = true
}

variable "tag" {
  type        = string
  description = "Tag related to datalake being created. E.g. `datalake-444`"
  default     = ""
}
