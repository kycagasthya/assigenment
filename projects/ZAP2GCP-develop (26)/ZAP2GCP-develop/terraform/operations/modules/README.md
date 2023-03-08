## Non-Production operations ##

This is an opinionated module that allows you to deploy following operations resources :
  1. Cloud sql instances
  2. Cloud storage bucket
  3. Bucket objects
  4. Instance Template
  5. Managed Instance groups
  6. Load Balancer
  7. Cloud Composer 

### Prerequisites ###
1. To run the commands user must have below tools installed:
    - [Git](https://git-scm.com/downloads)
    - [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
    - [Terraform](https://www.terraform.io/downloads.html)
2. The deployer should have permissions on Terraform Service account and State file storage bucket
3. The backend.tf and terraform.tfvars should be reviewed before deployment

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
11. Internal Load Balancer Forwarding rule : [Resource](https://registry.terraform.io/providers/hashicorp/google/
latest/docs/resources/compute_forwarding_rule)
12. Cloud Composer environment module : [CFT] (https://github.com/terraform-google-modules/terraform-google-composer/tree/master/modules/create_environment)