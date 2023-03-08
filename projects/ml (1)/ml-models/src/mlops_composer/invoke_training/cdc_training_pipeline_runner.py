# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

"""This is the pipeline runner for cdc processor training"""
from copy import deepcopy
import logging
import json
import sys
from os.path import dirname, abspath, join
from airflow.models import Variable
from google.cloud import aiplatform
sys.path.insert(0, abspath(dirname(__file__)))
sys.path.insert(0, join(abspath(dirname(dirname(__file__))), "config"))
from utils import check_params_exist, \
                remove_params, \
                check_update_timestamp, \
                retrieve_spec_file, update_params_timestamp



def train(config_dict):
    """
    cdc training pipeline
    Args:
        config_dict: cinfiguration dictionary
    Return:
        None
    """

    logging.info("Sys path: %s",str(sys.path))
    logging.info("User provided config: %s",str(config_dict))
    params_dict = {}
    stage = Variable.get("stage", default_var="")
    try:
        if stage == "":
            raise ValueError("Airflow variable 'stage' cannot be empty, \
                             please set it to either - dev/uat/prod")
        if stage not in ["dev", "uat", "prod"]:
            raise ValueError("Airflow variable 'stage' \
                             doesn't contain the correct value, \
                            please set it to either - dev/uat/prod")
        parent_dir = abspath(dirname(dirname(__file__)))
        if (not config_dict.get("config_path", 0)) or \
        config_dict.get("config_path") == "":
            config_path = f"{parent_dir}/config/config_{stage}/cdc_config.json"
        else:
            config_path = config_dict.get("config_path")
        with open(config_path, "r") as file:
            params_dict = json.load(file)

        compulsory_params = params_dict.get("compulsory_params", [])
        params_dict = check_update_timestamp(config_dict, params_dict)

        params_dict = {**params_dict, **config_dict}
        check_params_exist(params_dict, compulsory_params)
        params_dict = update_params_timestamp(
            params_dict, ["job_id", "data_pipeline_root"],
                                              config_dict.get("timestamp_dag"))
        pipeline_spec_file_path = retrieve_spec_file(
            params_dict.get("pipeline_spec_path"),
                                file_version=params_dict.get(
                                    "pipeline_spec_version", "latest"))

        if not pipeline_spec_file_path:
            raise FileNotFoundError("pipeline spec file not found. Exiting!")

        params_dict["pipeline_spec_file_path"] = pipeline_spec_file_path
        params_dict["ref_code_file_version"] = ""
        if pipeline_spec_file_path:
            params_dict["ref_code_file_version"] = str(
                pipeline_spec_file_path
                                                      ).rsplit(
                ".", 1)[0].rsplit("_", 1)[-1]

        params_dict["configuration"] = json.dumps(params_dict)
        parameter_values_dict = deepcopy(params_dict)
        params_to_remove = ["pipeline_root", "compulsory_params",
                          "pipeline_spec_path", "pipeline_spec_file_path",
                           "timestamp_dag", "service_account", "cmek"]
        parameter_values_dict = remove_params(parameter_values_dict,
                                              params_to_remove)

        logging.info("params dict: %s",str(params_dict))
        logging.info("parameter_values_dict: %s",str(parameter_values_dict))
        pipeline_job = aiplatform.PipelineJob(
            encryption_spec_key_name = params_dict["cmek"],
            display_name="cdc-train-pipeline",
            template_path=params_dict.get("pipeline_spec_file_path"),
            pipeline_root=params_dict.get("pipeline_root"),
            job_id=params_dict.get("job_id"),
            parameter_values=parameter_values_dict,
            location=params_dict.get("region"),
            project=params_dict.get("project_id"),
            enable_caching=False
        )
        if params_dict["service_account"] == "NA":
            pipeline_job.submit()
        else:
            pipeline_job.submit(service_account=params_dict["service_account"])
    except ValueError as err:
        logging.error(err)
        raise

    except FileNotFoundError as err:
        logging.error(err)
        raise

    except Exception as err:
        logging.error(err)
        raise
