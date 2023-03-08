resource "google_pubsub_topic" "topic" {
  project = var.project_id
  name    = var.pubsub_topic_name
  labels  = var.topic_labels

  dynamic "message_storage_policy" {
    for_each = var.message_storage_policy
    content {
      allowed_persistence_regions = message_storage_policy.key == "allowed_persistence_regions" ? message_storage_policy.value : null
    }
  }
}