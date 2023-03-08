# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

"""This file contains various utilities"""

import os
from datetime import datetime
from os.path import join
import logging
from google.cloud import storage

def list_files(bucket_name, bucket_folder):
    """Lists files in a GCP bucket."""

    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    elements = bucket.list_blobs(prefix=bucket_folder)
    files=["gs://"+ bucket_name + "/" + a.name for a in elements]

    return files

def retrieve_spec_file(bucket_path, file_version="latest"):
    """
    gives gcs uri
    Args:
        bucket_path: bucket path
        file_version: "latest"
    Return:
        gcs_uri:gcs uri
    """
    gcs_uri = None
    if not bucket_path:
        logging.error("bucket_path is empty. Exiting!")
        raise
    bucket_name = bucket_path.split("/")[2]
    bucket_folder = "/".join(bucket_path.split("/")[3:])

    if file_version == "latest":
        files = list_files(bucket_name, os.path.join(bucket_folder, "latest"))
        for file in files:
            if file.endswith(".json"):
                gcs_uri = file
                break
    else:
        files = list_files(bucket_name, os.path.join(
            bucket_folder, f"build/{file_version}"))
        for file in files:
            if file.endswith(".json"):
                gcs_uri = file
                break

    return gcs_uri

def check_params_exist(params_dict, params_list):
    """
    checking parameters
    Args:
        params_dict: Paramerts dictionary
        params_list: parameters list
    Returns:
        None
    Raise:
        ValueError
    """
    for param in params_list:
        if not params_dict.get(param):
            raise ValueError(f"Config parameter - {param} \
                             should be set and cannot be empty")

def remove_params(params_dict, params_to_remove):
    """
    Removing parameters
    Args:
        params_dict: Paramerts dictionary
        params_to_remove: parameters to be remove
    Retrun:
        params_dict: dictionary after removing paramaters
    """
    for param in params_to_remove:
        params_dict.pop(param, None)
    return params_dict

def check_update_timestamp(config_dict, params_dict):
    """
    checking updated timestamp
    Args:
        config_dict: config dictionary
        params_dict: parameter dictionary
    Returns:
        params_dict: updated dictionary with parameters
    """
    timestamp_dag = config_dict.get("timestamp_dag")
    if not timestamp_dag:
        raise Exception ("Airflow was not able to set the timestamp")

    if params_dict.get("timestamp_hr") == "":
        date = datetime.strptime(timestamp_dag, "%Y%m%d%H%M%S")
        timestamp = datetime.strftime(date, "%Y-%m-%d %H:%M:%S")
        params_dict["timestamp_hr"] = timestamp
    return params_dict

def update_params_timestamp(params_dict, params_list, timestamp):
    """
    updating timestamp para
    Args:
        params_dict: paramater dictionary
        params_list: parameter list
        timestamp: timestamp
    Returns:
        params_dict: updated dictionary with parameters
    """
    for param in params_list:
        if param == "job_id" and params_dict.get(param):
            params_dict[param] = str(params_dict[param])+"-"+str(timestamp)
        elif (param == "data_pipeline_root" and params_dict.get(
            "data_pipeline_root") == ""
                                              and params_dict.get(
                                                  "pipeline_root")):
            params_dict[param] = join(
                params_dict["pipeline_root"],
                "data_pipeline_root",
                str(timestamp))
    return params_dict
