resource "google_compute_firewall" "firewall" {
  name    = var.name
  network = var.network

  allow {
    protocol = var.protocol
    ports    = var.ports
  }

  target_tags   = ["${var.network}-${var.name}"]
  source_ranges = var.source_ranges

}

