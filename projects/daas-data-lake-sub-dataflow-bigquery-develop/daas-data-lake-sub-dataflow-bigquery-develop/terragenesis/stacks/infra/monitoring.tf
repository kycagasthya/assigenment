resource "google_monitoring_custom_service" "datalake" {
  service_id   = "datalake-subscriber-service"
  display_name = "Datalake subscriber service"
}

resource "google_monitoring_notification_channel" "slack" {
  display_name = "Takeoff Slack"
  type         = "slack"
  labels = {
    channel_name = var.slack["notification_channel"]
  }
  sensitive_labels {
    auth_token = var.slack["auth_token"]
  }
  user_labels = {}

  lifecycle {
    create_before_destroy = true
  }
}

resource "google_monitoring_notification_channel" "opsgenie" {
  display_name = "Takeoff Opsgenie"
  type         = "webhook_tokenauth"
  labels = {
    url = "https://api.opsgenie.com/v1/json/googlestackdriver?apiKey=${var.opsgenie_token}"
  }
  user_labels = {}

  lifecycle {
    create_before_destroy = true
  }
}
