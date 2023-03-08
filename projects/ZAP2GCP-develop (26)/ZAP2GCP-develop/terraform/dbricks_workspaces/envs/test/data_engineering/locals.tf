locals {
  service_account_email = tolist([
    "serviceAccount:${google_service_account.test_gcs_admin_sa.email}",
    "serviceAccount:${google_service_account.test_gcs_reader_sa.email}"
  ])
}


locals {
  group_and_sa_email_access = tolist([
    "group:gcds-its-zap-de-admin@zebra.com",
    "serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
 ])
}

locals {
  sa_email_access = tolist([
    "serviceAccount:sa-dbx-de-adm-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
  ])
}

locals {
  group_access = tolist([
    "group:gcds-its-zap-de-admin@zebra.com"
  ])
}