resource "google_compute_instance" "instance" {
  name         = var.instance_names
  machine_type = var.machine_type
  zone         = var.zone
  tags         = var.tags
  labels       = var.labels
  boot_disk {
    auto_delete = false
    initialize_params {
      size  = var.disk_size
      image = var.image_name
    }
  }
  deletion_protection = var.deletion_protection 
  allow_stopping_for_update = true

  network_interface {
    network    = var.vpc_network
    subnetwork = var.subnetwork
    network_ip = var.static_private_ip
    access_config {
      nat_ip = var.static_public_ip
    }
  }
  service_account {
    email = var.service_account
    scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
  }
}

