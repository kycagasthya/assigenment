# module "dbricks_vpc_hardening" {
#   source     = "../../../modules/"
#   project_id = var.project_id

#   dbx_network_name = var.dbx_network_name

#   db_gke_master_ip      = var.db_gke_master_ip
#   db_gke_node_subnet    = var.db_gke_node_subnet
#   db_gke_pods_subnet    = var.db_gke_pods_subnet
#   db_gke_service_subnet = var.db_gke_service_subnet

#   db_control_plane_nat_ip  = var.db_control_plane_nat_ip
#   db_control_plane_npip_ip = var.db_control_plane_npip_ip
#   db_workspace_url         = var.db_workspace_url
#   db_managed_hive          = var.db_managed_hive
#   db_endpoint_ip           = var.db_endpoint_ip

#   db_control_plane_nat_ip_rt  = var.db_control_plane_nat_ip_rt
#   db_control_plane_npip_ip_rt = var.db_control_plane_npip_ip_rt
#   db_workspace_url_rt         = var.db_workspace_url_rt
#   db_managed_hive_rt          = var.db_managed_hive_rt

#   hive_sql_cidr_range = var.hive_sql_cidr_range
# }

# Hard coded Values

# Google health-check IP 	- ["130.211.0.0/22, 35.191.0.0/16"]
# Google API access IP   	- ["199.36.153.4/30"]
# Zebra Sharepoint IP 	- ["20.190.155.0/24","13.107.136.0/22", "40.108.128.0/17", "52.104.0.0/14", "104.146.128.0/17", "150.171.40.0/22", "104.21.91.94/32", "20.190.155.3/32"]
# Python PYPI 	        - ["151.101.0.0/16"]

