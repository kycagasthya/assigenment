
output "bucket_name" {
  description = "Cloud sql Bucket name."
  value       = module.np_operations.bucket_name
}

output "instance_name" {
  description = "The instance name for the master instance"
  value       = module.np_operations.instance_name
}

output "instance_ip_address" {
  description = "The IPv4 address assigned for the master instance"
  value       = module.np_operations.instance_ip_address
}

output "instance_connection_name" {
  description = "The connection name of the master instance to be used in connection strings"
  value       = module.np_operations.instance_connection_name
}

output "template_self_link" {
  description = "Self-link of instance template"
  value       = module.np_operations.template_self_link
}

output "template_name" {
  description = "Name of instance template"
  value       = module.np_operations.template_name
}

output "mig_self_link" {
  description = "Self-link of managed instance group"
  value       = module.np_operations.mig_self_link
}

output "instance_group" {
  description = "Instance-group url of managed instance group"
  value       = module.np_operations.instance_group
}

output "health_check_self_links" {
  description = "All self_links of healthchecks created for the instance group."
  value       = module.np_operations.health_check_self_links
}

output "composer_env_name" {
  description = "Name of the Cloud Composer Environment."
  value       = module.np_operations.composer_env_name
}

output "composer_env_id" {
  description = "ID of Cloud Composer Environment."
  value       = module.np_operations.composer_env_id
}

output "gke_cluster" {
  description = "Google Kubernetes Engine cluster used to run the Cloud Composer Environment."
  value       = module.np_operations.gke_cluster
}

output "gcs_bucket" {
  description = "Google Cloud Storage bucket which hosts DAGs for the Cloud Composer Environment."
  value       = module.np_operations.gcs_bucket
}

output "airflow_uri" {
  description = "URI of the Apache Airflow Web UI hosted within the Cloud Composer Environment."
  value       = module.np_operations.airflow_uri
}