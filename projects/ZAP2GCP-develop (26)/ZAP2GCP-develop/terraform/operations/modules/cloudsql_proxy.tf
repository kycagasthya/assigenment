/******************************************************
 Service Account and IAM Binding
******************************************************/

resource "google_service_account" "cloudsql_proxy_mig" {
  project      = var.project_id
  account_id   = "sa-cloudsql-proxy"
  display_name = "CloudSql proxy mig instances Service Account"
}
resource "google_project_iam_member" "log_writer" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.cloudsql_proxy_mig.email}"
}

resource "google_service_account_iam_member" "tf_sa_access" {
  service_account_id = google_service_account.cloudsql_proxy_mig.name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${var.terraform_sa_email}"
}

resource "google_project_iam_member" "cloudsql_client" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.cloudsql_proxy_mig.email}"
}

resource "google_project_iam_member" "metric_writer" {
  project = var.project_id
  role    = "roles/monitoring.metricWriter"
  member  = "serviceAccount:${google_service_account.cloudsql_proxy_mig.email}"
}

resource "google_project_iam_member" "storage_object_viewer" {
  project = var.project_id
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${google_service_account.cloudsql_proxy_mig.email}"
}

/******************************************************
  Storage buckets and startup scripts
******************************************************/

module "sql_proxy_bucket" {
  source        = "github.com/terraform-google-modules/cloud-foundation-fabric//modules/gcs?ref=v5.1.0"
  project_id    = var.project_id
  name          = "${var.project_id}-np-proxy-bucket"
  storage_class = "REGIONAL"
  location      = "us-central1"
  versioning    = false
  force_destroy = false
  labels        = var.storage_bucket_labels
}

resource "google_storage_bucket_object" "gcs_proxy_object" {
  name   = "cloud_sql_proxy"
  source = var.cloudsql_bin_path
  bucket = module.sql_proxy_bucket.name
}

data "template_file" "mig_startup_script" {
  template = file("${path.module}/mig_startup_script.tpl")

  vars = {
    bucket_name          = module.sql_proxy_bucket.name
    cloudsql_conn_string = module.hive_metastore_cloudsql.instance_connection_name
  }
}

/******************************************************
  CloudSQL Proxy Instance Template
******************************************************/

module "proxy_instance_template" {
  source = "github.com/terraform-google-modules/terraform-google-vm//modules/instance_template?ref=v7.1.0"

  project_id           = var.project_id
  region               = var.region
  name_prefix          = var.instance_tmplt_prefix
  subnetwork           = var.subnetwork_name
  subnetwork_project   = var.project_id
  machine_type         = var.machine_type
  source_image_project = var.source_image_project
  source_image         = var.source_image
  source_image_family  = var.source_image_family
  disk_labels          = var.disk_labels
  disk_size_gb         = var.disk_size_gb
  disk_type            = var.instance_template_disk_type
  enable_shielded_vm   = var.enable_shielded_vm
  labels               = var.mig_labels
  tags                 = var.inst_tmplt_tags
  startup_script       = data.template_file.mig_startup_script.rendered
  auto_delete          = "true"
  service_account = {
    email = google_service_account.cloudsql_proxy_mig.email
    scopes = [
      "sql-admin",
      "storage-ro",
      "logging-write",
      "monitoring-write"
    ]
  }
}

/******************************************************
  CloudSQL Proxy MIG
******************************************************/

module "proxy_managed_instance_group" {
  source = "github.com/terraform-google-modules/terraform-google-vm//modules/mig?ref=v7.1.0"

  project_id                = var.project_id
  region                    = var.region
  hostname                  = var.hostname_prefix
  mig_name                  = var.mig_name
  target_size               = var.target_size
  health_check_name         = var.mig_hc_name
  health_check              = var.mig_health_check
  distribution_policy_zones = var.distribution_policy_zones
  instance_template         = module.proxy_instance_template.self_link
  named_ports = [{
    name = "port-sql-proxy"
    port = 3306
  }]
  update_policy = var.update_policy
  depends_on = [
    google_storage_bucket_object.gcs_proxy_object
  ]
}

/******************************************************
  CloudSQL Proxy TCP ILB
******************************************************/


# Health check
resource "google_compute_health_check" "hc_cloudsql_proxy" {
  project             = var.project_id
  name                = var.health_check_name
  description         = "Healthcheck fot TCP ILB CloudSQL Proxy service"
  timeout_sec         = var.ilb_health_check["timeout_sec"]
  check_interval_sec  = var.ilb_health_check["check_interval_sec"]
  healthy_threshold   = var.ilb_health_check["healthy_threshold"]
  unhealthy_threshold = var.ilb_health_check["unhealthy_threshold"]

  tcp_health_check {
    request      = var.ilb_health_check["request"]
    response     = var.ilb_health_check["response"]
    port         = var.ilb_health_check["port"]
    proxy_header = var.ilb_health_check["proxy_header"]
  }
}

# Backend
resource "google_compute_region_backend_service" "ilb_tcp_cloudsql" {
  project                         = var.project_id
  name                            = var.backend_name
  region                          = var.region
  description                     = "TCP ILB Backend CloudSQL Proxy service."
  protocol                        = "TCP"
  connection_draining_timeout_sec = var.connection_draining_timeout_sec
  session_affinity                = "NONE"
  backend {
    group       = module.proxy_managed_instance_group.instance_group
    description = "MIG CloudSQL Proxy Backend"
  }
  health_checks = [
    google_compute_health_check.hc_cloudsql_proxy.id
  ]
}

# Forwarding rule

resource "google_compute_forwarding_rule" "tcp_ilb_cloudsql" {
  project               = var.project_id
  name                  = var.frontend_name
  region                = var.region
  description           = "Internal TCP Load Balancer with global access."
  network               = data.google_compute_network.cloudsql_proxy_net.self_link
  subnetwork            = data.google_compute_subnetwork.proxy_mig_subnet.self_link
  allow_global_access   = true
  load_balancing_scheme = "INTERNAL"
  backend_service       = google_compute_region_backend_service.ilb_tcp_cloudsql.self_link
  ip_protocol           = "TCP"
  ports                 = [3306]
}
