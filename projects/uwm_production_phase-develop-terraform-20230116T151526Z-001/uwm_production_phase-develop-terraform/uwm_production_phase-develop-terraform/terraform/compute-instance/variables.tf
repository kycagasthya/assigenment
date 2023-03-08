variable "deletion_protection" {
  type        = bool
  description = "delete on protecton of Vm,if set true then we have remove this protection then delete"
  default     = false
}

variable "project_id" {
  type = string
  description = "give project id"
  default = "hostproj"
}


variable "instance_names" {
  type = string
  description = "give compute vm name"
  default = "demo"
}

variable "machine_type" {
  type = string
  description = "give compute vm machine type"
  default = "n1-standard-1"
}
variable "static_private_ip" {
  type = string
  description = "to attch static private IP , which was ealrier created,static private Ip is subnetwork specific"
  default    = ""
# exapmple is static_private_ip = "10.168.0.53"
}
variable "static_public_ip" {
  type = string
  description = "to attch static public IP , which was ealrier created, static public Ip is  region specific"
  default = ""
## exapmple is static_public_ip = "32.168.0.53"
}
variable "tags" {
  type = list(string)
  description = "give name of tags to attach VM"
  default     = []
}
variable "labels" {
  type = map(string)
  description = "vm labels"
  default = {
    environment = "dev"
  }

}
variable "image_name" {
  type = string
  description = "give base image to create comute vm"
  default = "ubuntu-1804-bionic-v20210129"
}
variable "vpc_network" {
  type = string
  description = "give vpc network name"
  default = "test-vpc"
}
variable "zone" {
  type = string
  description = "compute-vm launched zone"
  default = "us-central1-a"
}
variable "subnetwork" {
  type = string
  description = "(optional) describe your variable"
  default = "test-vpc-public-subnet"
}
variable "disk_size" {
  type = number
  description = "vm disk size"
  default = "50"
}
variable "service_account" {
  type = string
  description = "name of the service account attach to vm"
  default = ""
}
