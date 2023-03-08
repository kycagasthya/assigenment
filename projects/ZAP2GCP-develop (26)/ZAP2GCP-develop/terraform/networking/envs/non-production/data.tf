data "google_compute_network" "dbx_vpc_network" {
  project = var.dbx_project_id
  name    = var.dbx_network_name
}

data "google_compute_network" "dbx_ds_vpc_network" {
  project = var.dbx_ds_project_id
  name    = var.dbx_ds_network_name
}

data "google_compute_network" "dbx_test_vpc_network" {
  project = var.dbx_test_project_id
  name    = var.dbx_test_network_name
}

data "google_compute_network" "dbx_mktg_vpc_network" {
  project = var.dbx_mktg_project_id
  name    = var.dbx_mktg_network_name
}

data "google_compute_network" "dbx_mktg_t_vpc_network" {
  project = var.dbx_mktg_t_project_id
  name    = var.dbx_mktg_t_network_name
}


data "google_compute_network" "dbx_ds_t_vpc_network" {
  project = var.dbx_ds_t_project_id
  name    = var.dbx_ds_t_network_name
}