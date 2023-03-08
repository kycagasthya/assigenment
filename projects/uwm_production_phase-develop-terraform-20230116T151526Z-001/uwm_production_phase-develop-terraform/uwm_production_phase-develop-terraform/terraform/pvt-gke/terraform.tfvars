  project_id                 = "hostproj"
  name                       = "gke-pvt-cluster"
  region                     = "us-central1"
  zones                      = ["us-central1-a", "us-central1-b", "us-central1-f"]
  network                    = "test-vpc"
  subnetwork                 = "test-vpc-private-subnet"
  ip_range_pods              = "10.220.0.0/14"
  ip_range_services          = "10.0.0.0/16"
  http_load_balancing        = false
  horizontal_pod_autoscaling = true
  network_policy             = true
  enable_private_endpoint    = true
  enable_private_nodes       = true
  master_ipv4_cidr_block     = "172.16.0.0/28"

  node_pools = [
    {
      name               = "np-01"
      machine_type       = "e2-medium"
      node_locations     = "us-central1-b,us-central1-b"
      min_count          = 1
      max_count          = 3
      local_ssd_count    = 0
      disk_size_gb       = 100
      disk_type          = "pd-standard"
      image_type         = "COS"
      auto_repair        = true
      auto_upgrade       = true
      service_account    = "terraform@hostproj.iam.gserviceaccount.com"
      preemptible        = false
      initial_node_count = 2
    },
  ]

  node_pools_oauth_scopes = {
    all = []

    default-node-pool = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
  }

  node_pools_labels = {
    all = {}

    default-node-pool = {
      default-node-pool = true
    }
  }

  node_pools_metadata = {
    all = {}

    default-node-pool = {
      node-pool-metadata-custom-value = "my-node-pool"
    }
  }

  node_pools_taints = {
    all = []

    default-node-pool = [
      {
        key    = "default-node-pool"
        value  = true
        effect = "PREFER_NO_SCHEDULE"
      },
    ]
  }

  node_pools_tags = {
    all = []

    default-node-pool = [
      "default-node-pool",
    ]
  }

