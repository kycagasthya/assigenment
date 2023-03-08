resource "google_pubsub_topic" "topic1" {
  project = var.project_id
  name    = "uwm-classifcation-topic1"
  labels  = var.topic_labels

  dynamic "message_storage_policy" {
    for_each = var.message_storage_policy
    content {
      allowed_persistence_regions = message_storage_policy.key == "allowed_persistence_regions" ? message_storage_policy.value : null
    }
  }
}

resource "google_pubsub_subscription" "input-ds" {
  name    = "uwm-classifcation-sub1"
  topic   = google_pubsub_topic.topic1.name
  project = var.project_id
  ack_deadline_seconds = 10
  message_retention_duration = "600s"
  depends_on = [google_pubsub_topic.topic1]
}

