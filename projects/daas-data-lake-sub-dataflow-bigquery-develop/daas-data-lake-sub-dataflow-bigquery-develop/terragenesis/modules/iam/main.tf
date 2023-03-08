resource "google_service_account" "service_account" {
  # count        = var.service_account_email == "" ? 1 : 0
  project      = var.project
  account_id   = var.service_account_id
  display_name = var.service_account_description
}

resource "google_project_iam_member" "iam_roles" {
  for_each = toset(var.iam_roles)
  project  = var.project
  role     = each.value
  # member   = var.service_account_email == "" ? "serviceAccount:${google_service_account.service_account[0].email}" : var.service_account_email
  member = "serviceAccount:${google_service_account.service_account.email}"
}
