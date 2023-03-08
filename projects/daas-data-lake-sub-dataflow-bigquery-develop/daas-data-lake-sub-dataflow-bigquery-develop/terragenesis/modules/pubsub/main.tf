resource "google_pubsub_topic" "pubsub_topic" {
  name = var.pubsub_topic_name
  labels = var.labels
}

resource "google_pubsub_subscription" "ps_subscr" {
  name  = google_pubsub_topic.pubsub_topic.name
  topic = google_pubsub_topic.pubsub_topic.name

  message_retention_duration = "604800s"
  retain_acked_messages      = false

  ack_deadline_seconds = 20

  expiration_policy {
    ttl = "" # Never expires
  }

  labels = var.labels

  enable_message_ordering = false
}
