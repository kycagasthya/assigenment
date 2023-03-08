resource "google_storage_notification" "notification" {
  bucket         = var.bucket_name
  payload_format = "JSON_API_V1"
  topic          = var.topic_name
  event_types    = ["OBJECT_FINALIZE"]
}
