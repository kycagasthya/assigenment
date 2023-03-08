module "github_pat" {
  source       = "../../modules/secrets"
  secret_name  = "github-private-access-token"
  secret_value = var.github_private_access_token
}
