variable "project_id" {
  type        = string
  description = "The project ID to manage the Pub/Sub resources"
  default     = "qp-uwm-terra1-2021-02"
}

variable "bucket_name" {
  type        = string
  description = "The project ID to manage the Pub/Sub resources"
  default     = "uwm-teraform-template"
}

variable "topic_name" {
  type        = string
  description = "The project ID to manage the Pub/Sub resources"
  default     = "projects/qp-uwm-terra1-2021-02/topics/uwm-classifcation-topic1"
}
