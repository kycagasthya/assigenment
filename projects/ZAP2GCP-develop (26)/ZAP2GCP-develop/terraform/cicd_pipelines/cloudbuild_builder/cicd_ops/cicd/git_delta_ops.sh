#!/bin/bash
set -e
echo "### Stage 1: Fetching commited updates ###"
echo "### Activating Python Virtual Environment ###"
source /venv/bin/activate
export c_dir="/workspace"
cd cicd
if [ $BRANCH == "prod" ] && [ "$HARD_ROLLBACK" == "False" ]; then
  python git_delta_branch.py
  cd git_branch
  git diff $CURRENT_TAG $TAG_NAME --stat --name-only --diff-filter=ACMR | sort | uniq > ../stage_tag_diff 
  cd ../
  cat stage_tag_diff
fi

if [ "$HARD_ROLLBACK" == "True" ]; then
  git show --name-only  | awk -F "/*[^/]*/*$" '{ print ($1 == "" ? "." : $1); }' | sort | uniq > stage_tag
  cat stage_tag
fi

python3 git_tag_delta.py
sed -i '/^$/d' db_job_delta.txt
while IFS= read -r line; do
  export job_fdr_name=$c_dir/$line
  if ls $job_fdr_name/dag_dependency &> /dev/null; then
    tail -n +2 $job_fdr_name/dag_dependency >> dag_airflow_delta.txt
  fi
done  < db_job_delta.txt
sed -i '/^$/d' dag_airflow_delta.txt
awk '!seen[$0]++' dag_airflow_delta.txt > stage
cat stage > dag_airflow_delta.txt
echo "### Staged Databricks Job(s): ###"
cat db_job_delta.txt 
echo "### Staged Airflow DAG(s): ###"
cat dag_airflow_delta.txt 
