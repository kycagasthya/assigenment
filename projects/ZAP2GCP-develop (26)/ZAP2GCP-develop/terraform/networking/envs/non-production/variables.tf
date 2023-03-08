variable "project_id" {
  description = "The ID of the project where the hive metastore vpc will be created"
  type        = string
}

variable "region" {
  description = "GCP Region for the resource provisioning"
  type        = string
}

variable "dbx_project_id" {
  description = "The Databricks project id."
  type        = string
}

variable "dbx_network_name" {
  description = "The name of the Databricks network"
  type        = string
}

variable "dbx_ds_project_id" {
  description = "The Databricks project id for Data Science."
  type        = string
}

variable "dbx_ds_t_project_id" {
  description = "The Databricks project id."
  type        = string
}

variable "dbx_ds_t_network_name" {
  description = "The name of the Databricks network"
  type        = string
}



variable "terraform_sa_email" {
  description = "Terraform service account email id."
  type        = string
}
variable "network_name" {
  description = "The name of the network being created"
  type        = string
}

variable "dbx_ds_network_name" {
  description = "The name of the network used for DS"
  type        = string
}

variable "dbx_test_project_id" {
  description = "The Databricks project id for Test Data Engineering"
  type        = string
}

variable "dbx_test_network_name" {
  description = "The name of the network used for Test Data Engineering"
  type        = string
}

variable "dbx_mktg_project_id" {
  description = "The Databricks project id for Test Data Engineering"
  type        = string
}

variable "dbx_mktg_network_name" {
  description = "The name of the network used for Test Data Engineering"
  type        = string
}

variable "dbx_mktg_t_project_id" {
  description = "The Databricks project id for Test Data Engineering"
  type        = string
}

variable "dbx_mktg_t_network_name" {
  description = "The name of the network used for Test Data Engineering"
  type        = string
}

variable "proxy_subnet_name" {
  description = "Subnet name of cloud proxy"
  type        = string
}

variable "proxy_cidr_range" {
  description = "IP range to allocate to CLoud proxy instances"
  type        = string
}


variable "psa_labels" {
  description = "The key/value labels for the IP range allocated to the peered network."
  type        = map(string)
}

variable "psa_address" {
  description = "First IP address of the IP range to allocate to CLoud SQL instances and other Private Service Access services. If not set, GCP will pick a valid one for you."
  type        = string
}

variable "psa_net_prefix" {
  description = "Prefix length of the IP range reserved for Cloud SQL instances and other Private Service Access services. Defaults to /16."
  type        = number
}


variable "cidr_allow_sql_ingress" {
  type        = list(string)
  description = "The cidr range for allow sql ingresss"
}

variable "peer_prefix" {
  description = "Name prefix for the network peerings"
  type        = string
}
variable "peer_prefix_ds" {
  description = "Name prefix for the network peerings"
  type        = string
}

variable "peer_prefix_test" {
  description = "Name prefix for the network peerings"
  type        = string
}
variable "peer_prefix_mktg" {
  description = "Name prefix for the network peerings"
  type        = string
}

variable "peer_prefix_t_mktg" {
  description = "Name prefix for the network peerings"
  type        = string
}

variable "peer_prefix_t_ds" {
  description = "Name prefix for the network peerings"
  type        = string
}

variable "orchestrator_network_name" {
  description = "The name of the network being created"
  type        = string
}

variable "orchestrator_description" {
  description = "An optional description of this resource. The resource must be recreated to modify this field."
  type        = string
}

variable "composer_subnet_name" {
  description = "Cloud composer subnet name"
  type        = string
}

variable "composer_subnet_ip" {
  description = "Composer subnet ip ."
  type        = string
}


variable "nat_bgp_asn" {
  description = "ASN number for nat router"
  type        = string
}

variable "cc_gke_master_subnet" {
  type        = list(string)
  description = "GKE master size ip"
}

variable "cc_gke_node_subnet" {
  type        = list(string)
  description = "GKE nodes subnet ip"
}

variable "cc_gke_pods_subnet" {
  type        = list(string)
  description = "GKE pods subnet size"
}

variable "cc_gke_service_subnet" {
  type        = list(string)
  description = "GKE services subnet size"
}




