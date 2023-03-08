module "firewall_rules_on_prem" {
  source     = "github.com/terraform-google-modules/terraform-google-network//modules/fabric-net-firewall?ref=v3.3.0"
  project_id = var.project_id
  network    = local.network_name_ref

  internal_ranges_enabled = false
  admin_ranges_enabled    = false
  ssh_source_ranges       = []
  http_source_ranges      = []
  https_source_ranges     = []

  custom_rules = {
    /******************************************
    #   Firewall rules for On-premise network (non-prod)
    *****************************************/
    "fw-hive-vpc-150-i-a-5986-ansible-winrm" = {
      description          = "Allow ingress for ansible-winrm"
      direction            = "INGRESS"
      action               = "allow"
      ranges               = ["10.66.76.40/32"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
      rules = [{
        protocol = "tcp"
        ports    = ["5986"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "150"
      }
    },
    "fw-hive-vpc-350-e-a-52311-bigfix-internal" = {
      description          = "Allow egress for bigfix-internal"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["10.66.70.145", "172.16.0.0/12", "192.168.0.0/16", "10.0.0.0/8"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
      rules = [
        {
          protocol = "tcp"
          ports    = ["52311"]
        },
        {
          protocol = "udp"
          ports    = ["52311"]
        }
      ]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    },
    "fw-hive-vpc-450-e-a-443-crowdstrike-external-1" = {
      description          = "Allow egress for bigfix-internal"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["54.241.181.78", "54.241.182.78", "54.241.183.229", "54.67.41.192", "54.67.122.238", "54.67.17.131", "54.241.183.151", "54.241.183.232", "54.183.28.214", "54.183.51.31", "54.183.148.43", "54.183.148.116", "54.193.67.98", "52.8.61.206", "52.9.77.209", "52.9.87.98", "54.183.34.154", "54.183.140.32", "54.183.142.105", "54.67.108.17", "54.67.24.156", "54.67.72.218", "54.67.114.188", "54.67.4.108", "54.183.215.154", "50.18.198.237", "54.67.5.136", "52.8.160.82", "52.8.54.244", "54.183.24.162", "54.193.27.226", "54.215.176.108", "54.67.96.255", "52.8.172.89", "54.183.252.86", "54.193.29.47", "54.219.145.181", "54.67.99.247", "52.8.173.58", "54.183.122.156", "54.241.150.134", "52.8.32.113", "54.183.39.68", "54.193.90.171", "54.241.161.60", "52.8.45.162", "54.183.51.69", "54.215.131.232", "54.67.105.202", "52.8.52.230", "54.183.234.42", "54.193.117.199", "54.215.169.199", "54.67.123.150", "54.193.86.245", "54.219.179.25", "54.67.78.134", "54.219.158.223", "54.241.161.242", "54.67.51.32", "54.215.170.42"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
      rules = [{
        protocol = "tcp"
        ports    = ["443"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "450"
      }
    },
    "fw-hive-vpc-450-e-a-dmz-domain-controllers" = {
      description          = "Allow egress for dmz-domain-controllers"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["10.77.214.108", "192.168.203.123", "10.6.204.32", "10.6.204.33", "10.17.240.22", "10.17.240.23", "10.66.80.32"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
      rules = [
        {
          protocol = "tcp"
          ports    = ["139", "636", "3268", "3269", "53", "88", "135", "137", "464", "445", "389", "49152-65535"]
        },
        {
          protocol = "udp"
          ports    = ["123", "138", "53", "88", "135", "137", "464", "445", "389", "49152-65535"]
        }
      ]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    },
    "fw-hive-vpc-350-e-a-gcp-domain-controllers-sync" = {
      description          = "Allow egress for dmz-domain-controllers"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["10.3.1.248", "10.35.1.35", "10.35.1.34", "10.18.1.30", "10.78.1.29", "10.4.1.34", "10.21.1.32", "10.6.1.34", "10.42.20.24", "10.80.1.40", "10.2.1.16", "10.1.2.30", "10.63.2.12", "10.14.1.91", "10.1.1.30", "10.63.2.11", "10.225.1.30", "10.3.1.249", "10.21.1.31", "10.61.1.248", "10.31.1.31", "10.8.2.11", "10.104.1.30", "10.17.1.31", "10.39.1.21", "10.80.1.41", "10.9.1.34", "10.10.1.34", "10.45.1.30", "10.84.1.248", "10.37.1.30", "10.26.1.34", "10.112.2.2", "10.56.1.30", "10.6.1.35", "10.77.0.249", "10.80.1.42", "10.206.1.30", "10.66.0.249", "10.48.1.30", "10.61.1.249", "10.14.1.93", "10.25.1.32", "10.43.1.30", "10.16.1.30", "10.17.1.30", "10.83.16.47", "10.82.24.3", "10.82.16.8", "10.171.0.7", "10.170.0.3", "10.170.96.7", "10.171.96.2", "10.170.48.5", "10.171.48.2", "10.66.0.145", "10.77.0.250", "10.77.70.175"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
      rules = [
        {
          protocol = "tcp"
          ports    = ["42", "135", "137", "139", "389", "636", "3268", "3269", "445", "49152-65535", "53", "88", "9389", "5722", "464", "1024-5000"]
        },
        {
          protocol = "udp"
          ports    = ["389", "49152-65535", "53", "88", "445", "464", "123", "137", "138", "67", "2535", "1024-5000"]
        }
      ]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    },
    "fw-hive-vpc-350-e-a-gcp-zgn-icmp" = {
      description          = "Allow egress for gcp-zgn-icmp"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["10.0.0.0/8", "192.168.0.0/16", "172.16.0.0/12"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
      rules = [{
        protocol = "icmp"
        ports    = null
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    },
    "fw-hive-vpc-150-i-a-gcp-zgn-icmp" = {
      description          = "Allow ingress for gcp-zgn-icmp"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["10.0.0.0/8", "192.168.0.0/16", "172.16.0.0/12"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
      rules = [{
        protocol = "icmp"
        ports    = null
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "150"
      }
    },
    "fw-hive-vpc-350-e-a-internal-certificate-services" = {
      description          = "Allow egress for internal-certificate-services"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["10.1.1.35", "10.66.0.244", "10.66.70.63", "10.66.70.91", "10.77.70.105", "10.77.70.127"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
      rules = [{
        protocol = "tcp"
        ports    = ["80", "135", "443", "49152-65535"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    },
    "fw-hive-vpc-350-e-a-internal-email" = {
      description          = "Allow egress for internal-email"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["10.3.1.77"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
      rules = [{
        protocol = "tcp"
        ports    = ["25"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    },
    "fw-hive-vpc-350-e-a-linux-patching" = {
      description          = "Allow egress for linux-patching"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["10.66.76.34"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
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
    "fw-hive-vpc-450-e-a-logrhythm-external-1" = {
      description          = "Allow egress for logrhythm-external-1"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["35.160.202.132"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
      rules = [{
        protocol = "tcp"
        ports    = ["443"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "450"
      }
    },
    "fw-hive-vpc-350-e-a-logrythm-internal" = {
      description          = "Allow egress for logrythm-internal"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["10.88.3.10"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
      rules = [{
        protocol = "tcp"
        ports    = ["443", "137"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    },
    "fw-hive-vpc-150-i-a-logrythm-internal-1" = {
      description          = "Allow ingress for logrythm-internal-1"
      direction            = "INGRESS"
      action               = "allow"
      ranges               = ["10.88.3.10"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
      rules = [{
        protocol = "tcp"
        ports    = ["443"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "150"
      }
    },
    "fw-hive-vpc-450-e-a-nessus-external-1" = {
      description          = "Allow egress for nessus-external-1"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["13.59.252.0/25", "54.175.125.192/26", "34.201.223.128/25", "54.219.188.128/26", "13.56.21.128/25", "54.93.254.128/26", "18.194.95.64/26", "35.177.219.0/26", "3.9.159.128/25", "54.255.254.0/26", "18.139.204.0/25", "13.210.1.64/26", "3.106.118.128/25", "35.182.14.0/24", "13.115.104.0/24"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
      rules = [{
        protocol = "tcp"
        ports    = ["443"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "450"
      }
    },
    "fw-hive-vpc-50-i-a-non-prod-east-west" = {
      description          = "Allow egress for non-prod-east-west"
      direction            = "INGRESS"
      action               = "allow"
      ranges               = ["0.0.0.0/0"]
      sources              = ["non-prod"]
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
    "fw-hive-vpc-350-e-a-sccm-servers" = {
      description          = "Allow egress for sccm-servers"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["10.1.1.44", "10.4.1.40", "10.6.1.57", "10.8.41.24", "10.9.1.56", "10.104.1.59", "10.112.41.4", "10.14.1.72", "10.16.1.33", "10.17.0.37", "10.18.1.40", "10.206.5.32", "10.21.1.33", "10.225.5.32", "10.31.0.38", "10.35.1.70", "10.37.1.36", "10.39.1.45", "10.43.2.39", "10.48.1.34", "10.61.0.65", "10.63.41.32", "10.66.70.166", "10.66.70.123", "10.80.1.46", "10.82.16.6", "10.82.24.8", "10.82.80.5", "10.83.16.46", "10.80.122.120"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
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
    "fw-hive-vpc-350-e-a-squid-proxy" = {
      description          = "Allow egress for squid-proxy"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["10.3.0.65"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
      rules = [{
        protocol = "tcp"
        ports    = ["8080"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    },
    "fw-hive-vpc-450-e-a-ubuntu-public-repository" = {
      description          = "Allow egress for ubuntu-public-repository"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["91.189.88.152", "91.189.88.142", "91.189.91.38", "91.189.91.39"]
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
        priority           = "450"
      }
    },
    "fw-hive-vpc-350-e-a-wsus-servers" = {
      description          = "Allow egress for wsus-servers"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["10.3.1.66", "10.48.1.45", "10.1.1.85", "10.1.1.74", "10.77.70.114", "10.66.70.89", "10.18.1.91", "10.14.1.169", "10.6.1.54", "10.104.1.40"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
      rules = [{
        protocol = "tcp"
        ports    = ["80", "8530", "8531"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    },
    "fw-hive-vpc-350-e-a-zabbix-servers" = {
      description          = "Allow egress for zabbix-servers"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["10.66.1.107", "10.77.0.107", "10.6.1.249", "10.66.0.107", "10.17.8.34", "10.104.1.50"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
      rules = [{
        protocol = "tcp"
        ports    = ["10050", "10051"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    },
    "fw-hive-vpc-150-i-a-zabbix-servers-2" = {
      description          = "Allow ingress for zabbix-servers-2"
      direction            = "INGRESS"
      action               = "allow"
      ranges               = ["10.66.1.107", "10.77.0.107", "10.6.1.249", "10.66.0.107", "10.17.8.34", "10.104.1.50"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
      rules = [{
        protocol = "tcp"
        ports    = ["10050"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "150"
      }
    },
    "fw-hive-vpc-350-e-a-zebra-domain-controllers" = {
      description          = "Allow egress for zebra-domain-controllers"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["10.3.1.248", "10.35.1.35", "10.35.1.34", "10.18.1.30", "10.78.1.29", "10.4.1.34", "10.21.1.32", "10.6.1.34", "10.42.20.24", "10.80.1.40", "10.2.1.16", "10.1.2.30", "10.63.2.12", "10.14.1.91", "10.1.1.30", "10.63.2.11", "10.225.1.30", "10.3.1.249", "10.21.1.31", "10.61.1.248", "10.31.1.31", "10.8.2.11", "10.104.1.30", "10.17.1.31", "10.39.1.21", "10.80.1.41", "10.9.1.34", "10.10.1.34", "10.45.1.30", "10.84.1.248", "10.37.1.30", "10.26.1.34", "10.112.2.2", "10.56.1.30", "10.6.1.35", "10.77.0.249", "10.80.1.42", "10.206.1.30", "10.66.0.249", "10.48.1.30", "10.61.1.249", "10.14.1.93", "10.25.1.32", "10.43.1.30", "10.16.1.30", "10.17.1.30", "10.83.16.47", "10.82.24.3", "10.82.16.8", "10.61.0.49", "10.66.1.239", "10.170.0.3", "10.171.0.7", "10.170.96.7", "10.171.96.2", "10.170.48.5", "10.171.48.2", "10.77.0.250", "10.77.70.175"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
      rules = [
        {
          protocol = "tcp"
          ports    = ["389", "636"]
        },
        {
          protocol = "udp"
          ports    = ["123"]
        }
      ]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    },
    "fw-hive-vpc-150-i-a-zebra-pam-1" = {
      description          = "Allow ingress for zebra-pam-1"
      direction            = "INGRESS"
      action               = "allow"
      ranges               = ["10.77.71.38", "10.66.70.231", "10.77.0.161", "10.17.0.45", "10.17.0.46", "10.35.1.49", "10.35.1.74"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
      rules = [{
        protocol = "tcp"
        ports    = ["135", "139", "389", "445", "1433"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "150"
      }
    },
    "fw-hive-vpc-150-i-a-zgn-gcp-bigfix" = {
      description          = "Allow ingress for zgn-gcp-bigfix"
      direction            = "INGRESS"
      action               = "allow"
      ranges               = ["10.0.0.0/8", "192.168.0.0/16", "172.16.0.0/12"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
      rules = [
        {
          protocol = "tcp"
          ports    = ["52311"]
        },
        {
          protocol = "udp"
          ports    = ["52311"]
        }
      ]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "150"
      }
    },
    "fw-hive-vpc-150-i-a-zgn-gcp-rdp" = {
      description          = "Allow ingress for zgn-gcp-rdp"
      direction            = "INGRESS"
      action               = "allow"
      ranges               = ["10.1.76.0/23", "10.35.76.0/24", "10.6.76.0/24", "10.66.240.32/27", "10.66.76.0/24", "10.77.240.32/27", "10.77.76.0/24", "10.80.76.0/24", "10.63.76.0/24", "10.6.240.32/27", "10.35.240.32/27", "10.66.77.128/25", "10.4.76.0/24", "10.9.76.0/24", "10.21.76.0/24", "10.61.76.0/24", "10.17.76.0/24"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
      rules = [{
        protocol = "tcp"
        ports    = ["3389"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "150"
      }
    },
    "fw-hive-vpc-150-i-a-zgn-gcp-ssh" = {
      description          = "Allow ingress for zgn-gcp-ssh"
      direction            = "INGRESS"
      action               = "allow"
      ranges               = ["10.1.76.0/23", "10.35.76.0/24", "10.6.76.0/24", "10.66.240.32/27", "10.66.76.0/24", "10.77.240.32/27", "10.77.76.0/24", "10.80.76.0/24", "10.63.76.0/24", "10.6.240.32/27", "10.35.240.32/27", "10.66.77.128/25", "10.4.76.0/24", "10.9.76.0/24", "10.21.76.0/24", "10.61.76.0/24", "10.17.76.0/24"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
      rules = [{
        protocol = "tcp"
        ports    = ["22"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "150"
      }
    },
    "fw-hive-vpc-350-e-a-zgn-sep-servers" = {
      description          = "Allow ingress for zgn-sep-servers"
      direction            = "EGRESS"
      action               = "allow"
      ranges               = ["10.3.1.88", "10.3.0.114"]
      sources              = null
      use_service_accounts = false
      targets              = ["non-prod"]
      rules = [{
        protocol = "tcp"
        ports    = ["80", "8014"]
      }]
      extra_attributes = {
        flow_logs          = true,
        flow_logs_metadata = "INCLUDE_ALL_METADATA",
        priority           = "350"
      }
    }
  }
} 