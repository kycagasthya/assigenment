from pathlib import Path
import os
import requests
import json, re
from google.cloud import secretmanager
import json
import config_param
import time

project_id_sec =os.environ["PROJECT_ID_SEC"]
project_id_dbx =os.environ["PROJECT_ID_DBX"]
instance_id = os.environ["INSTANCE_ID"]
api_version = os.environ["API_VERSION"]
secret_id = os.environ["DB_SEC_ID"]
version_id = os.environ["DB_VER_ID"]
dag_file=os.environ["dag_file_name"]
client = secretmanager.SecretManagerServiceClient()

dag_dbx_job_names=[]
fltrd_dag_dbx_job_names=[]

def get_job_name():
    with open(str(dag_file), 'r') as f:
        for line in f.readlines():
            if '%' in line:
                x = line.split("=")
                dag_dbx_job_names.append(x)
        for l in dag_dbx_job_names:
            for j in l:
                if '%' in j:
                     fltrd_dag_dbx_job_names.append(j)
    return fltrd_dag_dbx_job_names
def list_job(params):
   try:
      api_command = '/jobs/list'
      url = f"https://{instance_id}{api_version}{api_command}"  
      acc_token=access_secret_version(project_id_sec, secret_id, version_id)
      response = requests.get(url, auth=(acc_token["Cloud_Build"]["login"], acc_token["Cloud_Build"]["password"]), params=params)
      response=json.loads(response.text)
      return response
   except json.decoder.JSONDecodeError as ex1:
      print("### ERROR: received an invaild response from databricks job list api,  please validate below environment variables  ###")
      print("instance_id", instance_id, "\n", "api_version", api_version, "\n", "api_command: ", api_command, "\n", "the above varible form databricks url: ", url)
      cmd = f'echo {ex1.response.text}>>exception'
      os.system(cmd)

def get_job_id():
   job_dbx_id_list=[]
   job_dbx_name_list=[]
   fltrd_job_dbx_name_list=[] 
   temp_dbx_job_list=get_job_name()
   for d in temp_dbx_job_list:
      k = re.sub(r"[^a-zA-Z0-9_-]","",d)
      fltrd_job_dbx_name_list.append(k)
   print("### Following Databricks Jobs are staged for deployment: ### \n", fltrd_job_dbx_name_list) 
   params = {
  'offset': 0, 'limit': 5}
   resp=list_job(params)
   if "jobs" not in str(resp):
      print("### Databricks Workspace returned empty job list ###")
   elif not resp["has_more"]:
      for dbx_job_name in fltrd_job_dbx_name_list:
         for name in resp['jobs']:
            if dbx_job_name == name['settings']['name']:
               job_dbx_id_list.append(name['job_id'])
               job_dbx_name_list.append(name['settings']['name'])
               print("### Identified job_id: ", name['job_id'], "for job_name: ", name['settings']['name'], " ###")

   else:
      while resp["has_more"]:
          for dbx_job_name in fltrd_job_dbx_name_list:
              for name in resp['jobs']:
                  if dbx_job_name == name['settings']['name']:
                     job_dbx_id_list.append(name['job_id'])
                     job_dbx_name_list.append(name['settings']['name'])
                     print("### Identified job_id: ", name['job_id'], "for job_name: ", name['settings']['name'], " ###")
          params.update(offset=params['offset']+params['limit'])
          resp=list_job(params)
          if not resp["has_more"]: 
              for dbx_job_name in fltrd_job_dbx_name_list:          
                  for name in resp['jobs']:
                      if dbx_job_name == name['settings']['name']:
                          job_dbx_id_list.append(name['job_id'])
                          job_dbx_name_list.append(name['settings']['name'])
                          print("### Identified job_id: ", name['job_id'], "for job_name: ", name['settings']['name'], " ###")
   return job_dbx_id_list, job_dbx_name_list

def update_job_id():
    try:
        time.sleep(7)
        config_param.update_env(f"{dag_file}")
        file = Path(str(dag_file))
        job_id, job_n=get_job_id()
        if len(job_id) == 0:
            print("### ERROR: Reference Databricks job in DAG not found ###")
        else:
            for (n,k) in zip(job_n,job_id):
                file.write_text(file.read_text().replace(f"%{n}", str(k)))
    except Exception as ex:
        cmd = f'echo {ex}>> "exception"'
        os.system(cmd)

def access_secret_version(project_id, secret_id, version_id):
    """
    Access the payload for the given secret version if one exists. The version
    can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
    """


    # Build the resource name of the secret version.
    name = f"projects/{project_id_sec}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(request={"name": name})

    # Print the secret payload.
    #
    # WARNING: Do not print the secret in a production environment - this
    # snippet is showing how to access the secret material.
    pd = response.payload.data.decode("UTF-8")
    return json.loads(pd)

update_job_id()
