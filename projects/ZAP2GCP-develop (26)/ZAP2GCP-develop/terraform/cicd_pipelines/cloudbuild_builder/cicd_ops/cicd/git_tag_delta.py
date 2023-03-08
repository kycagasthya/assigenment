import os, json
import git_delta

git_owner =os.environ["OWNER"]
branch = os.environ["BRANCH"]
repo = os.environ["REPO_NAME"]

def delta_file(file_name):
    git_dbx_folder_list=[]
    git_dag_files_list=[]
    with open(file_name) as f: 
        data = f.readlines()
    delta_dbx_job_file = open('db_job_delta.txt', 'a+')
    delta_dah_job_file = open('dag_airflow_delta.txt', 'a+')
    for i in data:
        if "dbx" in i:
            x = i.split("/")
            git_dbx_folder_list.append(x[0]+"/"+x[1])
        if "DAG/" in i:
            git_dag_files_list.append(i)

    for j in set(git_dbx_folder_list):
        delta_dbx_job_file.write(j)
        delta_dbx_job_file.write("\n")
    for k in set(git_dag_files_list):
        delta_dah_job_file.write(k)
        delta_dah_job_file.write("\n")
    delta_dbx_job_file.close() 
    return "success"
def git_tag():
    if branch != "prod":
        query_url = f"https://api.github.com/repos/{git_owner}/{repo}/commits/{branch}"
        git_delta.git_commit(query_url)
    elif branch == "prod":
        roll_flag = os.environ["HARD_ROLLBACK"]
        if roll_flag == "False":

            git_dbx_folder_list=[]
            git_dag_files_list=[]
            delta_file('stage_tag_diff')
        elif roll_flag == "True":
            delta_file('stage_tag') 
        else:
            print("No Opration Staged for CICD")
    else:
        print("No Operation Staged CICD")
git_tag()
