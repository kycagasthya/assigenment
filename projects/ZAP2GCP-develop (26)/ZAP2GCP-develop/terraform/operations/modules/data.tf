
# Required to fetch network
data "google_compute_network" "cloudsql_proxy_net" {
  project = var.project_id
  name    = var.network_name
}

# Required to fetch subnetwork
data "google_compute_subnetwork" "proxy_mig_subnet" {
  project = var.project_id
  name    = var.subnetwork_name
  region  = var.region
}
