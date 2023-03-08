variable "project_id" {
  type        = string
  description = "The project ID to manage the Pub/Sub resources"
}
variable "pubsub_topic_name" {
  type        = string
  description = "pubsub topic name"
}

variable "topic_labels" {
  type        = map(string)
  description = "A map of labels to assign to the Pub/Sub topic"
  default     = {}
}

variable "push_subscriptions" {
  type        = list(map(string))
  description = "The list of the push subscriptions"
  default     = []
}

variable "message_storage_policy" {
  type        = map
  description = "A map of storage policies. Default - inherit from organization's Resource Location Restriction policy."
  default     = {}
}