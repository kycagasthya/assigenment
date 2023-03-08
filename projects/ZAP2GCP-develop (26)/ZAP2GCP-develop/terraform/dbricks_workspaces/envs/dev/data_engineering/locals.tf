locals {
  service_account_email = tolist([
    "serviceAccount:${google_service_account.dev_gcs_admin_sa.email}",
    "serviceAccount:${google_service_account.dev_gcs_reader_sa.email}"
  ])
}

locals {
  custom_bucket_viewer_sa_email = tolist([
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-glo-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "group:gcds-its-zap-mktg-ds-analysts@zebra.com",
    "group:gcds-its-zap-mktg-ds-engineers@zebra.com",
    "group:gcds-its-zap-mktg-ds-scientists@zebra.com",
    "group:gcds-its-zap-goas-scientists@zebra.com",
    "group:gcds-its-zap-goas-enginners@zebra.com",
    "group:gcds-its-zap-goas-analysts@zebra.com",
    "group:gcds-its-zap-glo-engineers@zebra.com",
    "group:gcds-its-zap-glo-analysts@zebra.com",
    "group:gcds-its-zap-glo-scientists@zebra.com"
  ])
}

locals {
  log_writer_dbx_sa_email = tolist([
    "serviceAccount:sa-dbx-de-read-d@its-managed-dbx-zap-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-de-adm-d@its-managed-dbx-zap-d.iam.gserviceaccount.com"
  ])
}

locals {
  sa_security_reviewer_email = tolist([
    "serviceAccount:sa-dbx-mktg-de-d@its-managed-dbx-mktg-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goas-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-glo-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "group:gcds-its-zap-mktg-ds-engineers@zebra.com",
    "group:gcds-its-zap-mktg-ds-scientists@zebra.com",
    "group:gcds-its-zap-mktg-ds-analysts@zebra.com",
    "group:gcds-its-zap-goas-scientists@zebra.com",
    "group:gcds-its-zap-goas-enginners@zebra.com",
    "group:gcds-its-zap-goas-analysts@zebra.com",
    "group:gcds-its-zap-glo-engineers@zebra.com",
    "group:gcds-its-zap-glo-analysts@zebra.com",
    "group:gcds-its-zap-glo-scientists@zebra.com"
  ])
}

  