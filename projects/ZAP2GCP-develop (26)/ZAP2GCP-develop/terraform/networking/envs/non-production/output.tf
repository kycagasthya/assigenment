output "network_name" {
  description = "The name of the VPC being created"
  value       = module.np_operations_net.network_name
}

output "network_self_link" {
  description = "The URI of the VPC being created"
  value       = module.np_operations_net.network_self_link
}

output "address" {
  description = "First IP of the reserved range."
  value       = module.np_operations_net.address
}

output "google_compute_global_address_name" {
  description = "URL of the reserved range."
  value       = module.np_operations_net.google_compute_global_address_name
}

output "custom_egress_allow_rules" {
  description = "Custom egress rules with allow blocks."
  value       = module.np_operations_net.custom_egress_allow_rules
}

output "custom_ingress_allow_rules" {
  description = "Custom ingress rules with allow blocks."
  value       = module.np_operations_net.custom_ingress_allow_rules
}

output "peer_network_peering" {
  description = "Peer network peering resource."
  value       = module.peering.peer_network_peering
}

output "peer_network_peering_ds" {
  description = "Peer network peering resource for DS."
  value       = module.peering_ds.peer_network_peering
}

output "orch_network_name" {
  description = "The name of the Orchestrator VPC being created"
  value       = module.np_operations_net.network_name
}

output "orch_network_self_link" {
  description = "The URI of the Orchestrator VPC being created"
  value       = module.np_operations_net.network_self_link
}


output "peer_network_peering_ds_test" {
  description = "Peer network peering resource for DS test."
  value       = module.peering_ds_test.peer_network_peering
}
