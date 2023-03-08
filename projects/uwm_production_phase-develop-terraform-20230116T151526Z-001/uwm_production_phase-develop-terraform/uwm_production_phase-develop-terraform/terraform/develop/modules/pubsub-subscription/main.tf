resource "google_pubsub_subscription" "pubsub_subscription" {
  name    = var.pubsub_subscription_name
  topic   = var.topic_name
  project = var.project_id
  ack_deadline_seconds = 10
  message_retention_duration = "600s" 
}