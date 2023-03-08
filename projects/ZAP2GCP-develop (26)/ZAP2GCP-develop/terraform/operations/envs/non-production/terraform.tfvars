terraform_sa_email = "quantiphi-terraform-dev@za-global-service-accounts-p.iam.gserviceaccount.com"

project_id = "its-managed-dbx-edlops-t"
region     = "us-central1"

network_name    = "vpc-np-hive-metastore"
subnetwork_name = "sb-np-hive-metastore-proxy"

sql_instance_name    = "csmy-zapdbx-usc1-t"
random_instance_name = false
enable_default_user  = false
enable_default_db    = false
deletion_protection  = false
user_labels = {
  application         = ""
  application-contact = ""
  bu-manager          = ""
  bu                  = ""
  its-manager         = "ssundaramurthi"
  its-technical       = "kd3759"
  tier                = "non-production"
  cost-center         = ""
}
database_version = "MYSQL_5_7"
zone             = "us-central1-c"
tier             = "db-n1-standard-2"
ip_configuration = {
  "authorized_networks" : [],
  "ipv4_enabled" : false,
  "private_network" : "projects/its-managed-dbx-edlops-t/global/networks/vpc-np-hive-metastore",
  "require_ssl" : true
}
availability_type = "REGIONAL"
backup_configuration = {
  enabled                        = true
  binary_log_enabled             = true
  start_time                     = "20:55"
  location                       = null
  transaction_log_retention_days = null
  retained_backups               = 14
  retention_unit                 = "COUNT"
}
disk_autoresize                 = true
disk_size                       = 10
sql_disk_type                   = "PD_SSD"
maintenance_window_day          = 7
maintenance_window_hour         = 6
maintenance_window_update_track = "stable"

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
cloudsql_bin_path = "./cloud_sql_proxy"

instance_tmplt_prefix       = "cloudsql-proxy"
machine_type                = "n2-standard-2"

source_image_project= "rhel-cloud"
source_image= "rhel-8-v20220519"
source_image_family= "rhel-8"

#source_image_project        = "za-global-golden-images-p"
#source_image                = ""
#source_image_family         = "zeb-rhel-8-callback"
disk_labels                 = {}
disk_size_gb                = 100
instance_template_disk_type = "pd-standard"
enable_shielded_vm          = false
mig_labels = {
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
inst_tmplt_tags = ["non-prod", "sql-proxy"]

mig_name        = "z176st-zapapp01"
hostname_prefix = "z176st-zapapp01"
target_size     = 1
mig_hc_name     = "hc-mig-cloudsql-proxy"
mig_health_check = {
  "check_interval_sec" : 15,
  "healthy_threshold" : 2,
  "host" : "",
  "initial_delay_sec" : 60,
  "port" : 3306,
  "proxy_header" : "NONE",
  "request" : "",
  "request_path" : "/",
  "response" : "",
  "timeout_sec" : 10,
  "type" : "tcp",
  "unhealthy_threshold" : 3
}
distribution_policy_zones = ["us-central1-b"]
update_policy = [{
  max_surge_fixed              = 2
  type                         = "OPPORTUNISTIC"
  instance_redistribution_type = "PROACTIVE"
  minimal_action               = "REPLACE"
  max_surge_percent            = null
  max_unavailable_fixed        = 1
  max_unavailable_percent      = null
  min_ready_sec                = 60
  replacement_method           = "SUBSTITUTE"
}]

health_check_name = "hc-ilb-tcp-cloudsql-proxy"
ilb_health_check = {
  "check_interval_sec" : 10,
  "healthy_threshold" : 3,
  "unhealthy_threshold" : 4,
  "port" : 3306,
  "proxy_header" : "NONE",
  "request" : "",
  "response" : "",
  "timeout_sec" : 5,
}
connection_draining_timeout_sec = 30

backend_name  = "be-ilb-tcp-cloudsql-proxy"
frontend_name = "fe-ilb-tcp-cloudsql-proxy"

#Orchestrator
orchestrator_network_name    = "vpc-np-orchestrator"
orchestrator_subnetwork_name = "sb-np-orchestrator-composer"

cloud_sql_ipv4_cidr              = "10.176.14.0/24"
orchestrator_gke_master_ip_range = "100.120.0.96/28"
orchestrator_pod_range_name      = "pod-range"
orchestrator_svc_range_name      = "svc-range"
web_server_ipv4_cidr             = "10.176.15.0/24"


composer_env_name = "cmpr-zapdbx-usc1-t"
composer_labels = {
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
node_count            = "3"
composer_machine_type = "n1-standard-1"
composer_disk_size    = "100"
composer_tags         = ["non-prod"]
python_version        = "3"
image_version         = "composer-1.17.3-airflow-2.1.2"

pypi_packages = {
  apache-airflow-providers-databricks = ">=2.0.2"
}
env_variables = {
        SENDGRID_MAIL_FROM  = "zedl_operations_nonprod@zebra.com"
        SENDGRID_API_KEY = "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"
		SENDGRID_MAIL_TO = "['barath.srinivasan@zebra.com', 'zedl_data_ops@zebra.com', 'barath.srinivasa@tigeranalytics.com', 'siddharth.bhardw@tigeranalytics.com', 'depak.kurumpan@zebra.com', 'revathi.ganesh@zebra.com', 'vishnu.vijay@zebra.com', 'ramanathan.rajendran@zebra.com', 'arunprasath.viswanathan@zebra.com', 'megha.dhabal@zebra.com', 'ariff.syed@zebra.com']"
		landing_bucket_name_dev = "its-managed-dbx-zap-d-landing-di"
		landing_bucket_name_test = "ts-managed-dbx-zap-t-landing-t"
      }


deploy_maint_gce            = true
airflow_maint_instance_name = "airflow-maintenance-instance"
airflow_maint_labels = {
  bu_owner_manager        = ""
  bu_owner_technical      = ""
  cost_center             = ""
  project_or_product      = ""
  security_agent_exempt   = "all"
  tier                    = ""
  os_hostname             = ""
  access_privileges       = ""
  security_classification = ""
  backup                  = ""
  organization            = ""
}


