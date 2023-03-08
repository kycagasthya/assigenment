module "firewalls" {
  source     = "github.com/terraform-google-modules/terraform-google-network//modules/fabric-net-firewall?ref=v3.3.0"
  project_id = var.project_id
  network    = local.network_name_ref

  internal_ranges_enabled = false
  admin_ranges_enabled    = false
  ssh_source_ranges       = []
  http_source_ranges      = []
  https_source_ranges     = []

  custom_rules = {
    # Allow ingress to Google IP’s that perform health checks
    "fw-db-vpc-50-i-a-tcp-80-443-from-gcp-hc" = {
      description          = "Allow ingress from Google health check IPs"
      direction            = "INGRESS"
      action               = "allow"
      ranges               = ["130.211.0.0/22", "35.191.0.0/16"]
      sources              = null
      use_service_accounts = false
      targets              = null
      rules = [{
        protocol = "tcp"
        ports    = ["80", "443"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "50"
      }
    },

    # Allow ingress to GKE Nodes
    "fw-db-vpc-50-i-a-tcp-all-gke-node-pod-svc" = {
      description          = "Allow ingress from local network to GKE Nodes"
      direction            = "INGRESS"
      action               = "allow"
      ranges               = concat(var.db_gke_node_subnet, var.db_gke_pods_subnet, var.db_gke_service_subnet)
      sources              = null
      use_service_accounts = false
      targets              = null
      rules = [{
        protocol = "all"
        ports    = null
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "50"
      }
    },
    # Allow egress to Google IP’s that perform health checks
    "fw-db-vpc-350-e-a-tcp-80-443-to-gcp-hc" = {
      description          = "Allow egress to Google health check IPs"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["130.211.0.0/22", "35.191.0.0/16"]
      sources              = null
      use_service_accounts = false
      targets              = null
      rules = [{
        protocol = "tcp"
        ports    = ["80", "443"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    },

    #Allow traffic to the restricted Google APIs VIP (Virtual IP) 
    "fw-db-vpc-350-e-a-all-to-google-apis" = {
      description          = "Allow traffic to the restricted Google APIs"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["199.36.153.4/30"]
      sources              = null
      use_service_accounts = false
      targets              = null
      rules = [{
        protocol = "all" # all protocols
        ports    = null  # all ports
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    },

    #Allow traffic from the GKE worker-vpc (Databricks) to the master-vpc (peered GKE master) 
    "fw-db-vpc-350-e-a-all-to-gke-master" = {
      description          = "Allow traffic from the GKE worker-vpc (Databricks) to the master-vpc (peered GKE master)"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = var.db_gke_master_ip
      sources              = null
      use_service_accounts = false
      targets              = null
      rules = [{
        protocol = "all" # all protocols
        ports    = null  # all ports
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    },
    #Allow traffic from GKE Master to worker nodes
    "fw-db-vpc-50-i-a-443-10250-from-gke-master" = {
      description          = "Allow traffic from the GKE master to nodes"
      direction            = "INGRESS"
      action               = "allow"
      ranges               = var.db_gke_master_ip
      sources              = null
      use_service_accounts = false
      targets              = null
      rules = [{
        protocol = "tcp" # all protocols
        ports    = ["443", "10250"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "50"
      }
    },
    #Allow traffic to GKE nodes
    "fw-db-vpc-350-e-a-all-to-gke-nodes-subnet" = {
      description          = "Allow traffic to GKE nodes subnet"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = var.db_gke_node_subnet
      sources              = null
      use_service_accounts = false
      targets              = null
      rules = [{
        protocol = "all" # all protocols
        ports    = null  # all ports
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    },

    #Allow traffic to GKE pods subnet 
    "fw-db-vpc-350-e-a-all-to-gke-pods-subnet" = {
      description          = "Allow traffic to GKE pods subnet"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = var.db_gke_pods_subnet
      sources              = null
      use_service_accounts = false
      targets              = null
      rules = [{
        protocol = "all" # all protocols
        ports    = null  # all ports
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    },

    #Allow traffic to GKE service subnet 
    "fw-db-vpc-350-e-a-all-to-gke-service-subnet" = {
      description          = "Allow traffic to GKE service subnet"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = var.db_gke_service_subnet
      sources              = null
      use_service_accounts = false
      targets              = null
      rules = [{
        protocol = "all" # all protocols
        ports    = null  # all ports
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    },

    #Allow traffic to Databricks control plane (NAT IP) 
    "fw-db-vpc-350-e-a-tcp-443-80-to-db-control-plane-nat" = {
      description          = "Allow traffic to Databricks control plane (NAT IP)"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = var.db_control_plane_nat_ip
      sources              = null
      use_service_accounts = false
      targets              = null
      rules = [{
        protocol = "tcp"
        ports    = ["80", "443"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    },

    #Allow traffic to Databricks control plane (NPIP IP)
    "fw-db-vpc-350-e-a-tcp-443-80-to-db-control-plane-npip" = {
      description          = "Allow traffic to Databricks control plane (NPIP IP)"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = var.db_control_plane_npip_ip
      sources              = null
      use_service_accounts = false
      targets              = null
      rules = [{
        protocol = "tcp"
        ports    = ["80", "443"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    },
    #Allow traffic to Databricks Endpoint
    "fw-db-vpc-350-e-a-all-to-db-endpoint" = {
      description          = "Allow traffic to Databricks Endpoint"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = var.db_endpoint_ip
      sources              = null
      use_service_accounts = false
      targets              = null
      rules = [{
        protocol = "all"
        ports    = null
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    },

    #Allow traffic to Databricks workspace URL 
    "fw-db-vpc-350-e-a-tcp-443-80-to-db-workspace" = {
      description          = "Allow traffic to Databricks workspace URL"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = var.db_workspace_url
      sources              = null
      use_service_accounts = false
      targets              = null
      rules = [{
        protocol = "tcp"
        ports    = ["80", "443"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    },

    #Allow traffic to Databricks Managed Hive Metastore
    "fw-db-vpc-350-e-a-tcp-3306-to-db-managed-hive" = {
      description          = "Allow traffic to Databricks Managed Hive Metastore"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = var.db_managed_hive
      sources              = null
      use_service_accounts = false
      targets              = null
      rules = [{
        protocol = "tcp"
        ports    = ["3306"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    },
    #Allow traffic to CloudSQL Hive Metastore
    "fw-db-vpc-350-e-a-tcp-3306-to-cloudsql-hive" = {
      description          = "Allow traffic to CloudSQL Hive Metastore"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = var.hive_sql_cidr_range
      sources              = null
      use_service_accounts = false
      targets              = null
      rules = [{
        protocol = "tcp"
        ports    = ["3306"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    },
    # Allow traffic to Zebra Sharepoint
    "fw-db-vpc-350-e-a-tcp-80-443-zb-sharepoint" = {
      description = "Allow traffic to Zebra Sharepoint"
      direction   = "EGRESS"
      action      = "allow"
      ranges = [
        "13.107.136.0/22",
        "40.108.128.0/17",
        "52.104.0.0/14",
        "104.146.128.0/17",
        "150.171.40.0/22",
        "104.21.91.94/32",
        "20.190.155.3/32",
        "20.190.155.0/24"
      ]
      sources              = null
      use_service_accounts = false
      targets              = null
      rules = [{
        protocol = "tcp"
        ports    = ["80", "443"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    },

    # Allow traffic to Install Python PYPI packages 
    "fw-db-vpc-350-e-a-tcp-80-443-python-pypi" = {
      description          = "Allow traffic to Install Python PYPI packages"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["151.101.0.0/16"]
      sources              = null
      use_service_accounts = false
      targets              = null
      rules = [{
        protocol = "tcp"
        ports    = ["80", "443"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    },
    # Allow traffic for Git and SSH 
    "fw-db-vpc-350-e-a-tcp-22-443-for-git-ssh" = {
      description = "Allow traffic for Git HTTPS and SSH options"
      direction   = "EGRESS"
      action      = "allow"
      ranges = [
        "192.30.252.0/22", "185.199.108.0/22", "140.82.112.0/20", "143.55.64.0/20", "13.114.40.48/32", "52.192.72.89/32", "52.69.186.44/32", "15.164.81.167/32", "52.78.231.108/32", "13.234.176.102/32", "13.234.210.38/32", "13.229.188.59/32", "13.250.177.223/32", "52.74.223.119/32", "13.236.229.21/32", "13.237.44.5/32", "52.64.108.95/32", "18.228.52.138/32", "18.228.67.229/32", "18.231.5.6/32", "20.201.28.151/32", "20.205.243.166/32", "18.181.13.223/32", "54.238.117.237/32", "54.168.17.15/32", "3.34.26.58/32", "13.125.114.27/32", "3.7.2.84/32", "3.6.106.81/32", "18.140.96.234/32", "18.141.90.153/32", "18.138.202.180/32", "52.63.152.235/32", "3.105.147.174/32", "3.106.158.203/32", "54.233.131.104/32", "18.231.104.233/32", "18.228.167.86/32", "20.201.28.152/32", "20.205.243.160/32"
      ]
      sources              = null
      use_service_accounts = false
      targets              = null
      rules = [{
        protocol = "tcp"
        ports    = ["22", "443"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    },
    # Deny Ingress internal RFC1918 ranges
    "fw-db-vpc-200-i-d-all-rfc" = {
      description          = "Deny Ingress Internal RFC 1918 ranges."
      direction            = "INGRESS"
      action               = "deny"
      ranges               = ["10.0.0.0/8", "192.168.0.0/16", "172.16.0.0/12"]
      sources              = null
      use_service_accounts = false
      targets              = null
      rules = [{
        protocol = "all"
        ports    = null
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "200"
      }
    },
    # Deny Ingress all ranges
    "fw-db-vpc-300-i-d-all-source" = {
      description          = "Deny Ingress all ranges."
      direction            = "INGRESS"
      action               = "deny"
      ranges               = ["0.0.0.0/0"]
      sources              = null
      use_service_accounts = false
      targets              = null
      rules = [{
        protocol = "all"
        ports    = null
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "300"
      }
    },
    # Deny Ingress internal RFC1918 ranges
    "fw-db-vpc-400-e-d-all-rfc" = {
      description          = "Deny Egress Internal RFC 1918 ranges."
      direction            = "EGRESS"
      action               = "deny"
      ranges               = ["10.0.0.0/8", "192.168.0.0/16", "172.16.0.0/12"]
      sources              = null
      use_service_accounts = false
      targets              = null
      rules = [{
        protocol = "all"
        ports    = null
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "400"
      }
    },
    # Deny Egress to all ranges from the databricks VPC network
    "fw-db-vpc-500-e-d-all-source" = {
      description          = "Deny egress to all ranges from db vpc"
      direction            = "EGRESS"
      action               = "deny"
      ranges               = ["0.0.0.0/0"]
      sources              = null
      use_service_accounts = false
      targets              = null
      rules = [{
        protocol = "all" # all protocols
        ports    = null  # all ports
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "500"
      }
    },

    # Allow external sites from the databricks network 
    "fw-db-vpc-350-e-a-tcp-443-allow-external-sites-egress" = {
      description          = "Allow external sites from the databricks network"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["0.0.0.0/0"]
      sources              = null
      use_service_accounts = false
      targets              = null
      rules = [{
        protocol = "tcp"
        ports    = ["443"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    },
    # Allow access to ADW
    "fw-db-vpc-350-e-all-access-adw" = {
      description          = "Egress allow access to Oracle ADW"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["147.154.25.5/32", "130.35.203.118/32", "130.35.144.65/32", "130.35.147.64/32", "130.35.144.64/32"]
      sources              = null
      use_service_accounts = false
      targets              = null
      rules = [{
        protocol = "tcp" 
        ports    = ["1522"]  
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    },
	# Allow access to SQL Azure
    "fw-its-managed-dbx-de-sqlazure-egress" = {
      description          = "Egress allow access to SQL Azure"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["51.140.184.11", "51.105.64.0", "51.140.144.36", "51.105.72.32", "51.105.64.32/29", "51.105.72.32/29", "51.140.144.32/29"]
      sources              = null
      use_service_accounts = false
      targets              = null
      rules = [{
        protocol = "tcp" 
        ports    = ["1433"]  
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    }
  }
}
