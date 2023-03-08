# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

"""This is the custom od model training DAG. This will invoke the
standard preprocessing module and the vertex ai training module."""

from airflow import DAG
from airflow.operators import python_operator
import sys
import logging
from os.path import dirname, abspath
sys.path.insert(0, abspath(dirname(__file__)))
from dag_config import default_args
from standard_preprocessing.std_preproc import StandardPreprocessing
from invoke_training.custom_training_pipeline_runner import train

def std_preproc(**kwargs):
    try:
        timestamp_dag = str(kwargs.get("timestamp_dag")).replace("T","")
        dag_run = kwargs.get("dag_run")
        config_dict = dag_run.conf
        compulsory_params_list = ["train_path", "validation_path"]
        for param in compulsory_params_list:
            if not config_dict.get(param):
                raise ValueError(
                    f"Config parameter - {param} should be set and cannot be "
                    f"empty")
        logging.info("Initializing StandardPreprocessing and processing data")
        std_preprocessing = StandardPreprocessing()
        std_preprocessing.process(
            config_dict["train_path"], config_dict["train_path"], timestamp_dag)
        std_preprocessing.process(
            config_dict["validation_path"], config_dict["validation_path"],
                                                    timestamp_dag)
        logging.info("StandardPreprocessing Completed successfully")
        return True
    except ValueError as e:
        logging.error(e)
        raise
    except FileNotFoundError as e:
        logging.error(e)
        raise
    except Exception as e:
        logging.error(e)
        raise


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
    "custom_od_pipeline",
    default_args=default_args,
    description="Custom OD Training Pipeline",
    schedule_interval=None,
) as dag:

    # stage 1 of composer Dag
    std_preprocessing_task = python_operator.PythonOperator(
         task_id="std_preprocessing",
         python_callable=std_preproc,
         op_kwargs={"timestamp_dag": "{{ts_nodash}}" },
         dag=dag)

    #stage 2 of composer Dag
    invoke_training_task = python_operator.PythonOperator(
        task_id="invoke_training",
        python_callable=invoke_training,
        op_kwargs = {"timestamp_dag": "{{ts_nodash}}" },
        dag=dag)
    # Composer Pipeline Flow
    std_preprocessing_task >> invoke_training_task
