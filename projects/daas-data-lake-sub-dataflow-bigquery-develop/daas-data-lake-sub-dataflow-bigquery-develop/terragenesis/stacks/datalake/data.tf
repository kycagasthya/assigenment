data "terraform_remote_state" "infrastructure" {
  backend = "gcs"
  config = {
    bucket = "${var.project}-state"
    prefix = "infrastructure/state"
  }
}
