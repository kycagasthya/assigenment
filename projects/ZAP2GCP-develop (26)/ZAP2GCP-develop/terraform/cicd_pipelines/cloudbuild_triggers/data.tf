
data "google_storage_bucket" "dev_data_engg_pipeline" {
  name = "its-managed-dbx-zap-d-pipeline-code"
}

data "google_storage_bucket" "test_data_engg_pipeline" {
  name = "its-managed-dbx-de-01-t-pipeline-code"
}

data "google_storage_bucket" "dev_cc_bucket" {
  name = "us-central1-cmpr-zapdbx-usc-157ef630-bucket"
}




