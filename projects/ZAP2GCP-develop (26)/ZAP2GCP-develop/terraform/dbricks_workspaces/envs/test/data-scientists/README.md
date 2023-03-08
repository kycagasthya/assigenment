## Databricks Test DE Workspace ##

This folder helps provision the additional infrastructure required in the Data Engineering workspace project for Databricks. It consists of Cloud Storage buckets for delta tables and landing zone(SFDC,EOL,PLANIB) in test environment. Along with Buckets, two Service Accounts would be created for testing Databricks clusters and the permissions granted to them via GCP IAM Binding.


## Databricks VPC hardening ##

This folder also helps with the provision of hardening the databricks VPC environment by denying all the traffic and adding explicit firewall rules, VPC routes and creating Private DNS zones in the VPC environment.


### Prerequisites ###
1. To run the commands user must have below tools installed:
    - [Git](https://git-scm.com/downloads)
    - [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
    - [Terraform](https://www.terraform.io/downloads.html)
2. The deployer should have permissions on Terraform Service account and State file storage bucket
3. The backend.tf and terraform.tfvars should be reviewed before deployment

### Terraform CFT/Resource module links ###
For more information on accepted input and outputs please refer below module link to understand the accepted parameters.

1. Google cloud storage module : [CFT](https://github.com/terraform-google-modules/cloud-foundation-fabric/tree/master/modules/gcs)
2. Service account creation : [Resource](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/google_service_account)
3. Project IAM bindings : [Resource](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/google_project_iam)
4. Compute Network Firewall module: [CFT] (https://github.com/terraform-google-modules/terraform-google-network//modules/fabric-net-firewall)
5. VPC routes: [CFT] (https://github.com/terraform-google-modules/terraform-google-network//modules/routes)
6. Google Cloud DNS: [CFT] (https://github.com/terraform-google-modules/terraform-google-cloud-dns)

