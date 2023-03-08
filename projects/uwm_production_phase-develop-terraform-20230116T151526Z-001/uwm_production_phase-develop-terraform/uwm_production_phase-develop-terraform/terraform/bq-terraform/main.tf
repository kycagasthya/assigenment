 module "bigquery" {
  source  = "terraform-google-modules/bigquery/google"
  version = "~> 4.4"
 
  dataset_id                  = "sample_pch_ds"
  dataset_name                = "sample_pch_ds"
  description                 = "Sample PCH dataset description"
  project_id                  = var.project_id
  location                    = "US"
  default_table_expiration_ms = 3600000
  tables = [
    {
      table_id = "classification",
      schema   = "./classification.json",
      time_partitioning = {
        type                     = "DAY",
        field                    = null,
        require_partition_filter = false,
        expiration_ms            = null,
      },
      expiration_time = null,
      clustering      = []
      labels = {
        env      = "dev"
        billable = "true"
      },
    },
    {
      table_id = "entity_extraction",
      schema   = "./entity_extraction.json",
      time_partitioning = {
        type                     = "DAY",
        field                    = null,
        require_partition_filter = false,
        expiration_ms            = null,
      },
      expiration_time = null,
      clustering      = []
      labels = {
        env      = "dev"
        billable = "true"
      },
    },
  ]
  dataset_labels = {
    env      = "dev"
    billable = "true"
  }
}
