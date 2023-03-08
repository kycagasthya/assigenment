output "service_account" {
  description = "Service account resource."
  value       = google_service_account.service_account
}

output "email" {
  description = "Service account email."
  value       = google_service_account.service_account.email
}
