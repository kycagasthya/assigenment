## Non-Production networking ##

This folder allows you to deploy non-production networking components(Hive metastore vpc,private service access,firewall rules and the network connectivity from Databricks VPC to Hive CloudSQL Instance for non production centralized hive metastore.

### Prerequisites ###
1. To run the commands user must have below tools installed:
    - [Git](https://git-scm.com/downloads)
    - [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
    - [Terraform](https://www.terraform.io/downloads.html)
2. The deployer should have following role on the Terraform service account
   Service Account Token Creator
3. The backend.tf and terraform.tfvars should be reviewed before deployment
4. Validate the CIDR Range for Subnetwork, and Service networking range

### Terraform CFT/Resource module links ###
For more information on accepted input and outputs please refer below module link to understand the accepted parameters.

1. Firewall rules module : [CFT](https://github.com/terraform-google-modules/terraform-google-network/tree/master/modules/fabric-net-firewall)
2. Hive metastore vpc: [CFT](https://github.com/terraform-google-modules/terraform-google-network)
3. Private Service Access : [CFT](https://github.com/terraform-google-modules/terraform-google-sql-db/tree/master/modules/mysql)
4. VPC Peering: [CFT](https://github.com/terraform-google-modules/terraform-google-network/tree/master/modules/network-peering)
5. NAT compute router : [Resource](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_router)
6. NAT compute address: [Resource](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_address)

