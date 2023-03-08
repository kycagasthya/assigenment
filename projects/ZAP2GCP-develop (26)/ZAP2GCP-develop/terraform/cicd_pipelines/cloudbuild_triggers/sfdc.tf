/*********************************************************
          Cloud Trigger Build for Dev env
*********************************************************/

resource "google_cloudbuild_trigger" "dev_trigger_sfdc" {
  project     = var.project_id
  name        = "cb-sfdc-d-dbx-trigger"
  description = "Trigger for sfdc repository in dev env"
  github {
    name  = "ZAP2GCP-DE-SFDC"
    owner = "zebratechnologies"
    push {
      branch = "^dev$"
    }
  }

  build {
    step {
      name    = "us-docker.pkg.dev/its-registry-it-kcl-p/zbr-zapdbx-dcr-repo/cicd-utilities:v0.1.0"
      args    = ["sh", "/cicd/pipeline_setup_ops.sh"]
      timeout = "120s"
    }
    step {
      name = "us-docker.pkg.dev/its-registry-it-kcl-p/zbr-zapdbx-dcr-repo/cicd-utilities:v0.1.0"
      args = ["sh", "./cicd/git_delta_ops.sh"]
      env = [
        "PROJECT_ID_SEC=$_PROJECT_ID_SEC",
        "PROJECT_ID_DBX=$_PROJECT_ID_DBX",
        "MOUNT=$_MOUNT",
        "BRANCH=$_BRANCH",
        "INSTANCE_ID=$_INSTANCE_ID",
        "GIT_SEC_ID=$_GIT_SEC_ID",
        "GIT_VER_ID=$_GIT_VER_ID",
        "REPO_NAME=$_REPO_NAME",
        "OWNER=$_OWNER"
      ]
      timeout = "120s"
    }
    step {
      name = "us-docker.pkg.dev/its-registry-it-kcl-p/zbr-zapdbx-dcr-repo/cicd-utilities:v0.1.0"
      args = ["sh", "./cicd/dbx_job_ops.sh"]
      env = [
        "PROJECT_ID_SEC=$_PROJECT_ID_SEC",
        "PROJECT_ID_DBX=$_PROJECT_ID_DBX",
        "MOUNT=$_MOUNT",
        "BRANCH=$_BRANCH",
        "INSTANCE_ID=$_INSTANCE_ID",
        "API_VERSION=$_API_VERSION",
        "DB_SEC_ID=$_DB_SEC_ID",
        "DB_VER_ID=$_DB_VER_ID",
        "DB_SVC=$_DB_SVC",
        "REPO_NAME=$_REPO_NAME",
        "HIVE_META_IP=$_HIVE_META_IP"
      ]
      timeout = "120s"
    }
    step {
      name = "us-docker.pkg.dev/its-registry-it-kcl-p/zbr-zapdbx-dcr-repo/cicd-utilities:v0.1.0"
      args = ["sh", "./cicd/comp_dag_ops.sh"]
      env = [
        "PROJECT_ID_SEC=$_PROJECT_ID_SEC",
        "PROJECT_ID_DBX=$_PROJECT_ID_DBX",
        "MOUNT=$_MOUNT",
        "BRANCH=$_BRANCH",
        "INSTANCE_ID=$_INSTANCE_ID",
        "API_VERSION=$_API_VERSION",
        "DB_SEC_ID=$_DB_SEC_ID",
        "DB_VER_ID=$_DB_VER_ID",
        "DB_SVC=$_DB_SVC",
        "DAG_BUCKET=$_DAG_BUCKET",
        "REPO_NAME=$_REPO_NAME",
        "HIVE_META_IP=$_HIVE_META_IP"
      ]
      timeout = "120s"
    }
    logs_bucket = module.cb_log_bucket.name
  }

  tags = ["ZAP2GCP-DE-SFDC", "sfdc", "dev"]

  substitutions = {
    _PROJECT_ID_SEC = "its-registry-it-kcl-p"
    _PROJECT_ID_DBX = "its-managed-dbx-zap-d"
    _MOUNT          = "its-managed-dbx-zap-d-pipeline-code"
    _BRANCH         = "dev"
    _INSTANCE_ID    = "1235921161438059.9.gcp.databricks.com"
    _API_VERSION    = "/api/2.1"
    _DB_SEC_ID      = "zbr-dev-itdedbx-secret"
    _DB_VER_ID      = "latest"
    _GIT_SEC_ID     = "zbr-itdedbx-git-secret"
    _GIT_VER_ID     = "latest"
    _DB_SVC         = "sa-gke-gcs-object-admin@its-managed-dbx-zap-d.iam.gserviceaccount.com"
    _REPO_NAME      = "ZAP2GCP-DE-SFDC"
    _DAG_BUCKET     = "us-central1-cmpr-zapdbx-usc-157ef630-bucket"
    _OWNER          = "zebratechnologies"
    _HIVE_META_IP = "10.176.11.88"
  }
  depends_on = [
    module.cb_log_bucket
  ]
}

/*********************************************************
          Cloud Trigger Build for Test env
*********************************************************/

resource "google_cloudbuild_trigger" "test_trigger_sfdc" {
  project     = var.project_id
  name        = "cb-sfdc-t-dbx-trigger"
  description = "Trigger for sfdc repository in test env"

  github {
    name  = "ZAP2GCP-DE-SFDC"
    owner = "zebratechnologies"
    push {
      branch = "^test$"
    }
  }

  build {
    step {
      name    = "us-docker.pkg.dev/its-registry-it-kcl-p/zbr-zapdbx-dcr-repo/cicd-utilities:v0.1.0"
      args    = ["sh", "/cicd/pipeline_setup_ops.sh"]
      timeout = "120s"
    }
    step {
      name = "us-docker.pkg.dev/its-registry-it-kcl-p/zbr-zapdbx-dcr-repo/cicd-utilities:v0.1.0"
      args = ["sh", "./cicd/git_delta_ops.sh"]
      env = [
        "PROJECT_ID_SEC=$_PROJECT_ID_SEC",
        "PROJECT_ID_DBX=$_PROJECT_ID_DBX",
        "MOUNT=$_MOUNT",
        "BRANCH=$_BRANCH",
        "INSTANCE_ID=$_INSTANCE_ID",
        "GIT_SEC_ID=$_GIT_SEC_ID",
        "GIT_VER_ID=$_GIT_VER_ID",
        "REPO_NAME=$_REPO_NAME",
        "OWNER=$_OWNER"
      ]
      timeout = "120s"
    }
    step {
      name = "us-docker.pkg.dev/its-registry-it-kcl-p/zbr-zapdbx-dcr-repo/cicd-utilities:v0.1.0"
      args = ["sh", "./cicd/dbx_job_ops.sh"]
      env = [
        "PROJECT_ID_SEC=$_PROJECT_ID_SEC",
        "PROJECT_ID_DBX=$_PROJECT_ID_DBX",
        "MOUNT=$_MOUNT",
        "BRANCH=$_BRANCH",
        "INSTANCE_ID=$_INSTANCE_ID",
        "API_VERSION=$_API_VERSION",
        "DB_SEC_ID=$_DB_SEC_ID",
        "DB_VER_ID=$_DB_VER_ID",
        "DB_SVC=$_DB_SVC",
        "REPO_NAME=$_REPO_NAME",
        "HIVE_META_IP=$_HIVE_META_IP"
      ]
      timeout = "120s"
    }
    step {
      name = "us-docker.pkg.dev/its-registry-it-kcl-p/zbr-zapdbx-dcr-repo/cicd-utilities:v0.1.0"
      args = ["sh", "./cicd/comp_dag_ops.sh"]
      env = [
        "PROJECT_ID_SEC=$_PROJECT_ID_SEC",
        "PROJECT_ID_DBX=$_PROJECT_ID_DBX",
        "MOUNT=$_MOUNT",
        "BRANCH=$_BRANCH",
        "INSTANCE_ID=$_INSTANCE_ID",
        "API_VERSION=$_API_VERSION",
        "DB_SEC_ID=$_DB_SEC_ID",
        "DB_VER_ID=$_DB_VER_ID",
        "DB_SVC=$_DB_SVC",
        "DAG_BUCKET=$_DAG_BUCKET",
        "REPO_NAME=$_REPO_NAME",
        "HIVE_META_IP=$_HIVE_META_IP"
      ]
      timeout = "120s"
    }
    logs_bucket = module.cb_log_bucket.name
  }

  tags = ["ZAP2GCP-DE-SFDC", "sfdc", "test"]


  substitutions = {
    _PROJECT_ID_SEC = "its-registry-it-kcl-p"
    _PROJECT_ID_DBX = "its-managed-dbx-de-01-t"
    _MOUNT          = "its-managed-dbx-de-01-t-pipeline-code"
    _BRANCH         = "test"
    _INSTANCE_ID    = "188879976212547.7.gcp.databricks.com"
    _API_VERSION    = "/api/2.1"
    _DB_SEC_ID      = "zbr-test-itdedbx-secret"
    _DB_VER_ID      = "latest"
    _GIT_SEC_ID     = "zbr-itdedbx-git-secret"
    _GIT_VER_ID     = "latest"
    _DB_SVC         = "sa-gke-gcs-object-admin-t@its-managed-dbx-de-01-t.iam.gserviceaccount.com"
    _REPO_NAME      = "ZAP2GCP-DE-SFDC"
    _DAG_BUCKET     = "us-central1-cmpr-zapdbx-usc-157ef630-bucket"
    _OWNER          = "zebratechnologies"
    _HIVE_META_IP = "10.176.11.88"
  }
  depends_on = [
    module.cb_log_bucket
  ]
}

/*********************************************************
          Cloud Trigger Build for Prod env
*********************************************************/
resource "google_cloudbuild_trigger" "prod_trigger_sfdc" {
  project     = var.project_id
  name        = "cb-sfdc-p-dbx-trigger"
  description = "Trigger for sfdc repository in prod env"

  github {
    name  = "ZAP2GCP-DE-SFDC"
    owner = "zebratechnologies"
    push {
      branch = "^prod$"
    }
  }

  build {
    step {
      name    = "us-docker.pkg.dev/its-registry-it-kcl-p/zbr-zapdbx-dcr-repo/cicd-utilities:v0.1.0"
      args    = ["sh", "/cicd/pipeline_setup_ops.sh"]
      timeout = "120s"
    }
    step {
      name = "us-docker.pkg.dev/its-registry-it-kcl-p/zbr-zapdbx-dcr-repo/cicd-utilities:v0.1.0"
      args = ["sh", "./cicd/git_delta_ops.sh"]
      env = [
        "PROJECT_ID_SEC=$_PROJECT_ID_SEC",
        "PROJECT_ID_DBX=$_PROJECT_ID_DBX",
        "MOUNT=$_MOUNT",
        "BRANCH=$_BRANCH",
        "INSTANCE_ID=$_INSTANCE_ID",
        "GIT_SEC_ID=$_GIT_SEC_ID",
        "GIT_VER_ID=$_GIT_VER_ID",
        "REPO_NAME=$_REPO_NAME",
        "OWNER=$_OWNER",
        "CURRENT_TAG=$_CURRENT_TAG",
        "HARD_ROLLBACK=False",
        "GIT_USER=$_GIT_USER"
      ]
      timeout = "120s"
    }
    step {
      name = "us-docker.pkg.dev/its-registry-it-kcl-p/zbr-zapdbx-dcr-repo/cicd-utilities:v0.1.0"
      args = ["sh", "./cicd/dbx_job_ops.sh"]
      env = [
        "PROJECT_ID_SEC=$_PROJECT_ID_SEC",
        "PROJECT_ID_DBX=$_PROJECT_ID_DBX",
        "MOUNT=$_MOUNT",
        "BRANCH=$_BRANCH",
        "INSTANCE_ID=$_INSTANCE_ID",
        "API_VERSION=$_API_VERSION",
        "DB_SEC_ID=$_DB_SEC_ID",
        "DB_VER_ID=$_DB_VER_ID",
        "DB_SVC=$_DB_SVC",
        "REPO_NAME=$_REPO_NAME",
        "CURRENT_TAG=$_CURRENT_TAG",
        "HARD_ROLLBACK=False",
        "HIVE_META_IP=$_HIVE_META_IP"
      ]
      timeout = "120s"
    }
    step {
      name = "us-docker.pkg.dev/its-registry-it-kcl-p/zbr-zapdbx-dcr-repo/cicd-utilities:v0.1.0"
      args = ["sh", "./cicd/comp_dag_ops.sh"]
      env = [
        "PROJECT_ID_SEC=$_PROJECT_ID_SEC",
        "PROJECT_ID_DBX=$_PROJECT_ID_DBX",
        "MOUNT=$_MOUNT",
        "BRANCH=$_BRANCH",
        "INSTANCE_ID=$_INSTANCE_ID",
        "API_VERSION=$_API_VERSION",
        "DB_SEC_ID=$_DB_SEC_ID",
        "DB_VER_ID=$_DB_VER_ID",
        "DB_SVC=$_DB_SVC",
        "DAG_BUCKET=$_DAG_BUCKET",
        "REPO_NAME=$_REPO_NAME",
        "CURRENT_TAG=$_CURRENT_TAG",
        "HARD_ROLLBACK=False",
        "HIVE_META_IP=$_HIVE_META_IP"
      ]
      timeout = "120s"
    }
    logs_bucket = module.cb_log_bucket.name
  }
  tags = ["ZAP2GCP-DE-SFDC", "sfdc", "prod"]
  lifecycle {
    ignore_changes = [github]
  }

  substitutions = {
    _PROJECT_ID_SEC = "its-registry-it-kcl-p"
    _PROJECT_ID_DBX = "its-managed-dbx-de-01-p"
    _MOUNT          = "its-managed-dbx-de-01-p-pipeline-code"
    _BRANCH         = "prod"
    _INSTANCE_ID    = "1659180362012466.6.gcp.databricks.com"
    _API_VERSION    = "/api/2.1"
    _DB_SEC_ID      = "zbr-prod-itdbxbatch-secret"
    _DB_VER_ID      = "latest"
    _GIT_SEC_ID     = "zbr-itdedbx-git-secret"
    _GIT_VER_ID     = "latest"
    _DB_SVC         = "sa-prod-gke-gcs-object-admin@its-managed-dbx-de-01-p.iam.gserviceaccount.com"
    _REPO_NAME      = "ZAP2GCP-DE-SFDC"
    _DAG_BUCKET     = "us-central1-cmpr-zapdbx-usc-0501ed27-bucket"
    _OWNER          = "zebratechnologies"
    _CURRENT_TAG    = "0.0"
    _GIT_USER       = "itdedbxgit"
    _HIVE_META_IP   = "10.176.11.68"
  }
  depends_on = [
    module.cb_log_bucket
  ]
}


/*********************************************************
          Rollback Trigger
*********************************************************/
/*
resource "google_cloudbuild_trigger" "prod_rollback_trigger_sfdc" {
  project     = var.project_id
  name        = "cb-sfdc-p-rollback-dbx-trigger "
  description = "Trigger for sfdc repository for rollback in prod env"

  github {
    name  = "ZAP2GCP-DE-SFDC"
    owner = "zebratechnologies"
    push {
      branch = "^prod$"
    }
  }

  build {
    step {
      name    = "us-docker.pkg.dev/its-registry-it-kcl-p/zbr-zapdbx-dcr-repo/cicd-utilities:v0.1.0"
      args    = ["sh", "/cicd/pipeline_setup_ops.sh"]
      timeout = "120s"
    }
    step {
      name = "us-docker.pkg.dev/its-registry-it-kcl-p/zbr-zapdbx-dcr-repo/cicd-utilities:v0.1.0"
      args = ["sh", "./cicd/git_delta_ops.sh"]
      env = [
        "PROJECT_ID_SEC=$_PROJECT_ID_SEC",
        "PROJECT_ID_DBX=$_PROJECT_ID_DBX",
        "MOUNT=$_MOUNT",
        "BRANCH=$_BRANCH",
        "INSTANCE_ID=$_INSTANCE_ID",
        "GIT_SEC_ID=$_GIT_SEC_ID",
        "GIT_VER_ID=$_GIT_VER_ID",
        "REPO_NAME=$_REPO_NAME",
        "OWNER=$_OWNER",
        "HARD_ROLLBACK=$_HARD_ROLLBACK"
      ]
      timeout = "120s"
    }
    step {
      name = "us-docker.pkg.dev/its-registry-it-kcl-p/zbr-zapdbx-dcr-repo/cicd-utilities:v0.1.0"
      args = ["sh", "./cicd/dbx_job_ops.sh"]
      env = [
        "PROJECT_ID_SEC=$_PROJECT_ID_SEC",
        "PROJECT_ID_DBX=$_PROJECT_ID_DBX",
        "MOUNT=$_MOUNT",
        "BRANCH=$_BRANCH",
        "INSTANCE_ID=$_INSTANCE_ID",
        "API_VERSION=$_API_VERSION",
        "DB_SEC_ID=$_DB_SEC_ID",
        "DB_VER_ID=$_DB_VER_ID",
        "DB_SVC=$_DB_SVC",
        "REPO_NAME=$_REPO_NAME",
        "HARD_ROLLBACK=$_HARD_ROLLBACK",
        "HIVE_META_IP=$_HIVE_META_IP"
      ]
      timeout = "120s"
    }
    step {
      name = "us-docker.pkg.dev/its-registry-it-kcl-p/zbr-zapdbx-dcr-repo/cicd-utilities:v0.1.0"
      args = ["sh", "./cicd/comp_dag_ops.sh"]
      env = [
        "PROJECT_ID_SEC=$_PROJECT_ID_SEC",
        "PROJECT_ID_DBX=$_PROJECT_ID_DBX",
        "MOUNT=$_MOUNT",
        "BRANCH=$_BRANCH",
        "INSTANCE_ID=$_INSTANCE_ID",
        "API_VERSION=$_API_VERSION",
        "DB_SEC_ID=$_DB_SEC_ID",
        "DB_VER_ID=$_DB_VER_ID",
        "DB_SVC=$_DB_SVC",
        "DAG_BUCKET=$_DAG_BUCKET",
        "REPO_NAME=$_REPO_NAME",
        "HARD_ROLLBACK=$_HARD_ROLLBACK",
        "HIVE_META_IP=$_HIVE_META_IP"
      ]
      timeout = "120s"
    }
    logs_bucket = module.cb_log_bucket.name
  }
  tags = ["ZAP2GCP-DE-SFDC", "sfdc", "prod", "rollback"]
  lifecycle {
    ignore_changes = [github]
  }

  substitutions = {
    _PROJECT_ID_SEC = "its-registry-it-kcl-p"
    _PROJECT_ID_DBX = "its-managed-dbx-de-01-p"
    _MOUNT          = "its-managed-dbx-de-01-p-pipeline-code"
    _BRANCH         = "prod"
    _INSTANCE_ID    = "1659180362012466.6.gcp.databricks.com"
    _API_VERSION    = "/api/2.1"
    _DB_SEC_ID      = "zbr-prod-itdbxbatch-secret"
    _DB_VER_ID      = "latest"
    _GIT_SEC_ID     = "zbr-itdedbx-git-secret"
    _GIT_VER_ID     = "latest"
    _DB_SVC         = "sa-prod-gke-gcs-object-admin@its-managed-dbx-de-01-p.iam.gserviceaccount.com"
    _REPO_NAME      = "ZAP2GCP-DE-SFDC"
    _DAG_BUCKET     = "us-central1-cmpr-zapdbx-usc-0501ed27-bucket"
    _OWNER          = "zebratechnologies"
    _HARD_ROLLBACK  = False
    _HIVE_META_IP = "10.176.11.68"
  }

  depends_on = [
    module.cb_log_bucket
  ]
}
*/

