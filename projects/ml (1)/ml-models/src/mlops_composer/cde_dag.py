# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

"""This is the cde processor training DAG. This will invoke the
vertex ai training module."""

from airflow import DAG
from airflow.operators import python_operator
import sys
import logging
from os.path import dirname, abspath
sys.path.insert(0, abspath(dirname(__file__)))
from dag_config import default_args
from invoke_training.cde_training_pipeline_runner import train


def invoke_training(**kwargs):
    """
    Invoke training pipeline
    """
    try:
        timestamp_dag = str(kwargs.get("timestamp_dag")).replace("T","")
        dag_run = kwargs.get("dag_run")
        config_dict = dag_run.conf
        config_dict["timestamp_dag"] = timestamp_dag
        train(config_dict)
        return True
    except Exception as e:
        logging.error(e)
        raise

# Create a DAG
with DAG(
    "cde_pipeline",
    default_args=default_args,
    description="CDE Training Pipeline",
    schedule_interval=None
) as dag:
    invoke_training_task = python_operator.PythonOperator(
        task_id="invoke_training",
        python_callable=invoke_training,
        op_kwargs = {"timestamp_dag": "{{ts_nodash}}" },
        dag=dag)
    # Composer Pipeline Flow
    invoke_training_task
