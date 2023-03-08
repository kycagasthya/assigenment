## Pipeline Terraform ##

This module aims to create cloudbuild trigger for CICD pipeline.

### Prerequisites ###
1. To run the commands user must have below tools installed:
    - [Git](https://git-scm.com/downloads)
    - [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
    - [Terraform](https://www.terraform.io/downloads.html)
2. The deployer should have permissions on Terraform Service account and State file storage bucket
3. The backend.tf and terraform.tfvars should be reviewed before deployment
4. To get the cloudbuild trigger image run the following commands:
                cd cicd_pipelines/cicd_ops/cloudbuild_builder/
                
   gcloud builds submit --project its-registry-it-kcl-p --impersonate-service-account=quantiphi-terraform-dev@za-global-service-accounts-p.iam.gserviceaccount.com --config cloudbuild.yaml .
5. Get the image and use it in cloudbuild_triggers terraform resource
 


# Cloud Build Terraform #

Below GCP resources are provisioned using this module:
  1. Cloud build Trigger
  2. CICD Docker Image
  
### Terraform CFT/Resource module links ###
For more information on accepted input and outputs please refer below module link to understand the accepted parameters.

1. Cloudbuild Trigger : [Resource](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloudbuild_trigger)

