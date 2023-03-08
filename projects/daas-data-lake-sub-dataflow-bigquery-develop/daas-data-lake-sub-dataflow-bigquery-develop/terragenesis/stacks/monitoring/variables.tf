variable "project" {
  type        = string
  description = "The ID of the project in which the resource belongs."
}

variable "labels" {
  type        = map(string)
  description = "The labels associated with resources. Used to organize and group different cloud resources."
  default = {
    platform = "google"
  }
}
