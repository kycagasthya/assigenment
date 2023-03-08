
variable "project_id" {
  description = "The ID of the project where the hive metastore vpc will be created"
  type        = string
}

variable "description" {
  description = "Description of the VPC Network."
  type        = string
}

variable "region" {
  description = "GCP Region."
  type        = string
}

variable "cidr_allow_sql_ingress" {
  description = "The cidr range for allow sql ingresss"
  type        = list(string)
}

variable "network_name" {
  description = "The name of the network being created"
  type        = string
}

variable "subnets" {
  type        = list(map(string))
  description = "The list of subnets being created"
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

variable "orchestrator_network_name" {
  description = "The name of the network being created"
  type        = string
}

variable "orchestrator_description" {
  description = "An optional description of this resource. The resource must be recreated to modify this field."
  type        = string
}

variable "orchestrator_subnets" {
  type        = list(map(string))
  description = "The list of subnets being created"
}

variable "orchestrator_secondary_ranges" {
  type        = map(list(object({ range_name = string, ip_cidr_range = string })))
  description = "Secondary ranges that will be used in some of the subnets"
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


















