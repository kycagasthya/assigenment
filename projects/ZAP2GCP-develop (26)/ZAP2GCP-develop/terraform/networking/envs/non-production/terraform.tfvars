terraform_sa_email = "quantiphi-terraform-dev@za-global-service-accounts-p.iam.gserviceaccount.com"

project_id     = "its-managed-dbx-edlops-t"
dbx_project_id = "its-managed-dbx-zap-d"
region         = "us-central1"

dbx_network_name  = "databricks-managed-1235921161438059"
network_name      = "vpc-np-hive-metastore"
proxy_subnet_name = "sb-np-hive-metastore-proxy"
proxy_cidr_range  = "10.176.11.80/28"

dbx_ds_project_id   = "its-managed-dbx-ds-01-d"
dbx_ds_network_name = "databricks-managed-2945417879364985"

dbx_ds_t_project_id   = "its-managed-dbx-ds-01-t"
dbx_ds_t_network_name = "databricks-managed-2348922014507522"

dbx_test_project_id   = "its-managed-dbx-de-01-t"
dbx_test_network_name = "databricks-managed-188879976212547"

dbx_mktg_project_id   = "its-managed-dbx-mktg-01-d"
dbx_mktg_network_name = "databricks-managed-389646803545106"

dbx_mktg_t_project_id   = "its-managed-dbx-mktg-01-t"
dbx_mktg_t_network_name = "databricks-managed-436375686858014"



psa_labels = {
  env = "non-prod"
}
psa_net_prefix         = "24"
psa_address            = "10.176.13.0"
cidr_allow_sql_ingress = ["100.120.0.0/28", "10.176.6.0/23", "100.80.0.0/19", "100.66.0.0/25", "100.120.0.48/28", "10.176.8.0/24", "100.76.0.0/20", "100.65.0.0/26", "100.120.0.16/28", "10.176.4.0/23", "100.80.32.0/19", "100.66.0.128/25", "100.120.0.64/28", "10.176.9.0/24", "100.76.16.0/20", "100.65.0.64/26", "10.176.11.96/28", "100.72.32.0/21", "100.64.0.0/27", "10.176.11.97", "10.176.11.112/28", "100.64.0.32/27", "100.72.40.0/21"]

peer_prefix      = "net-peer"
peer_prefix_ds   = "ds-net-peer"
peer_prefix_t_ds   = "ds-t-net-peer"
peer_prefix_test = "test-net-peer"
peer_prefix_mktg = "mktg-net-peer"
peer_prefix_t_mktg = "mktg-test-net-peer"
# Orchestrator resources
orchestrator_network_name = "vpc-np-orchestrator"
orchestrator_description  = "Cloud Composer VPC Network name"
composer_subnet_name      = "sb-np-orchestrator-composer"
composer_subnet_ip        = "10.176.11.0/26"

nat_bgp_asn = 65222

cc_gke_node_subnet    = ["10.176.11.0/26"]
cc_gke_pods_subnet    = ["100.72.0.0/21"]
cc_gke_service_subnet = ["100.64.0.0/27"]
cc_gke_master_subnet  = ["100.120.0.96/28"]
