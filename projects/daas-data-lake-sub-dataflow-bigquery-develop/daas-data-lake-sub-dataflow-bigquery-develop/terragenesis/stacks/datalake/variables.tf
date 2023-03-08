variable "project" {
  type        = string
  description = "The ID of the project in which the resource belongs."
}

variable "region" {
  type        = string
  description = "A reference to the region where the resources reside."
  default     = "us-east1"
}

variable "env" {
  type        = string
  description = "Describes a general deployment target."
}

variable "client_id" {
  type        = string
  description = "A unique ID for the client."
  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{0,63}$", var.client_id))
    error_message = "The client_id value must not be longer than 64 characters, must start with a lowercase letter and only contain letters, numbers or hyphens."
  }
}

variable "dataset_id" {
  type        = string
  description = "A unique ID for dataset, without the project name."
  validation {
    condition     = can(regex("^[a-z][a-z0-9_]{0,63}$", var.dataset_id))
    error_message = "The dataset_id value must not be longer than 64 characters, must start with a lowercase letter and only contain letters, numbers or underscores."
  }
}

variable "sources" {
  type = map(object({
    source_name    = string
    schema_version = string
  }))
  validation {
    condition     = can([for k, v in var.sources : regex("^[a-z][a-z0-9_]{0,63}$", v.source_name)])
    error_message = "The source_name value must not be longer than 64 characters, must start with a lowercase letter and only contain letters, numbers or underscores."
  }
  validation {
    condition     = can([for k, v in var.sources : regex("^[a-z][a-z0-9-]{0,63}$", v.schema_version)])
    error_message = "The schema_version value must not be longer than 64 characters, must start with a lowercase letter and only contain letters, numbers or hyphens."
  }
  description = "Pub/Sub source complex definition."
}

variable "tables" {
  type = map(object({
    table_id          = string
    protected         = bool
    description       = string
    client_labels     = map(any)
    table_schema_file = string
  }))
  validation {
    condition     = can([for k, v in var.tables : regex("^[a-zA-Z][a-zA-Z0-9_]{0,63}$", v.table_id)])
    error_message = "The table_id value must not be longer than 64 characters, must start with a letter and only contain letters, numbers or underscores."
  }
  description = "BigQuery table complex definition."
}

variable "template_path" {
  type        = string
  description = "The GCS path to the Dataflow job flex template."
  validation {
    condition     = can(regex("^gs://[a-z0-9/_-]*\\.json$", var.template_path))
    error_message = "The template_path value must be a valid gs:// path to JSON manifest."
  }
}

variable "labels" {
  type        = map(string)
  description = "The labels associated with resources. Used to organize and group different cloud resources."
  default = {
    vendor = "takeoff"
  }
}

variable "views" {
  type = map(object({
    view_id         = string
    view_query_file = string
  }))
  validation {
    condition     = can([for k, v in var.views : regex("^[a-zA-Z][a-zA-Z0-9_]{0,63}$", v.view_id)])
    error_message = "The view_id value must not be longer than 64 characters, must start with a letter and only contain letters, numbers or underscores."
  }
  description = "BigQuery view table complex definition."
  default     = {}
}

variable "raw_prefix" {
  type        = string
  description = "Defines string prefix for PubSub to Bigquery export resources."
  default     = "raw"
}

variable "tag" {
  type        = string
  description = "Tag related to datalake being created. E.g. `datalake-444`"
  default     = ""
}
