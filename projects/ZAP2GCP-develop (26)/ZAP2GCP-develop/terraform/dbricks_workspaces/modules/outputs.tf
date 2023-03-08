output "fw_egress_allow_rules" {
  value       = module.firewalls.custom_egress_allow_rules
  description = "Custom egress rules with allow blocks"
}

output "fw_egress_deny_rules" {
  value       = module.firewalls.custom_egress_deny_rules
  description = "Custom egress rules with allow blocks"
}

output "fw_ingress_allow_rules" {
  value       = module.firewalls.custom_ingress_allow_rules
  description = "Custom ingress rules with allow blocks"
}

output "routes" {
  value       = module.routes
  description = "The created routes resources for databricks"
}

output "dns_zone_googleapi_domain" {
  value       = module.dns-private-zone-google-apis.domain
  description = "The DNS zone domain for restricted google apis"
}

output "dns_zone_gcr_domain" {
  value       = module.dns-private-zone-google-gcr.domain
  description = "The DNS zone domain for gcr"
}