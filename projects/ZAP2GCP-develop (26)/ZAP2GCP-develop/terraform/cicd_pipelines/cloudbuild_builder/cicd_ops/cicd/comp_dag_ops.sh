#!/bin/bash
#set -e
echo "### Stage 3 : Composer DAG Operations ###"
echo "### Activating Python Virtual Environment  ###"

source /venv/bin/activate
export c_dir="/workspace"
cd cicd

if [ -s dag_airflow_delta.txt ]; then
    while IFS= read -r line; do
        export dag_file_name=$c_dir/$line
        echo "### Initializing Composer DAG Operations for "$dag_file_name" ###"
        python3 dag_ops.py
        if [ -s exception ]; then
            echo "### ERROR: Composer DAG Operation failed : ###" 
            cat exception
            exit 1
        fi
        if grep -q % "$dag_file_name"; then
            echo "### ERROR: One Or More Job IDs Faild to extract or missing in Databricks for "$dag_file_name" ###"
            echo $dag_file_name >> dag_failure
        else
            echo "### Uploading DAG  Artifact to Composer Bucket for "$dag_file_name" ###"
            fld=`echo "$line" | awk -F'/' '{print $1}'`
            fle=`echo "$line" | awk -F'/' '{print $2}'`
            mv $dag_file_name $c_dir/$fld/$BRANCH"_"$fle
            gsutil cp $c_dir/$fld/$BRANCH"_"$fle gs://$DAG_BUCKET/dags/
        fi 
    done  < dag_airflow_delta.txt
    if [ -s dag_failure ]; then
       echo "### ERROR: Composer DAG Operation failed to push below files: ###" 
       cat dag_failure
       exit 1
    fi
    if [ -s exception ]; then
       echo "### ERROR: Composer DAG Operation failed : ###" 
       cat exception
       exit 1
    fi

else
    echo "### Pipeline did not find any changes to Composer DAGs ###"
fi    

