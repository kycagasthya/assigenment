/******************************************
  Non-Production Network
*****************************************/

module "np_operations_net" {
  source = "../../modules/"

  project_id   = var.project_id
  region       = var.region
  network_name = var.network_name
  description  = "Hive Metastore VPC to host centralized hive metastore for non-production environments"
  subnets = [
    {
      subnet_name           = var.proxy_subnet_name
      subnet_ip             = var.proxy_cidr_range
      subnet_region         = var.region
      subnet_private_access = true
      subnet_flow_logs      = true
      description           = "Subnetwork to host CloudSQL Proxy Instance Group and ILB."
    }
  ]

  psa_labels     = var.psa_labels
  psa_address    = var.psa_address
  psa_net_prefix = var.psa_net_prefix

  cidr_allow_sql_ingress = var.cidr_allow_sql_ingress

  # Orchestrator resources
  orchestrator_network_name = var.orchestrator_network_name
  orchestrator_description  = var.orchestrator_description
  orchestrator_subnets = [
    {
      subnet_name           = var.composer_subnet_name
      subnet_ip             = var.composer_subnet_ip
      subnet_region         = var.region
      subnet_private_access = true
      subnet_flow_logs      = true
      description           = "Subnetwork to host Cloud Composer."
    }
  ]


  orchestrator_secondary_ranges = {
    "${var.composer_subnet_name}" = [
      {
        range_name    = "pod-range"
        ip_cidr_range = "100.72.0.0/21"
      },
      {
        range_name    = "svc-range"
        ip_cidr_range = "100.64.0.0/27"
      },
    ]
  }

  nat_bgp_asn = var.nat_bgp_asn

  cc_gke_node_subnet    = var.cc_gke_node_subnet
  cc_gke_pods_subnet    = var.cc_gke_pods_subnet
  cc_gke_service_subnet = var.cc_gke_service_subnet
  cc_gke_master_subnet  = var.cc_gke_master_subnet
}

/******************************************
  VPC Peering
*****************************************/

module "peering" {
  source = "github.com/terraform-google-modules/terraform-google-network//modules/network-peering?ref=v3.4.0"

  prefix        = var.peer_prefix
  local_network = module.np_operations_net.network_self_link
  peer_network  = data.google_compute_network.dbx_vpc_network.self_link

  depends_on = [
    module.np_operations_net
  ]
}

/******************************************
  VPC Peering to Data Science WS
*****************************************/

module "peering_ds" {
  source = "github.com/terraform-google-modules/terraform-google-network//modules/network-peering?ref=v3.4.0"

  prefix        = var.peer_prefix_ds
  local_network = module.np_operations_net.network_self_link
  peer_network  = data.google_compute_network.dbx_ds_vpc_network.self_link

  depends_on = [
    module.np_operations_net
  ]
}
    
/******************************************
  VPC Peering to Marketing WS
*****************************************/

module "peering_mk_ws" {
  source = "github.com/terraform-google-modules/terraform-google-network//modules/network-peering?ref=v3.4.0"

  prefix        = var.peer_prefix_mktg
  local_network = module.np_operations_net.network_self_link
  peer_network  = data.google_compute_network.dbx_mktg_vpc_network.self_link

  depends_on = [
    module.np_operations_net
  ]
}
 /******************************************
  VPC Peering to Marketing test WS
*****************************************/

module "peering_t_mk_ws" {
  source = "github.com/terraform-google-modules/terraform-google-network//modules/network-peering?ref=v3.4.0"

  prefix        = var.peer_prefix_t_mktg
  local_network = module.np_operations_net.network_self_link
  peer_network  = data.google_compute_network.dbx_mktg_t_vpc_network.self_link

  depends_on = [
    module.np_operations_net
  ]
}

/******************************************
  VPC Peering to Data Science WS
*****************************************/

module "peering_test" {
  source = "github.com/terraform-google-modules/terraform-google-network//modules/network-peering?ref=v3.4.0"

  prefix        = var.peer_prefix_test
  local_network = module.np_operations_net.network_self_link
  peer_network  = data.google_compute_network.dbx_test_vpc_network.self_link

  depends_on = [
    module.np_operations_net
  ]
}

/******************************************
  VPC Peering to Data Science WS
*****************************************/

module "peering_ds_test" {
  source = "github.com/terraform-google-modules/terraform-google-network//modules/network-peering?ref=v3.4.0"

  prefix        = var.peer_prefix_t_ds
  local_network = module.np_operations_net.network_self_link
  peer_network  = data.google_compute_network.dbx_ds_t_vpc_network.self_link

  depends_on = [
    module.np_operations_net
  ]
}
