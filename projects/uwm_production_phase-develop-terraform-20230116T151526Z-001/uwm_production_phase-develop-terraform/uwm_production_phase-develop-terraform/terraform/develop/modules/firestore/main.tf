resource "google_firestore_document" "firestore_document" {
  project     = var.project_id
  collection  = var.collection
  document_id = var.document_id
  fields      = "{\"something\":{\"mapValue\":{\"fields\":{\"akey\":{\"stringValue\":\"avalue\"}}}}}"
}