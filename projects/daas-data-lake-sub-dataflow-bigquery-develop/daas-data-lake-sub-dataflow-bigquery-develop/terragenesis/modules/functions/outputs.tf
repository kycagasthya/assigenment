# output "function_url" {
#   value = google_cloudfunctions_function.function.https_trigger_url
# }
output "function2_url" {
  value = google_cloudfunctions2_function.function.service_config[0].uri
}
