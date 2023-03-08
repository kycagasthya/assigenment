
variable "project_id" {
  description = "The GCP project ID."
  type        = string
}
variable "region" {
  description = "Region where the resource is created"
  type        = string
}

variable "network_name" {
  description = "The name of the network being created"
  type        = string
}
variable "subnetwork_name" {
  description = "The subnetwork name where cloudsql proxy is provisioned"
  type        = string
}

variable "terraform_sa_email" {
  description = "Terraform service account email id."
  type        = string
}

variable "sql_instance_name" {
  description = "The name for Cloud SQL instance"
  type        = string
}

variable "random_instance_name" {
  description = "Sets random suffix at the end of the Cloud SQL resource name"
  type        = bool
}

variable "enable_default_user" {
  description = "Enable or disable the creation of the default user"
  type        = bool
}


variable "enable_default_db" {
  description = "Enable or disable the creation of the default database"
  type        = bool
}

variable "user_labels" {
  description = "The key/value labels for the sql instances."
  type        = map(string)
}

variable "deletion_protection" {
  description = "Used to block Terraform from deleting a SQL Instance."
  type        = bool
}

variable "database_version" {
  description = "The database version to use for cloud sql instance"
  type        = string
}

variable "zone" {
  description = "The zone for the master instance."
  type        = string
}

variable "tier" {
  description = "The tier for the master instance."
  type        = string
}

variable "ip_configuration" {
  description = "The ip_configuration settings subblock"
  type = object({
    authorized_networks = list(map(string))
    ipv4_enabled        = bool
    private_network     = string
    require_ssl         = bool
  })
}

variable "availability_type" {
  description = "The availability type for the master instance."
  type        = string
}

variable "backup_configuration" {
  description = "The backup_configuration settings subblock for the database setings"
  type = object({
    binary_log_enabled             = bool
    enabled                        = bool
    start_time                     = string
    location                       = string
    transaction_log_retention_days = string
    retained_backups               = number
    retention_unit                 = string
  })
}

variable "disk_autoresize" {
  description = "Configuration to increase storage size"
  type        = bool
}

variable "disk_size" {
  description = "The disk size for the master instance"
  type        = number
}

variable "sql_disk_type" {
  description = "The disk type for the master instance."
  type        = string
}

variable "maintenance_window_day" {
  description = "The day of week (1-7) for the master instance maintenance."
  type        = number
}

variable "maintenance_window_hour" {
  description = "The hour of day (0-23) maintenance window for the master instance maintenance."
  type        = number
}

variable "maintenance_window_update_track" {
  description = "The update track of maintenance window for the master instance maintenance."
  type        = string
}

variable "storage_bucket_labels" {
  description = "A map of key/value label pairs to assign to the logsinks GCS bucket."
  type        = map(string)
}

variable "cloudsql_bin_path" {
  description = "CloudSQL Binary local path"
  type        = string
}

variable "machine_type" {
  description = "Machine type to create."
  type        = string
}

variable "instance_tmplt_prefix" {
  description = "Name prefix for the instance template"
  type        = string
}

variable "source_image_project" {
  description = "Project where the source image comes from"
  type        = string
}

variable "source_image" {
  description = "Source disk image"
  type        = string
}

variable "source_image_family" {
  description = "Source image family"
  type        = string
}

variable "disk_labels" {
  description = "Labels to be assigned to boot disk, provided as a map"
  type        = map(string)
}

variable "disk_size_gb" {
  description = "Boot disk size in GB"
  type        = string
}

variable "instance_template_disk_type" {
  description = "Boot disk type, can be either pd-ssd, local-ssd, or pd-standard"
  type        = string
}

variable "enable_shielded_vm" {
  description = "Whether to enable shielded vm or not"
  type        = bool
}

variable "mig_labels" {
  description = "Managed instance group labels"
  type        = map(string)
}

variable "inst_tmplt_tags" {
  description = "Tags assigned to managed instance templates"
  type        = list(string)
}

variable "mig_name" {
  description = "Managed instance group name."
  type        = string
}

variable "hostname_prefix" {
  description = "Host name prefix."
  type        = string
}


variable "target_size" {
  description = "The target number of running instances for this managed instance group"
  type        = number
}


variable "mig_hc_name" {
  description = "Name for MIG Healthcheck resource"
  type        = string
}

variable "mig_health_check" {
  description = "MIG Health check to determine whether instances are responsive and able to do work"
  type = object({
    type                = string
    initial_delay_sec   = number
    check_interval_sec  = number
    healthy_threshold   = number
    timeout_sec         = number
    unhealthy_threshold = number
    response            = string
    proxy_header        = string
    port                = number
    request             = string
    request_path        = string
    host                = string
  })
}

variable "distribution_policy_zones" {
  description = "The zones instances are created in."
  type        = list(string)
}

variable "update_policy" {
  description = "The update policy for the managed instance group"
  type = list(object({
    max_surge_fixed              = number
    instance_redistribution_type = string
    max_surge_percent            = number
    max_unavailable_fixed        = number
    max_unavailable_percent      = number
    min_ready_sec                = number
    replacement_method           = string
    minimal_action               = string
    type                         = string
  }))
}

variable "health_check_name" {
  description = "Name for ILB Healthcheck resource"
  type        = string
}

variable "ilb_health_check" {
  description = "ILB Health check to determine whether instances are responsive and able to do work"
  type = object({
    check_interval_sec  = number
    healthy_threshold   = number
    timeout_sec         = number
    unhealthy_threshold = number
    response            = string
    port                = string
    proxy_header        = string
    request             = string
  })
}

variable "backend_name" {
  description = "Name for ILB Backend resource"
  type        = string
}
variable "connection_draining_timeout_sec" {
  description = "Time for which instance will be drained"
  type        = number
}

variable "frontend_name" {
  description = "Name for ILB Frontend resource"
  type        = string
}

variable "cloud_sql_ipv4_cidr" {
  description = "The CIDR block from which IP range in tenant project will be reserved for Cloud SQL."
  type        = string
}

variable "web_server_ipv4_cidr" {
  description = "The CIDR block from which IP range in tenant project will be reserved for the web server."
  type        = string
}

variable "orchestrator_gke_master_ip_range" {
  description = "The CIDR block from which IP range in tenant project will be reserved for the master."
  type        = string
}

variable "orchestrator_pod_range_name" {
  description = "The name of the cluster's secondary range used to allocate IP addresses to pods."
  type        = string
}

variable "orchestrator_svc_range_name" {
  type        = string
  description = "The name of the services' secondary range used to allocate IP addresses to the cluster."
}

variable "composer_env_name" {
  description = "Name of Cloud Composer Environment"
  type        = string
}

variable "orchestrator_network_name" {
  type        = string
  description = "The VPC network to host the composer cluster."
}

variable "orchestrator_subnetwork_name" {
  type        = string
  description = "The subnetwork to host the composer cluster."
}

variable "composer_disk_size" {
  description = "The disk size for nodes."
  type        = string
}

variable "composer_tags" {
  description = "Tags applied to all nodes. Tags are used to identify valid sources or targets for network firewalls."
  type        = list(string)
}

variable "composer_labels" {
  type        = map(string)
  description = "The resource labels (a map of key/value pairs) to be applied to the Cloud Composer."
}

variable "node_count" {
  description = "Number of worker nodes in Cloud Composer Environment."
  type        = number
}

variable "composer_machine_type" {
  description = "Machine type of Cloud Composer nodes."
  type        = string
}

variable "python_version" {
  description = "The default version of Python used to run the Airflow scheduler, worker, and webserver processes."
  type        = string
}

variable "image_version" {
  type        = string
  description = "The version of the aiflow running in the cloud composer environment."
}


variable "airflow_maint_instance_name" {
  description = "Airflow maitenance gce to manage cloud composer cluster."
  type        = string
}

variable "airflow_maint_labels" {
  description = "GCE Labels for Airflow maintenance server"
  type        = map(string)
}

variable "deploy_maint_gce" {
  description = "Boolean flag to provision or de-provision the Airflow maintenance server. Defaults to false"
  type        = bool
  default     = false
}

variable "airflow_config_overrides" {
  type        = map(string)
  description = "Airflow configuration properties to override. Property keys contain the section and property names, separated by a hyphen, for example \"core-dags_are_paused_at_creation\"."
}

variable "pypi_packages" {
  type        = map(string)
  description = " Custom Python Package Index (PyPI) packages to be installed in the environment. Keys refer to the lowercase package name (e.g. \"numpy\")."
}

variable "env_variables" {
  type        = map(string)
  description = "Variables of the airflow environment."
  default     = {}
}
