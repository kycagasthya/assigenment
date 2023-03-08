
module "routes" {
  source = "github.com/terraform-google-modules/terraform-google-network//modules/routes?ref=v3.4.0"

  project_id   = var.project_id
  network_name = local.network_name_ref

  routes = [
    {
      name              = "route-to-google-apis"
      description       = "Route to Google restricted APIs"
      destination_range = "199.36.153.4/30"
      priority          = "1000"
      next_hop_internet = "true"
    }
  ]
}

module "orchestrator_routes" {
  source = "github.com/terraform-google-modules/terraform-google-network//modules/routes?ref=v3.4.0"

  project_id   = var.project_id
  network_name = local.orchestrator_network_name_ref

  routes = [
    {
      name              = "orch-route-to-google-apis"
      description       = "Route to Google restricted APIs"
      destination_range = "199.36.153.4/30"
      priority          = "1000"
      next_hop_internet = "true"
    }
  ]
}