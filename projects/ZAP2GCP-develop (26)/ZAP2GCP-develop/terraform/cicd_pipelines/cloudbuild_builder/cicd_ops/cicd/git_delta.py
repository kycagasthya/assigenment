import json, re, requests, os
from pathlib import Path
from google.cloud import secretmanager

project_id_sec =os.environ["PROJECT_ID_SEC"]
git_owner =os.environ["OWNER"]
branch = os.environ["BRANCH"]
repo = os.environ["REPO_NAME"]
secret_id = os.environ["GIT_SEC_ID"]
version_id = os.environ["GIT_VER_ID"]


# Create the Secret Manager client.
client = secretmanager.SecretManagerServiceClient()


def access_secret_version(project_id, secret_id, version_id):
    """
    Access the payload for the given secret version if one exists. The version
    can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
    """

    # Create the Secret Manager client.

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(request={"name": name})

    # Print the secret payload.
    #
    # WARNING: Do not print the secret in a production environment - this
    # snippet is showing how to access the secret material.
    pd = response.payload.data.decode("UTF-8")
    return json.loads(pd)
def git_commit(query_url):
    git_dbx_folder_list=[]
    git_dag_files_list=[]
    file_object = open('db_job_delta.txt', 'a+')
    file_object1 = open('dag_airflow_delta.txt', 'a+')
    acc_token=access_secret_version(project_id_sec, secret_id, version_id)

    headers = {'Authorization': f'token {acc_token["token"]}'}
    r = requests.get(query_url, headers=headers)
    data = r.json()

    for i in data["files"]:
        git_delta_file_json=i["filename"]
        git_delta_file_status_json=i["status"]

        if git_delta_file_status_json != 'removed':
            if "dbx" in git_delta_file_json:
                x = git_delta_file_json.split("/")
                git_dbx_folder_list.append(x[0]+"/"+x[1])
            if "DAG/" in git_delta_file_json:
                git_dag_files_list.append(git_delta_file_json)

    for j in set(git_dbx_folder_list):
        file_object.write(j)
        file_object.write("\n")
    for k in set(git_dag_files_list):
        file_object1.write(k)
        file_object1.write("\n")
    file_object.close() 

