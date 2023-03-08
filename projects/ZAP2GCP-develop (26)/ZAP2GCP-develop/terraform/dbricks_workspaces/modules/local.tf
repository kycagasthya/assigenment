locals {
  network_name_ref  = data.google_compute_network.vpc_network.name
  network_self_link = data.google_compute_network.vpc_network.self_link
}
