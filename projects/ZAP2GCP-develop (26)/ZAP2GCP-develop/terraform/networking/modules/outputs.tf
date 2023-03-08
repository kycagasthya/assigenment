output "network_name" {
  value       = module.hive_metastore_vpc.network_name
  description = "The name of the VPC being created"
}

output "network_self_link" {
  value       = module.hive_metastore_vpc.network_self_link
  description = "The URI of the VPC being created"
}

output "address" {
  value       = module.private_service_access.address
  description = "First IP of the reserved range."
}

output "google_compute_global_address_name" {
  value       = module.private_service_access.google_compute_global_address_name
  description = "URL of the reserved range."
}

output "custom_egress_allow_rules" {
  description = "Custom egress rules with allow blocks."
  value       = module.firewall_rules.custom_egress_allow_rules
}

output "custom_ingress_allow_rules" {
  description = "Custom ingress rules with allow blocks."
  value       = module.firewall_rules.custom_ingress_allow_rules
}

output "custom_egress_allow_rules_on_prem" {
  description = "Custom egress rules with allow blocks."
  value       = module.firewall_rules_on_prem.custom_egress_allow_rules
}

output "custom_ingress_allow_rules_on_prem" {
  description = "Custom ingress rules with allow blocks."
  value       = module.firewall_rules_on_prem.custom_ingress_allow_rules
}

output "orch_custom_egress_allow_rules" {
  description = "Custom egress rules with allow blocks for orchestrator firewalls."
  value       = module.orchestrator_firewall_rules.custom_egress_allow_rules
}

output "orch_custom_ingress_allow_rules" {
  description = "Custom ingress rules with allow blocks for orchestrator firewalls"
  value       = module.orchestrator_firewall_rules.custom_ingress_allow_rules
}

output "orch_network_name" {
  description = "The name of the Orchestrator VPC being created"
  value       = module.orchestrator_vpc.network_name
}

output "orch_network_self_link" {
  description = "The URI of the Orchestrator VPC being created"
  value       = module.orchestrator_vpc.network_self_link
}

