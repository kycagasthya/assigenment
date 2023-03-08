data "google_compute_network" "vpc_network" {
  project = var.project_id
  name    = var.dbx_network_name
}