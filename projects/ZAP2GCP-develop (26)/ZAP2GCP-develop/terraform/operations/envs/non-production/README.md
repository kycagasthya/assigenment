## Non-Production operations ##

This folder allows you to deploy non-production operations components required to host CloudSQL proxy and CloudSQL instance for non-production centralized Hive metastore.

### Prerequisites ###
1. To run the commands user must have below tools installed:
    - [Git](https://git-scm.com/downloads)
    - [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
    - [Terraform](https://www.terraform.io/downloads.html)
2. The deployer should have permissions on Terraform Service account and State file storage bucket
3. The backend.tf and terraform.tfvars should be reviewed before deployment
4. Download CloudSQL Binary in the current working directory, refer following command:

   `wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy`
### Terraform CFT/Resource module links ###
For more information on accepted input and outputs please refer below module link to understand the accepted parameters.

1. Hive metastore cloudsql : [CFT](https://github.com/terraform-google-modules/terraform-google-sql-db/blob/master/examples/mysql-ha)
2. Service Account : [Resource](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/google_service_account)
3. Service Account IAM Binding : [Resource](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/google_service_account_iam)
4. Project IAM Binding : [Resource](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/google_project_iam)
5. Cloud storage bucket : [CFT](https://github.com/terraform-google-modules/cloud-foundation-fabric/tree/master/modules/gcs?ref=v5.1.0)
6. Storage object in bucket : [Resource](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket_object)

7. Cloud sql proxy instance template : [CFT](https://github.com/terraform-google-modules/terraform-google-vm/tree/master/modules/instance_template)
8. Cloud sql proxy managed instance group : [Resource](https://github.com/terraform-google-modules
terraform-google-vm/tree/master/modules/mig)
9. Internal Load Balancer Health check : [Resource](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_health_check)
10. Internal Load Balancer Backend : [Resource](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_region_backend_service)
11. Internal Load Balancer Forwarding rule : [Resource](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_forwarding_rule)
