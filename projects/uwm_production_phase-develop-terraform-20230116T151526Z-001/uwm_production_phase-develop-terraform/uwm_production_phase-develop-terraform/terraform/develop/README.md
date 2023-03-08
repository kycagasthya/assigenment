#### Common Terraform files
1. backend.tf - Define location to store Terraform state file remotely
2. locals.tf - Define Terraform local variables
3. data.tf - Define Terraform remote state file location
4. variables.tf - Declare Terraform variable
5. outputs.tf - Outputs the attributes of resources created by Terraform
6. terraform.tfvars - Define values for Terraform variables

### Usage
#### Install Git
To use Github as a source for Terraform modules, install git packages on the system:
```
sudo apt install git
```
#### Install Terraform
Install Terraform on the system:
```
UBUNTU

curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install terraform

OR

export TF_VERSION=0.13.5
wget \
https://releases.hashicorp.com/terraform/${TF_VERSION}/terraform_${TF_VERSION}_linux_amd64.zip

sudo unzip terraform_${TF_VERSION}_linux_amd64.zip -d /usr/local/bin/

terraform --version
```
#### Setup GCP credentials
Configure the authentication before deploying the GCP resources using Terraform. Terraform provides various [options](https://www.terraform.io/docs/providers/google/guides/provider_reference.html#full-reference) to authenticate itself with GCP.

The recommendation is to use GCP environment variables:

```
export GOOGLE_CREDENTIALS=/path/to/serviceaccount.json
```

Note: Do not store the Service Account keyfile inside local repository folder as it may happen that it gets published in one of the commits.

#### Executing Terraform
Based on the validation of above steps the Terraform configuration files can be executed, the resources are organized under different file/folder structure, each having its own seperate [Terraform state file](https://www.terraform.io/docs/state/index.html) defined in the `backend.tf` file

To perform an operation on a given resource, follow the below procedure:
1. Change Directory
2. Create a binary plan file, and text plan file
3. Review the text plan file
4. If valid, execute the binary plan file

##### Example
```
cd foundations

terraform plan -out=tf_bin_plan.bin -no-color > tf_txt_plan.txt
(Validate text plan file, tf_txt_plan.txt)

terraform apply -auto-approve tf_bin_plan.bin
(If valid, execute binary file, tf_bin_plan.bin)
```
