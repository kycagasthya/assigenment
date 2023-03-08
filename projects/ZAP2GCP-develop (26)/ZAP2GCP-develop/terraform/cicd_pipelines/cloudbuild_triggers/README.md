## Cloud Build Terraform ##

This module aims to create the cloudbuild triggers for cicd pipeline in dev,test and prod environments.

### Prerequisites ###
1. To run the commands user must have below tools installed:
    - [Git](https://git-scm.com/downloads)
    - [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
    - [Terraform](https://www.terraform.io/downloads.html)
2. The deployer should have permissions on Terraform Service account and State file storage bucket
3. The backend.tf and terraform.tfvars should be reviewed before deployment
4. Execute the cloudbuild_builders first before running this module

## Cloud Build Terraform ##

Below GCP resources are provisioned using this module:
  1. Cloud build Trigger
  2. Bucket IAM 

  
### Terraform CFT/Resource module links ###
For more information on accepted input and outputs please refer below module link to understand the accepted parameters.

1. Coudbuild Trigger : [Resource](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloudbuild_trigger)
2. Bucket IAM        : [Resource](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket_iam)
