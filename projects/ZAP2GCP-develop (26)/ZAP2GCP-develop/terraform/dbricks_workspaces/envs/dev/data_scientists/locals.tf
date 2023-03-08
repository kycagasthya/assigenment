locals {
  service_account_email = tolist([
    "serviceAccount:${google_service_account.dev_gcs_admin_sa.email}"
  ])
}

locals {
  group_and_sa_email_access = tolist([
    "group:gcds-its-zap-goas-ds-sec-fin-engineers@zebra.com",	
    "group:gcds-its-zap-goas-ds-sec-fin-scientists@zebra.com",	
    "group:gcds-its-zap-goas-ds-sec-fin-analysts@zebra.com",	
    "group:gcds-its-zap-glo-engineers@zebra.com",	
    "group:gcds-its-zap-glo-analysts@zebra.com",
    "group:gcds-its-zap-glo-scientists@zebra.com",	
    "group:gcds-its-zap-goas-scientists@zebra.com",	
    "group:gcds-its-zap-goas-enginners@zebra.com",	
    "group:gcds-its-zap-goas-analysts@zebra.com",	
    "group:gcds-its-zap-fin-scientists@zebra.com",	
    "group:gcds-its-zap-fin-enginners@zebra.com",	
    "group:gcds-its-zap-fin-analysts@zebra.com",
    "serviceAccount:sa-dbx-goassecfin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goassecfin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goassecfin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",  
    "serviceAccount:sa-dbx-glo-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-glo-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-glo-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",  
    "serviceAccount:sa-dbx-goas-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goas-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goas-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",  
    "serviceAccount:sa-dbx-fin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-fin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-fin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
 ])
}

locals {
  sa_email_access = tolist([
    "serviceAccount:sa-dbx-goassecfin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",
    "serviceAccount:sa-dbx-goassecfin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goassecfin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",  
    "serviceAccount:sa-dbx-glo-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-glo-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-glo-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",  
    "serviceAccount:sa-dbx-goas-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goas-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-goas-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com",  
    "serviceAccount:sa-dbx-fin-de-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-fin-ds-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com", 
    "serviceAccount:sa-dbx-fin-da-d@its-managed-dbx-ds-01-d.iam.gserviceaccount.com"
  ])
}

locals {
  group_access = tolist([
    "group:gcds-its-zap-de-admin@zebra.com",
    "group:gcds-its-zap-goas-ds-sec-fin-engineers@zebra.com",	
    "group:gcds-its-zap-goas-ds-sec-fin-scientists@zebra.com",	
    "group:gcds-its-zap-goas-ds-sec-fin-analysts@zebra.com",	
    "group:gcds-its-zap-glo-engineers@zebra.com",	
    "group:gcds-its-zap-glo-analysts@zebra.com",
    "group:gcds-its-zap-glo-scientists@zebra.com",	
    "group:gcds-its-zap-goas-scientists@zebra.com",	
    "group:gcds-its-zap-goas-enginners@zebra.com",	
    "group:gcds-its-zap-goas-analysts@zebra.com",	
    "group:gcds-its-zap-fin-scientists@zebra.com",	
    "group:gcds-its-zap-fin-enginners@zebra.com",	
    "group:gcds-its-zap-fin-analysts@zebra.com"
  ])
}