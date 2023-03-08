project_id         = "its-managed-dbx-zap-d"
terraform_sa_email = "quantiphi-terraform-dev@za-global-service-accounts-p.iam.gserviceaccount.com"

dbx_network_name = "databricks-managed-1235921161438059"

db_gke_master_ip      = ["100.120.0.0/28"] # We need to fetch this IP address after the workspace is created
db_gke_node_subnet    = ["10.176.6.0/23"]
db_gke_pods_subnet    = ["100.80.0.0/19"] # We need to fetch this Subnet Range after the workspace is created
db_gke_service_subnet = ["100.66.0.0/25"] # We need to fetch this Subnet Range after the workspace is created

db_control_plane_nat_ip  = ["34.123.97.237/32"]  # Control Plane NAT IP for us-central1 region
db_control_plane_npip_ip = ["35.224.199.248/32"] # Control Plane NPIP IP for us-central1 region
db_workspace_url         = ["34.72.196.197/32"]  # Databricks Workspace URL
db_managed_hive          = ["35.239.64.150/32"]  # Databricks Managed Hive Metastore IP for us-central1 region
db_endpoint_ip           = ["35.223.57.48/32"]

db_control_plane_nat_ip_rt  = "34.123.97.237/32"  # Control Plane NAT IP for us-central1 region
db_control_plane_npip_ip_rt = "35.224.199.248/32" # Control Plane NPIP IP for us-central1 region
db_workspace_url_rt         = "34.72.196.197/32"  # Databricks Workspace URL
db_managed_hive_rt          = "35.239.64.150/32"  # Databricks Managed Hive Metastore IP for us-central1 region

hive_sql_cidr_range = ["10.176.11.80/28"]

storage_bucket_labels = {
  bu_owner_manager        = ""
  bu_owner_technical      = ""
  cost_center             = ""
  project_or_product      = ""
  security_agent_exempt   = ""
  tier                    = ""
  os_hostname             = ""
  access_privileges       = ""
  security_classification = ""
  backup                  = ""
  organization            = ""
}
