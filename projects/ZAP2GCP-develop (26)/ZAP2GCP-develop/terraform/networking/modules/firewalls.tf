/******************************************
  Hive Metastore Firewall rules
*****************************************/

module "firewall_rules" {
  source     = "github.com/terraform-google-modules/terraform-google-network//modules/fabric-net-firewall?ref=v3.3.0"
  project_id = var.project_id
  network    = local.network_name_ref

  internal_ranges_enabled = false
  admin_ranges_enabled    = false
  ssh_source_ranges       = []
  http_source_ranges      = []
  https_source_ranges     = []

  custom_rules = {
    "fw-hive-vpc-350-e-a-tcp-3306-3307-mysql" = {
      description          = "Allow CloudSql Mysql egress ports"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = concat(module.hive_metastore_vpc.subnets_ips, local.psa_ip_range)
      sources              = null
      use_service_accounts = false
      targets              = ["sql-proxy"]
      rules = [{
        protocol = "tcp"
        ports    = ["3306", "3307"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    },
    # Allow ingress to Google IP’s that perform health checks
    "fw-hive-vpc-50-i-a-tcp-3306-from-gcp-hc" = {
      description          = "Allow ingress from Google health check IPs"
      direction            = "INGRESS"
      action               = "allow"
      ranges               = ["130.211.0.0/22", "35.191.0.0/16"]
      sources              = null
      use_service_accounts = false
      targets              = ["sql-proxy"]
      rules = [{
        protocol = "tcp"
        ports    = ["3306"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "50"
      }
    },

    # Allow egress to Google IP’s that perform health checks
    "fw-hive-vpc-350-e-a-tcp-3306-to-gcp-hc" = {
      description          = "Allow egress to Google health check IPs"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["130.211.0.0/22", "35.191.0.0/16"]
      sources              = null
      use_service_accounts = false
      targets              = ["sql-proxy"]
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
    "fw-hive-vpc-50-i-a-tcp-3306-mysql" = {
      description          = "Allow ingress to MySql connections"
      direction            = "INGRESS"
      action               = "allow"
      ranges               = var.cidr_allow_sql_ingress
      sources              = null
      use_service_accounts = false
      targets              = ["sql-proxy"]
      rules = [{
        protocol = "tcp"
        ports    = ["3306"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "50"
      }
    },
    #Allow traffic to the restricted Google APIs VIP (Virtual IP) 
    "fw-hive-vpc-350-e-a-all-to-google-apis" = {
      description          = "Allow traffic to the restricted Google APIs"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["199.36.153.4/30"]
      sources              = null
      use_service_accounts = false
      targets              = ["sql-proxy"]
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
    # Deny Ingress internal RFC1918 ranges
    "fw-hive-vpc-200-i-d-all-rfc" = {
      description          = "Deny Ingress Internal RFC 1918 ranges."
      direction            = "INGRESS"
      action               = "deny"
      ranges               = ["10.0.0.0/8", "192.168.0.0/16", "172.16.0.0/12"]
      sources              = null
      use_service_accounts = false
      targets              = ["sql-proxy"]
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
    "fw-hive-vpc-300-i-d-all-source" = {
      description          = "Deny Ingress all ranges."
      direction            = "INGRESS"
      action               = "deny"
      ranges               = ["0.0.0.0/0"]
      sources              = null
      use_service_accounts = false
      targets              = ["sql-proxy"]
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
    "fw-hive-vpc-400-e-d-all-rfc" = {
      description          = "Deny Egress Internal RFC 1918 ranges."
      direction            = "EGRESS"
      action               = "deny"
      ranges               = ["10.0.0.0/8", "192.168.0.0/16", "172.16.0.0/12"]
      sources              = null
      use_service_accounts = false
      targets              = ["sql-proxy"]
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
    "fw-hive-vpc-500-e-d-all-source" = {
      description          = "Deny egress to all ranges from db vpc"
      direction            = "EGRESS"
      action               = "deny"
      ranges               = ["0.0.0.0/0"]
      sources              = null
      use_service_accounts = false
      targets              = ["sql-proxy"]
      rules = [{
        protocol = "all" # all protocols
        ports    = null  # all ports
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "500"
      }
    }
  }
}

/******************************************
  Orchestrator Firewall rules
*****************************************/
module "orchestrator_firewall_rules" {
  source = "github.com/terraform-google-modules/terraform-google-network//modules/fabric-net-firewall?ref=v3.3.0"

  project_id = var.project_id
  network    = local.orchestrator_network_name_ref

  internal_ranges_enabled = false
  admin_ranges_enabled    = false
  ssh_source_ranges       = []
  http_source_ranges      = []
  https_source_ranges     = []

  custom_rules = {
    #Allow egress from GKE Node IP range to any destination.
    "fw-orch-vpc-50-i-a-tcp-80-443-gcp-hc" = {
      description          = "Allow ingress to Google health check IPs"
      direction            = "INGRESS"
      action               = "allow"
      ranges               = ["130.211.0.0/22", "35.191.0.0/16"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
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
    #Allow egress from GKE Node IP range to GCP Health Checks
    "fw-orch-vpc-350-e-a-all-to-gcp-hc" = {
      description          = "Allow egress from GKE Node IP range to GCP Health Checks"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["130.211.0.0/22", "35.191.0.0/16"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
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
    #Allow egress from GKE Node IP range to any destination.
    "fw-orch-vpc-350-e-a-tcp-53" = {
      description          = "Allow egress from GKE Node IP range to any destination on TCP/UDP port 53"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["0.0.0.0/0"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
      rules = [{
        protocol = "tcp"
        ports    = ["53"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    },
    # Allow ingress to GKE Nodes
    "fw-orch-vpc-50-i-a-tcp-all-gke-node-pod-svc" = {
      description          = "Allow ingress from local network to GKE Nodes"
      direction            = "INGRESS"
      action               = "allow"
      ranges               = concat(var.cc_gke_node_subnet, var.cc_gke_pods_subnet, var.cc_gke_service_subnet, var.cc_gke_master_subnet)
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
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
    #Allow egress from to GKE Service Range.
    "fw-orch-vpc-350-e-a-all-to-gke-svc" = {
      description          = "Allow egress to GKE Svc IP range"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = var.cc_gke_service_subnet
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
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
    #Allow egress from GKE Node IP range to GKE Node IP range, all ports.
    "fw-orch-vpc-350-e-a-all-to-gke-nodes" = {
      description          = "Allow egress to GKE Node IP range"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = var.cc_gke_node_subnet
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
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
    #Allow egress from GKE Node IP range to GKE Pods IP range, all ports.
    "fw-orch-vpc-350-e-a-all-to-gke-pods" = {
      description          = "Allow egress to GKE Pods IP range"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = var.cc_gke_pods_subnet
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
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
    #Allow egress from GKE Node IP range to GKE Control Plane IP range.
    "fw-orch-vpc-350-e-a-all-to-gke-control-plane" = {
      description          = "Allow egress from GKE Node IP range to GKE Control Plane IP range"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = var.cc_gke_master_subnet
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
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
    #Allow egress from GKE Node IP range to Web server IP range.
    "fw-orch-vpc-350-e-a-all-to-web-server" = {
      description          = "Allow egress from GKE Node IP range to Web server IP range"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["10.176.15.0/24"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
      rules = [{
        protocol = "tcp"
        ports    = ["3306", "3307"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    },
    #Allow traffic to the restricted Google APIs VIP (Virtual IP)
    "fw-orch-vpc-350-e-a-all-to-google-apis" = {
      description          = "Allow traffic to the restricted Google APIs"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["199.36.153.4/30"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
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
    # Deny Ingress internal RFC1918 ranges
    "fw-orch-vpc-200-i-d-all-rfc" = {
      description          = "Deny Ingress Internal RFC 1918 ranges."
      direction            = "INGRESS"
      action               = "deny"
      ranges               = ["10.0.0.0/8", "192.168.0.0/16", "172.16.0.0/12"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
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
    "fw-orch-vpc-300-i-d-all-source" = {
      description          = "Deny Ingress all ranges."
      direction            = "INGRESS"
      action               = "deny"
      ranges               = ["0.0.0.0/0"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
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
    "fw-orch-vpc-400-e-d-all-rfc" = {
      description          = "Deny Egress Internal RFC 1918 ranges."
      direction            = "EGRESS"
      action               = "deny"
      ranges               = ["10.0.0.0/8", "192.168.0.0/16", "172.16.0.0/12"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
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
    # Deny Egress to all ranges
    "fw-orch-vpc-500-e-d-all" = {
      description          = "Deny Egress to all ranges"
      direction            = "EGRESS"
      action               = "deny"
      ranges               = ["0.0.0.0/0"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
      rules = [{
        protocol = "all"
        ports    = null
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "500"
      }
    },
    # Allow traffic to Install Python PYPI packages 
    "fw-orch-vpc-350-e-a-tcp-80-443-python-pypi" = {
      description          = "Allow traffic to Install Python PYPI packages"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["151.101.0.0/16"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
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
    # Allow egress to Google Ips - https://cloud.google.com/vpc/docs/configure-private-google-access#ip-addr-defaults
    "fw-orch-vpc-450-e-a-setup-ips" = {
      description = "Allowing egress access to these 4Ips required during setup - workoud"
      direction   = "EGRESS"
      action      = "allow"
      ranges = [
        "8.8.4.0/24", "8.8.8.0/24", "8.34.208.0/20", "8.35.192.0/20", "23.236.48.0/20", "23.251.128.0/19", "34.64.0.0/10", "34.128.0.0/10", "35.184.0.0/13", "35.192.0.0/14", "35.196.0.0/15", "35.198.0.0/16", "35.199.0.0/17", "35.199.128.0/18", "35.200.0.0/13", "35.208.0.0/12", "35.224.0.0/12", "35.240.0.0/13", "64.15.112.0/20", "64.233.160.0/19", "66.102.0.0/20", "66.249.64.0/19", "70.32.128.0/19", "72.14.192.0/18", "74.114.24.0/21", "74.125.0.0/16", "104.154.0.0/15", "104.196.0.0/14", "104.237.160.0/19", "107.167.160.0/19", "107.178.192.0/18", "108.59.80.0/20", "108.170.192.0/18", "108.177.0.0/17", "130.211.0.0/16", "136.112.0.0/12", "142.250.0.0/15", "146.148.0.0/17", "162.216.148.0/22", "162.222.176.0/21", "172.110.32.0/21", "172.217.0.0/16", "172.253.0.0/16", "173.194.0.0/16", "173.255.112.0/20", "192.158.28.0/22", "192.178.0.0/15", "193.186.4.0/24", "199.36.154.0/23", "199.36.156.0/24", "199.192.112.0/22", "199.223.232.0/21", "207.223.160.0/20", "208.65.152.0/22", "208.68.108.0/22", "208.81.188.0/22", "208.117.224.0/19", "209.85.128.0/17", "216.58.192.0/19", "216.73.80.0/20", "216.239.32.0/19"
      ]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
      rules = [{
        protocol = "all"
        ports    = null
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "450"
      }
    },
    # Allow SSH access to Compute Instance ()
    "fw-orch-vpc-50-i-a-iap-ssh" = {
      description          = "Allowing egress access to these 4Ips required during setup - workoud"
      direction            = "INGRESS"
      action               = "allow"
      ranges               = ["35.235.240.0/20"]
      sources              = null
      use_service_accounts = false
      targets              = ["allow-iap-ssh"]
      rules = [{
        protocol = "tcp"
        ports    = ["22"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "50"
      }
    }
  }
} 