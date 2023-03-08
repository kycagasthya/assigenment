module "docker_artifact_registry" {
  source     = "./modules/artifact-registry"
  project_id = var.project_id
  location   = "us-east4"
  format     = "DOCKER"
  repository_name  = "uwm_np_dev2_artigactrepo"
    labels = {
        env      = "dev"
        billable = "true"
      }
}

module "service-account1" {
  source            = "./modules/iam-service-account"
  project_id        = var.project_id
  account_id        = "test-terraform"
  display_name      = "test-terraform"
}

module "bucket" {
  source     = "./modules/gcs"
  project_id = var.project_id
  prefix     = "uwm"
  name       = "test-bucket"
  location   = "US"
}

module "firestore_claasification" {
  source       = "./modules/firestore"
  project_id   = var.project_id
  collection   = "classification"
  document_id  = "collection"
}

module "firestore_entityextraction" {
  source       = "./modules/firestore"
  project_id   = var.project_id
  collection   = "entityextraction"
  document_id  = "collection"
}

module "pubsub_topic1" {
  source              = "./modules/pubsub-topic"
  project_id          = var.project_id
  pubsub_topic_name   = "uwm-classifcation-topic1"
  topic_labels = {
        env      = "dev"
        billable = "true"
      }
}

module "pubsub_subscription1" {
  source                     = "./modules/pubsub-subscription"
  project_id                 = var.project_id
  pubsub_subscription_name   = "uwm-classifcation-sub1"
  topic_name                 = module.pubsub_topic1.pubsub_topic_name  
}

module "pubsub-gcs-trigger" {
  source                     = "./modules/notification-trigger"
  project_id                 = var.project_id
  bucket_name                = module.bucket.name
  topic_name                 = module.pubsub_topic1.pubsub_topic_name
}
 module "bigquery" {
  source  = "terraform-google-modules/bigquery/google"
  version = "~> 4.4"
 
  dataset_id                  = "uwm_np_dev2_bq"
  dataset_name                = "uwm_np_dev2_bq"
  description                 = "big query for dev2 project"
  project_id                  = var.project_id
  location                    = "US"
  default_table_expiration_ms = 3600000
  tables = [
    {
      table_id = "classification",
      schema   = "./bqjson/classification.json",
      time_partitioning = {
        type                     = "DAY",
        field                    = null,
        require_partition_filter = false,
        expiration_ms            = null,
      },
      expiration_time = null,
      clustering      = []
      labels = {
        env      = "dev"
        billable = "true"
      },
    },
    {
      table_id = "entity_extraction",
      schema   = "./bqjson/entity_extraction.json",
      time_partitioning = {
        type                     = "DAY",
        field                    = null,
        require_partition_filter = false,
        expiration_ms            = null,
      },
      expiration_time = null,
      clustering      = []
      labels = {
        env      = "dev"
        billable = "true"
      },
    },
  ]
  dataset_labels = {
    env      = "dev"
    billable = "true"
  }
}

module "gke" {
 source                    = "github.com/terraform-google-modules/terraform-google-kubernetes-engine//modules/private-cluster/"
 project_id                = var.project_id
 name                      = "uwm-np-pvt-cluster"
 regional                  = true
 region                    = "us-east4"
 network                   = var.network
 subnetwork                = var.subnetwork
 ip_range_pods             = var.ip_range_pods
 ip_range_services         = var.ip_range_services
 create_service_account    = false
 service_account           = var.nodepool_service_account
 enable_private_endpoint   = true
 enable_private_nodes      = true
 master_ipv4_cidr_block    = "172.16.0.0/28"
 remove_default_node_pool  = true
 identity_namespace = "enabled"
 initial_node_count = 1
 network_policy = false
 network_project_id = var.host-project-id
 skip_provisioners = true
 master_authorized_networks = [{
    cidr_block   = "10.10.1.14/32"
    display_name = "Test Instance IP"
  }]

 node_pools = [
   {
     name              = "uwm-np-nodepool-01"
     min_count         = 1
     max_count         = 4
     local_ssd_count   = 0
     disk_size_gb      = 100
     disk_type         = "pd-ssd"
     machine_type      = "e2-standard-8"
     image_type        = "COS"
     auto_repair       = true
     auto_upgrade      = true
     service_account   = var.nodepool_service_account
     preemptible       = false
   },
 ]
}
