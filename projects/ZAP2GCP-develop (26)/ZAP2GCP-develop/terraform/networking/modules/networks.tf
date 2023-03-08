/******************************************
  Hive Metastore VPC Networks
*****************************************/

module "hive_metastore_vpc" {
  source = "github.com/terraform-google-modules/terraform-google-network?ref=v3.4.0"

  project_id              = var.project_id
  network_name            = var.network_name
  description             = var.description
  routing_mode            = "GLOBAL"
  auto_create_subnetworks = false

  subnets = var.subnets
}

/********************************************
  Private Service Access for Hive Metastore
*******************************************/

module "private_service_access" {
  source = "github.com/terraform-google-modules/terraform-google-sql-db//modules/private_service_access?ref=v7.1.0"

  project_id  = var.project_id
  vpc_network = local.network_name_ref
  labels      = var.psa_labels

  address       = var.psa_address
  prefix_length = var.psa_net_prefix

  depends_on = [
    module.hive_metastore_vpc
  ]
}



/**********************************************
 Hive Metastore NAT Cloud Router & NAT config
 *********************************************/

resource "google_compute_router" "hive_nat_router" {
  name    = "cr-hive-vpc-nat-router"
  project = var.project_id
  region  = var.region
  network = module.hive_metastore_vpc.network_self_link

  bgp {
    asn = var.nat_bgp_asn
  }
}

resource "google_compute_address" "hive_nat_external_addresses" {
  project = var.project_id
  name    = "ca-hive-vpc-nat"
  region  = var.region
}

resource "google_compute_router_nat" "hive_egress_nat" {
  name                   = "rn-hive-vpc-egress"
  project                = var.project_id
  router                 = google_compute_router.hive_nat_router.name
  region                 = var.region
  nat_ip_allocate_option = "MANUAL_ONLY"
  nat_ips                = [google_compute_address.hive_nat_external_addresses.self_link]

  source_subnetwork_ip_ranges_to_nat = "LIST_OF_SUBNETWORKS"
  subnetwork {
    name                    = module.hive_metastore_vpc.subnets_self_links[0]
    source_ip_ranges_to_nat = ["ALL_IP_RANGES"]
  }

  log_config {
    filter = "TRANSLATIONS_ONLY"
    enable = true
  }

  depends_on = [
    module.hive_metastore_vpc
  ]
}

/******************************************
  Orchestrator VPC Network
*****************************************/
module "orchestrator_vpc" {
  source = "github.com/terraform-google-modules/terraform-google-network?ref=v3.4.0"

  project_id              = var.project_id
  network_name            = var.orchestrator_network_name
  description             = var.orchestrator_description
  routing_mode            = "GLOBAL"
  auto_create_subnetworks = false

  subnets          = var.orchestrator_subnets
  secondary_ranges = var.orchestrator_secondary_ranges
}



/********************************************
  Orchestrator NAT Cloud Router & NAT config
 *******************************************/

resource "google_compute_router" "nat_router" {
  name    = "cr-orch-vpc-nat-router"
  project = var.project_id
  region  = var.region
  network = module.orchestrator_vpc.network_self_link

  bgp {
    asn = var.nat_bgp_asn
  }
}

resource "google_compute_address" "nat_external_addresses" {
  project = var.project_id
  name    = "ca-orch-vpc-nat"
  region  = var.region
}

resource "google_compute_router_nat" "egress_nat" {
  name                   = "rn-orch-vpc-egress"
  project                = var.project_id
  router                 = google_compute_router.nat_router.name
  region                 = var.region
  nat_ip_allocate_option = "MANUAL_ONLY"
  nat_ips                = [google_compute_address.nat_external_addresses.self_link]

  source_subnetwork_ip_ranges_to_nat = "LIST_OF_SUBNETWORKS"
  subnetwork {
    name                    = module.orchestrator_vpc.subnets_self_links[0]
    source_ip_ranges_to_nat = ["ALL_IP_RANGES"]
  }

  log_config {
    filter = "TRANSLATIONS_ONLY"
    enable = true
  }

  depends_on = [
    module.orchestrator_vpc
  ]
}

