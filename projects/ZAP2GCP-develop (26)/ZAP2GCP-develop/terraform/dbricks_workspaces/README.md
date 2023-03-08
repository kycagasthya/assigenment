## Databricks Workspace Terraform ##

This module should be used to provision supporting infrastructure for Databricks workspaces such as GCP Service Accounts, Cloud Storage, IAM Bindings, etc. The folders can further be segregated within different environment folder(dev, test, prod) Data Engineers, etc.

### Prerequisites ###
1. To run the commands user must have below tools installed:
    - [Git](https://git-scm.com/downloads)
    - [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
    - [Terraform](https://www.terraform.io/downloads.html)
2. The deployer should have permissions on Terraform Service account and State file storage bucket
3. The backend.tf and terraform.tfvars should be reviewed before deployment