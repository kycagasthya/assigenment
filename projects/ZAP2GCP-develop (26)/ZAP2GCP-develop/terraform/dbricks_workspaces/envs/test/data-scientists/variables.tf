variable "project_id" {
  description = "GCP test Databricks workspace Project ID."
  type        = string
}

variable "test_project_id" {
  description = "test Data Engineering Project ID"
  type        = string
}

variable "terraform_sa_email" {
  description = "Terraform service account email id."
  type        = string
}

variable "storage_bucket_labels" {
  description = "A map of key/value label pairs to assign to the logsinks GCS bucket."
  type        = map(string)
}

variable "db_gke_master_ip" {
  description = "Master IP address of the GKE cluster"
  type        = list(string)
}

variable "db_gke_node_subnet" {
  description = "Node Subnet range of the GKE cluster"
  type        = list(string)
}

variable "db_gke_pods_subnet" {
  description = "Pods Subnet range of the GKE cluster"
  type        = list(string)
}

variable "db_gke_service_subnet" {
  description = "Service Subnet range of the GKE cluster"
  type        = list(string)
}

variable "db_control_plane_nat_ip" {
  description = "Databricks Control NAT IP based on region (us_central1)"
  type        = list(string)

}
variable "db_control_plane_npip_ip" {
  description = "Databricks Control NPIP IP based on region (us_central1)"
  type        = list(string)

}

variable "db_endpoint_ip" {
  description = "Databricks Endpoint IP"
  type        = list(string)
}

variable "db_workspace_url" {
  description = "Databricks Workspace URL based on region (us_central1)"
  type        = list(string)

}

variable "db_managed_hive" {
  description = "Databricks Managed Hive IP based on region (us_central1)"
  type        = list(string)

}
variable "db_control_plane_nat_ip_rt" {
  description = "Databricks Control NAT IP based on region (us_central1)"
  type        = string

}
variable "db_control_plane_npip_ip_rt" {
  description = "Databricks Control NPIP IP based on region (us_central1)"
  type        = string

}

variable "db_workspace_url_rt" {
  description = "Databricks Workspace URL based on region (us_central1)"
  type        = string

}

variable "db_managed_hive_rt" {
  description = "Databricks Managed Hive IP based on region (us_central1)"
  type        = string

}

variable "dbx_network_name" {
  description = "Databricks Network Name."
  type        = string
}

variable "hive_sql_cidr_range" {
  description = "CloudSql proxy subnetwork CIDR range for Centralized Hive."
  type        = list(string)
}