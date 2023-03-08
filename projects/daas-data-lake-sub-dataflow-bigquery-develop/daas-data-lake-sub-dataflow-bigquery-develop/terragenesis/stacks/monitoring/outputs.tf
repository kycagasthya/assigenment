output "opsgenie" {
  value = data.terraform_remote_state.infrastructure.outputs.opsgenie_channel
}