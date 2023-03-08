
module "np_operations" {
  source = "../../modules"

  project_id      = var.project_id
  region          = var.region
  network_name    = var.network_name
  subnetwork_name = var.subnetwork_name

  terraform_sa_email = var.terraform_sa_email

  sql_instance_name               = var.sql_instance_name
  random_instance_name            = var.random_instance_name
  enable_default_user             = var.enable_default_user
  enable_default_db               = var.enable_default_db
  user_labels                     = var.user_labels
  deletion_protection             = var.deletion_protection
  database_version                = var.database_version
  zone                            = var.zone
  tier                            = var.tier
  ip_configuration                = var.ip_configuration
  availability_type               = var.availability_type
  backup_configuration            = var.backup_configuration
  disk_autoresize                 = var.disk_autoresize
  disk_size                       = var.disk_size
  sql_disk_type                   = var.sql_disk_type
  maintenance_window_day          = var.maintenance_window_day
  maintenance_window_hour         = var.maintenance_window_hour
  maintenance_window_update_track = var.maintenance_window_update_track

  storage_bucket_labels = var.storage_bucket_labels

  instance_tmplt_prefix       = var.instance_tmplt_prefix
  enable_shielded_vm          = var.enable_shielded_vm
  machine_type                = var.machine_type
  disk_labels                 = var.disk_labels
  disk_size_gb                = var.disk_size_gb
  instance_template_disk_type = var.instance_template_disk_type
  source_image_project        = var.source_image_project
  source_image_family         = var.source_image_family
  source_image                = var.source_image
  mig_labels                  = var.mig_labels
  inst_tmplt_tags             = var.inst_tmplt_tags

  mig_name                        = var.mig_name
  hostname_prefix                 = var.hostname_prefix
  target_size                     = var.target_size
  distribution_policy_zones       = var.distribution_policy_zones
  update_policy                   = var.update_policy
  connection_draining_timeout_sec = var.connection_draining_timeout_sec
  frontend_name                   = var.frontend_name
  backend_name                    = var.backend_name
  health_check_name               = var.health_check_name

  ilb_health_check = var.ilb_health_check
  mig_health_check = var.mig_health_check
  mig_hc_name      = var.mig_hc_name

  cloudsql_bin_path = var.cloudsql_bin_path

  orchestrator_network_name    = var.orchestrator_network_name
  orchestrator_subnetwork_name = var.orchestrator_subnetwork_name

  cloud_sql_ipv4_cidr              = var.cloud_sql_ipv4_cidr
  orchestrator_gke_master_ip_range = var.orchestrator_gke_master_ip_range
  orchestrator_pod_range_name      = var.orchestrator_pod_range_name
  orchestrator_svc_range_name      = var.orchestrator_svc_range_name
  web_server_ipv4_cidr             = var.web_server_ipv4_cidr


  composer_env_name     = var.composer_env_name
  composer_labels       = var.composer_labels
  node_count            = var.node_count
  composer_machine_type = var.composer_machine_type
  composer_disk_size    = var.composer_disk_size
  composer_tags         = var.composer_tags
  python_version        = var.python_version
  image_version         = var.image_version

  deploy_maint_gce            = var.deploy_maint_gce
  airflow_maint_instance_name = var.airflow_maint_instance_name
  airflow_maint_labels        = var.airflow_maint_labels

  airflow_config_overrides = {
    secrets-backend                       = "airflow.providers.google.cloud.secrets.secret_manager.CloudSecretManagerBackend",
    secrets-backend_kwargs                = jsonencode({ "project_id" = "its-registry-it-kcl-p", "connections_prefix" = "zbr-sa-composer-conn", "variables_prefix" = "zbr-sa-composer-var", "sep" = "-" }),
    webserver-rbac_user_registration_role = "User"
  }
  pypi_packages = var.pypi_packages
  env_variables = var.env_variables

}
