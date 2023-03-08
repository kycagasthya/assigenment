import json, re, requests, os
from pathlib import Path
from google.cloud import secretmanager

project_id_sec =os.environ["PROJECT_ID_SEC"]
git_owner =os.environ["OWNER"]
branch = os.environ["BRANCH"]
repo = os.environ["REPO_NAME"]
secret_id = os.environ["GIT_SEC_ID"]
version_id = os.environ["GIT_VER_ID"]
git_user =os.environ["GIT_USER"]

client = secretmanager.SecretManagerServiceClient()

def git_clone():
 
   acc_token=access_secret_version(project_id_sec, secret_id, version_id)
   git_cmd= f'git clone https://{git_user}:{acc_token["token"]}@github.com/{git_owner}/{repo}.git ./git_branch'
   os.system(git_cmd)



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
git_clone()
