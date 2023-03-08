/******************************************************
  CloudSQL Instance
******************************************************/

module "hive_metastore_cloudsql" {
  source                          = "github.com/terraform-google-modules/terraform-google-sql-db//modules/mysql?ref=v7.1.0"
  name                            = var.sql_instance_name
  project_id                      = var.project_id
  random_instance_name            = var.random_instance_name
  enable_default_user             = var.enable_default_user
  enable_default_db               = var.enable_default_db
  user_labels                     = var.user_labels
  deletion_protection             = var.deletion_protection
  database_version                = var.database_version
  region                          = var.region
  zone                            = var.zone
  tier                            = var.tier
  ip_configuration                = var.ip_configuration
  availability_type               = var.availability_type
  backup_configuration            = var.backup_configuration
  disk_autoresize                 = var.disk_autoresize
  disk_size                       = var.disk_size
  disk_type                       = var.sql_disk_type
  maintenance_window_day          = var.maintenance_window_day
  maintenance_window_hour         = var.maintenance_window_hour
  maintenance_window_update_track = var.maintenance_window_update_track
}
