locals {
  network_name_ref  = module.hive_metastore_vpc.network_name
  network_self_link = module.hive_metastore_vpc.network_self_link

  psa_ip_range = ["${var.psa_address}/${var.psa_net_prefix}"]

  orchestrator_network_name_ref  = module.orchestrator_vpc.network_name
  orchestrator_network_self_link = module.orchestrator_vpc.network_self_link
}