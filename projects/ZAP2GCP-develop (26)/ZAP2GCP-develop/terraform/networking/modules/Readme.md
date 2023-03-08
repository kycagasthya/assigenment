##  Networking modules ##

This is an opinionated module that allows you to deploy networking resources, following are the resources it can deploy based on inputs recieved:
  1. VPC
  2. Private service Access
  3. Firewall rules
  4. VPC Peering
  5. NAT

### Prerequisites ###
1. To run the commands user must have below tools installed:
    - [Git](https://git-scm.com/downloads)
    - [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
    - [Terraform](https://www.terraform.io/downloads.html)
2. The backend.tf and terraform.tfvars should be reviewed before deployment
3. The deployer should have permissions on Terraform Service account and State file storage bucket

### Terraform CFT/Resource module links ###
For more information on accepted input and outputs please refer below module link to understand the accepted parameters.

1. Firewall rules module : [CFT](https://github.com/terraform-google-modules/terraform-google-network/tree/master/modules/fabric-net-firewall)
2. Hive metastore vpc: [CFT](https://github.com/terraform-google-modules/terraform-google-network)
3. Private Service Access : [CFT](https://github.com/terraform-google-modules/terraform-google-sql-db/tree/master/modules/mysql)
4. VPC Peering: [CFT](https://github.com/terraform-google-modules/terraform-google-network/tree/master/modules/network-peering)
5. NAT compute router : [Resource](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_router)
6. NAT compute address: [Resource](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_address)

