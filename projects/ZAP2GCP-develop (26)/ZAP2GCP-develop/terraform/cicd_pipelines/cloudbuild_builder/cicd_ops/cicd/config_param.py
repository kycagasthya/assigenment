import os

project_id_dbx =os.environ["PROJECT_ID_DBX"]
branch = os.environ["BRANCH"]
db_svc = os.environ["DB_SVC"]
hive_meta_ip= os.environ["HIVE_META_IP"]


def update_env(file_name):
    try:
        file_name=file_name.replace(" ", "") 
        env_key_list = [project_id_dbx, branch, db_svc, hive_meta_ip]
        env_val_list = ["$project_id", "$env", "$svc", "$hive_sql_host"]
        # Read in the file
        with open(file_name, 'r') as file :
          filedata = file.read()

        # Replace the target string
        for (i,j) in zip(env_val_list, env_key_list):
          filedata = filedata.replace(i, j)

        # Write the file out again
        with open(file_name, 'w') as file :
          file.write(filedata)
    except IOError:
        print('### file not found, skipping operation ###')  


