variable "name" {
  type = string
  description = "give firewall name"
  default = "test"
}

variable "network" {
  type = string
  description = "give network name"
  default = "test-vpc"
}

variable "target_tags" {
  type = list(string)
  description = "give name of tags to attach VM"
  default     = []
}

variable "source_ranges" {
  type = list
  default = []
}

variable "protocol" {
  type = string
  default = "tcp"
}

variable "ports" {
  type = list(string)
  default = ["22", "3389"]
}
