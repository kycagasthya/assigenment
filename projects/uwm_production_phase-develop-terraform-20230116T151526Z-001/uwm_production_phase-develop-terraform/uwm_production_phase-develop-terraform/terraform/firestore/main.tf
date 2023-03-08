resource "google_firestore_document" "classification" {
  project     = var.project_id
  collection  = "classification"
  document_id = "collection"
  fields      = "{\"something\":{\"mapValue\":{\"fields\":{\"akey\":{\"stringValue\":\"avalue\"}}}}}"
}
resource "google_firestore_document" "entity-extraction" {
  project     = var.project_id
  collection  = "entityextraction"
  document_id = "collection"
  fields      = "{\"something\":{\"mapValue\":{\"fields\":{\"akey\":{\"stringValue\":\"avalue\"}}}}}"
  }