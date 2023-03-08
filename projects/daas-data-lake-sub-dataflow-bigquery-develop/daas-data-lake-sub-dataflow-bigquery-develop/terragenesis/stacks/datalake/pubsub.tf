module "google_pubsub" {
  source            = "../../modules/pubsub"
  for_each          = var.sources
  project           = var.project
  pubsub_topic_name = "${var.client_id}-${each.value.source_name}-${each.value.schema_version}"
  labels = {
    client_name = var.client_id
    source_name = each.value.source_name
  }
}

resource "google_pubsub_subscription" "subscr_raw" {
  for_each = var.sources
  project  = var.project
  name     = "${var.raw_prefix}-${var.client_id}-${each.value.source_name}-${each.value.schema_version}"
  topic    = "${var.client_id}-${each.value.source_name}-${each.value.schema_version}"

  bigquery_config {
    table               = "${var.project}:${var.raw_prefix}_${var.dataset_id}.${var.raw_prefix}_${var.tables[each.value.source_name].table_id}"
    use_topic_schema    = false
    write_metadata      = true
    drop_unknown_fields = false
  }

  expiration_policy {
    ttl = "" # Never expires
  }

  labels                  = var.labels
  enable_message_ordering = false

  depends_on = [
    module.google_pubsub,
    module.google_bigquery_raw
  ]
}
