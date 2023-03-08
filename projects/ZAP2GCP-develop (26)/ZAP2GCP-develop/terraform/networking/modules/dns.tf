module "dns-private-zone-google-apis" {
  source     = "github.com/terraform-google-modules/terraform-google-cloud-dns?ref=v3.0.0"
  project_id = var.project_id
  type       = "private"
  name       = "google-apis"
  domain     = "googleapis.com."

  private_visibility_config_networks = [local.network_self_link, local.orchestrator_network_self_link]

  recordsets = [
    {
      name    = "*"
      type    = "CNAME"
      ttl     = 300
      records = ["restricted.googleapis.com."]
    },
    {
      name    = "restricted"
      type    = "A"
      ttl     = 300
      records = ["199.36.153.4", "199.36.153.5", "199.36.153.6", "199.36.153.7"]
    }
  ]
}

module "dns-private-zone-google-gcr" {
  source     = "github.com/terraform-google-modules/terraform-google-cloud-dns?ref=v4.0.0"
  project_id = var.project_id
  type       = "private"
  name       = "gcr-io"
  domain     = "gcr.io."

  private_visibility_config_networks = [local.network_self_link, local.orchestrator_network_self_link]

  recordsets = [
    {
      name    = "*"
      type    = "CNAME"
      ttl     = 300
      records = ["gcr.io."]
    },
    {
      name    = ""
      type    = "A"
      ttl     = 300
      records = ["199.36.153.4", "199.36.153.5", "199.36.153.6", "199.36.153.7"]
    }
  ]
}