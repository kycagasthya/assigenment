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
    },
    {
      name              = "route-to-databricks-controlplane"
      description       = "Route to Databricks Control Plane"
      destination_range = var.db_control_plane_nat_ip_rt
      priority          = "1000"
      next_hop_internet = "true"
    },
    {
      name              = "route-to-databricks-npip-service"
      description       = "Route to Databricks NPIP Service"
      destination_range = var.db_control_plane_npip_ip_rt
      priority          = "1000"
      next_hop_internet = "true"
    },
    {
      name              = "route-to-databricks-managed-hive"
      description       = "Route to Databricks Managed Hive IP"
      destination_range = var.db_managed_hive_rt
      priority          = "1000"
      next_hop_internet = "true"
    },
    {
      name              = "route-to-databricks-workspace"
      description       = "Route to Databricks Workspace URL"
      destination_range = var.db_workspace_url_rt
      priority          = "1000"
      next_hop_internet = "true"
    }

  ]
}