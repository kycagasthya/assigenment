variable "project_id" {
  type        = string
  description = "The project ID to manage the Pub/Sub resources"
}

variable "pubsub_subscription_name" {
  type        = string
  description = "The pubsub subscription name"
}

variable "topic_name" {
  type        = string
  description = "topic name name for pubsub subscription"
}