
import requests
import json, os
from google.cloud import secretmanager
import json
import config_param

project_id_sec =os.environ["PROJECT_ID_SEC"]
instance_id = os.environ["INSTANCE_ID"]
api_version = os.environ["API_VERSION"]
secret_id = os.environ["DB_SEC_ID"]
version_id = os.environ["DB_VER_ID"]
db_svc = os.environ["DB_SVC"]
fld_name = os.environ["job_fdr_name"]


def access_secret_version(project_id, secret_id, version_id):
    """
    Access the payload for the given secret version if one exists. The version
    can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
    """

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

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

def create_job():
   api_command = '/jobs/create'
   url = f"https://{instance_id}{api_version}{api_command}"
   acc_token=access_secret_version(project_id_sec, secret_id, version_id)
   response = requests.post(url, auth=(acc_token["Cloud_Build"]["login"], acc_token["Cloud_Build"]['password']), data = open(f"{fld_name}/create_job.json", 'rb'))
   print("### Databricks Job create operation: \n", json.dumps(json.loads(response.text), indent = 2))

def reset_job():
   try:
      api_command = '/jobs/reset'
      url = f"https://{instance_id}{api_version}{api_command}"
      acc_token=access_secret_version(project_id_sec, secret_id, version_id)
      response = requests.post(url, auth=(acc_token["Cloud_Build"]["login"], acc_token["Cloud_Build"]["password"]), data = open(f"{fld_name}/reset_job.json", 'rb'))
      print("### Databricks Job reset operation: ### \n", json.dumps(json.loads(response.text), indent = 2))
   except IOError:
      print('### Databricks job reset file not found, skipping operation ###')
def check_job_status(params):
   try:
      api_command = '/jobs/list'
      url = f"https://{instance_id}{api_version}{api_command}"
      acc_token=access_secret_version(project_id_sec, secret_id, version_id)
      response = requests.get(url, auth=(acc_token["Cloud_Build"]["login"], acc_token["Cloud_Build"]["password"]), params=params) 
      response1=json.loads(response.text)
      return response1
   except json.decoder.JSONDecodeError as ex1:
      print("### ERROR: received an invaild response from databricks job list api,  please validate below environment variables  ###")
      print("instance_id", instance_id, "\n", "api_version", api_version, "\n", "api_command: ", api_command, "\n", "the above varible form databricks url: ", url)
      cmd = f'echo {ex1.response.text}>>exception'
      os.system(cmd)

def reset_file_update(job_id):
   try:
      with open('{}/reset_job.json'.format(fld_name)) as f: 
         data = json.load(f)
      data.update(job_id=int(job_id))
      with open('{}/reset_job.json'.format(fld_name), 'w') as f: 
         json.dump(data, f, ensure_ascii=False, indent = 4)
   except IOError:
      print('### Databricks job reset file not found, skipping operation ###')
def get_job_id(resp, job_name):
   for name in resp['jobs']:
      if job_name in str(name):
         print("### Identified job_id: ", name['job_id'], "for job_name: ", name['settings']['name'], " ###")
         reset_file_update(name['job_id']) 
         return "success"
def job_id_check(resp, job_name):
   for name in resp['jobs']:
      if job_name == name['settings']['name']:
         print("### Identified job_id: ", name['job_id'], "for job_name: ", name['settings']['name'], " ###")
         get_job_id(resp, job_name)
         return True
   return False
def list_job(job_name):
   params = {
  'offset': 0, 'limit': 25}
   resp=check_job_status(params)
   if "jobs" not in str(resp):
        print("### Databricks Workspace returned empty job list ###")
        return False
   else:
        if not resp["has_more"]:
            job_name_sts=job_id_check(resp, job_name)
            if job_name_sts:
                return True
            else:
                return False
        else:
            while resp["has_more"]:
                resp=check_job_status(params)
                job_name_sts=job_id_check(resp, job_name)
                if job_name_sts:
                    return True
                if not resp["has_more"]:
                    job_name_sts=job_id_check(resp, job_name)
                    if job_name_sts:
                        return True
                params.update(offset=params['offset']+params['limit'])
            return False
    
  
def main():
   try:
      with open('{}/create_job.json'.format(fld_name)) as f: 
         data = json.load(f)
      job_name = data["name"]
      print(job_name)
      config_param.update_env(f"{fld_name}/create_job.json")
      file_list = os.listdir(fld_name)
      for file in file_list:
         if ".cfg" in str(file): 
            config_param.update_env(f"{fld_name}/{file}")
      status=list_job(job_name)
      if status == True:
         try:
            config_param.update_env(f"{fld_name}/reset_job.json")
         except IOError:
            print('### Databricks job reset file not found, skipping operation ###')
         reset_job()
      else:
         create_job() 
   except IOError:
      print('### Databricks job create file not found, skipping operation ###')   
      config_param.update_env(f"{fld_name}/app_config.cfg")


main()

