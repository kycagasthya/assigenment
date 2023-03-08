output "firestore_name" {
  description = "firestore collection name"
  value       = google_firestore_document.firestore_document.collection
}

