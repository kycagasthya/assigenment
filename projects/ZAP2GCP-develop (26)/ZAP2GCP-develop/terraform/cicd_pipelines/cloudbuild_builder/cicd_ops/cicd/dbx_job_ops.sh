#!/bin/bash
set -e
echo "### Stage 2 : DBX Job Operation ###"
echo "### Activating Python Virtual Environment  ###"
source /venv/bin/activate
export c_dir="/workspace"
#cp -r /cicd /workspace
cd cicd

echo "# Stage 2 : DBX Job Operation"
if [ -s db_job_delta.txt ]; then
    while IFS= read -r line; do
        export job_fdr_name=$c_dir/$line
        echo "### Initializing Databrick Job Operations for "$job_fdr_name" ####"
        python3 db_ops.py
        if [ -s exception ]; then
          echo "### ERROR: Databrick Operation failed : ###" 
          cat exception
          exit 1
        fi
        if [[ "$job_fdr_name" != *"generic-utilities"* ]]; then
          echo "### Uploading Databrick Job Artifact to DBFS Mount Bucket for "$job_fdr_name" ###"
          gsutil cp $job_fdr_name/*.cfg gs://$MOUNT/$REPO_NAME/$line/ 
          if ls $job_fdr_name/*.py &> /dev/null; then
            echo "found"
            gsutil cp $job_fdr_name/*.py gs://$MOUNT/$REPO_NAME/$line/
          fi
        else
          echo "### Uploading Databrick Job Artifact to DBFS Mount Bucket for "$job_fdr_name" ###"
          gsutil cp $job_fdr_name/*.py gs://$MOUNT/$REPO_NAME/$line/ 
        fi
    done  < db_job_delta.txt
else
    echo "### Pipeline did not find any changes to DBX Jobs ###"
fi
