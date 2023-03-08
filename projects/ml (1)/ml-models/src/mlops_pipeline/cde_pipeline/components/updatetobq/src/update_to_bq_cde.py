# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# ==============================================================================
"""This module will write evaluation metrics to bq"""

from kfp.v2.components.executor import Executor
from kfp.v2.dsl import Input, Metrics, Artifact
import google.auth
import google.auth.transport.requests
import requests
import json
import pandas as pd
from custom_logger import ml_logger as logger
from google.cloud import bigquery
import traceback
import argparse


def get_url(location, url_substring):
    """
    Component to url and authentication token

    Args:
    location : The location for the processor
    url_substring: The substring of the url
    Returns:
    url:The url of the request
    token : The authentication token
    """
    authentication_request = google.auth.transport.requests.Request()
    credentials,_ = google.auth.default()
    credentials.refresh(authentication_request)
    token = credentials.token
    endpoint = f"{location}-documentai.googleapis.com"
    host = f"https://{endpoint}"
    url = f"{host}{url_substring}"
    return url, token


def get_train_test_size(project_number, processor_id, location):
    """
    Component to get the train set and test set count
    Args:
    project_id : The project id
    processor_id : The id of the processor to be trained
    location : The location for the processor
    Returns:
    train count: The count of samples of train set
    test count: The count of samples of test set
    """
    try:
        url_substring = f"/uiv1beta3/projects/{project_number}" \
                f"/locations/us/processors/{processor_id}" \
                f"/dataset:getAllDatasetSplitStats/"
        url, token = get_url(location, url_substring)
        response = requests.get(
            url, headers={"Authorization": f"Bearer {token}"}
        )
        response_json = response.json()
        logger("INFO", "Updatetobq", f"Response:{response_json}")
    except Exception as error:
        trace = traceback.format_exc()
        logger("ERROR", "Updatetobq", error, "500", response.json(), trace)
        raise
    resp_dict = response.json()
    train_count = 0
    test_count = 0
    try:
        for i in range(len(resp_dict["splitStats"])):
            if "TRAIN" in resp_dict["splitStats"][i]["type"]:
                train_count = resp_dict["splitStats"][i]["datasetStats"][
                    "documentCount"
                ]
            elif "TEST" in resp_dict["splitStats"][i]["type"]:
                test_count = resp_dict["splitStats"][i]["datasetStats"][
                    "documentCount"
                ]
        logger(
            "INFO",
            "Updatetobq",
            f"train_count:{train_count} and test_count:{test_count}",
        )

    except Exception as error:
        trace = traceback.format_exc()
        logger("ERROR", "Updatetobq", error, "400", response.json(), trace)
        raise

    return train_count, test_count


def get_train_gcs_uri(project_number, processor_id, location):
    """
    Component to get the train_gcs_uri

    Args:
    project_id : The project id
    processor_id : The id of the processor to be trained
    location : The location for the processor


    Returns:
    train_gcs_uri : The gcs_uri for the training data

    """
    try:
        url_substring = f"/uiv1beta3/projects/{project_number}" \
                        f"/locations/us/processors/{processor_id}/dataset"
        url, token = get_url(location, url_substring)
        response = requests.get(
            url, headers={"Authorization": f"Bearer {token}"}
        )
        resp_dict = response.json()
        gcs_uri = ""
        gcs_uri = resp_dict["gcsManagedConfig"]["gcsPrefix"]["gcsUriPrefix"]
        logger("INFO", "Updatetobq", f"gcs_uri:{gcs_uri}")
        return gcs_uri
    except Exception as error:
        trace = traceback.format_exc()
        logger(
            "ERROR",
            "Updatetobq",
            "Error: cannot get GCS URI of the training data",
            "400",
            error,
            trace,
        )
        raise


def get_main_dict_overall_dict(class_dic, overall_dic):
    """
    Component to get the main_dict and overall_dict

    Args:
    class_dic : The artifact  containing class level metrics
    overall_dic : The artifact  containing overall metrics

    Returns:
    main_dict: The main dictionary containing the metircs
    overall_dict: The dictionary for test and golden metrics

    """
    entities = []
    main_dict = {}
    for key in class_dic.keys():
        entities.append("_".join(key.split("_")[:-1]))
    entities = list(set(entities))
    for ent in entities:
        main_dict[ent] = {}
    for key in class_dic.keys():
        ent = "_".join(key.split("_")[:-1])
        sub_ent = key.split("_")[-1]
        main_dict[ent][sub_ent] = class_dic[key]
    golden_m = {}
    test_m = {}
    for key in overall_dic.keys():
        doc = key.split("_")
        if doc[0] == "golden":
            golden_m[doc[-1]] = overall_dic[key]
        else:
            test_m[doc[-1]] = overall_dic[key]

    overall_main_dict = {}
    overall_main_dict["golden"] = golden_m
    overall_main_dict["test"] = test_m
    overall_main_dict = (
        str(overall_main_dict).replace("'", '"').replace("f1-score", "f1_score")
    )
    return main_dict, overall_main_dict


def add_modelmetrics_tobq(
    model_name,
    job_id,
    processor_version_id,
    processor_id,
    processor_version_name,
    is_deployed,
    pipeline_name,
    region,
    ref_code_file_version,
    train_percent,
    train_size,
    test_size,
    timestamp,
    dataset_uri,
    overall_main_dict,
    gcs_path_evaluation_csv,
    gcs_path_model,
    configuration,
    project_id,
    dataset_model,
    table_name_model,
):
    """
    Function to add model metrics to Bigquery table

    Args:
    class_dic : The artifact  containing class level metrics
    overall_dic : The artifact  containing overall metrics
    model_name: DocAI processor Name/Vertex AI Model name
    job_id: Id of the Training pipeline job on Vertex AI
    ref_code_file_version: Version of the code (commit id)
    doc_type: type of the document
    project_id: GCP project ID
    model_region: Region of the model hosting
    timestamp: time from date time
    dataset_model: dataset name of the bq
    table_name_model: table name of the bq of model
    dataset_class: dataset of class table in bq
    table_name_class: table name of the bq of class
    configuration: Record with hyper-parameter and threshold values
    version_name: Version name of the trained model
    is_deployed: status whether model is deployed or not
    data_pipeline_root: Pipeline root directory
    overall_metrics: Metrics from the model
    classwise_metrics: metrics from the model
    pipeline_name: type of the model
    processor_version_id: version ID of the trained model
    gcs_ref_training_data: gcs reference path of training data
    train_test_count: Artifact contain train and test size

    Returns:


    """
    try:
        jsons_model = (
            "[{"
            + '"model_name":"'
            + str(model_name)
            + '","job_id":"'
            + str(job_id)
            + '", "processor_version_id":"'
            + str(processor_version_id)
            + '", "model_id":"'
            + str(processor_id)
            + '","version_name":"'
            + str(processor_version_name)
            + '","is_deployed":"'
            + str(is_deployed)
            + '","pipeline_name":"'
            + str(pipeline_name)
            + '","model_region":"'
            + str(region)
            + '","ref_code_file_version":"'
            + str(ref_code_file_version)
            + '","train_test_split":'
            + str(train_percent)
            + ',"train_test_size":'
            + '{"train":'
            + str(train_size)
            + ',"test":'
            + str(test_size)
            + "},"
            + '"gcs_ref_training_data":"'
            + str(dataset_uri)
            + '","trained_on":"'
            + str(pd.Timestamp(timestamp.replace(" ", "T")))
            + '","deployed_on":"'
            + str(pd.Timestamp(timestamp.replace(" ", "T")))
            + '","score":'
            + str(overall_main_dict).replace("'", '"')
            + ',"gcs_path_evaluation_csv":"'
            + str(gcs_path_evaluation_csv)
            + '","gcs_path_model":"'
            + str(gcs_path_model)
            + '","configuration":"'
            + str(configuration).replace('"', "'")
            + '"}]'
        )
        jsons_model = json.loads(jsons_model)
    except TypeError as error:
        trace = traceback.format_exc()
        logger(
            "ERROR",
            "UpdatetoBq",
            "row not added to class table in bq",
            "500",
            error,
            trace,
        )
        raise "unable to create json_model"

    bq = bigquery.Client()
    destination_table_model = bq.get_table(
        "{}.{}.{}".format(project_id, dataset_model, table_name_model)
    )
    error_model = bq.insert_rows(destination_table_model, jsons_model)
    if len(error_model) == 0:
        logger(
            "INFO",
            "UpdatetoBq",
            "row added to model table in bq",
        )
    if len(error_model) != 0:
        trace = "error while adding data to BQ"
        logger(
            "ERROR",
            "UpdatetoBq",
            "row not added to model table in bq",
            "500",
            error_model,
            trace,
        )
        raise Exception("unable to add row to table_model")


def add_classmetrics_tobq(  main_dict,
                            model_name,
                            job_id,
                            processor_version_id,
                            processor_id,
                            processor_version_name,
                            is_deployed,
                            pipeline_name,
                            region,
                            doc_type,
                            project_id,
                            dataset_class,
                            table_name_class,
                        ):
    """
    Function to add model metrics to Bigquery table

    Args:
    main_dic : The main dictionary containing the metircs
    model_name: DocAI processor Name/Vertex AI Model name
    job_id: Id of the Training pipeline job on Vertex AI
    processor_version_id: version ID of the trained model
    processor_id: ID of the trained model
    processor_version_name: Version name of the trained model
    is_deployed: status whether model is deployed or not
    pipeline_name: type of the model
    region: Region of the model hosting
    doc_type: type of the document
    ref_code_file_version: Version of the code (commit id)
    timestamp: time from date time
    project_id: GCP project ID
    model_region: Region of the model hosting
    dataset_class: dataset of class table in bq
    table_name_class: table name of the bq of class

    Returns:

    """
    k = list(main_dict.keys())
    json_class_list = []
    for i in range(len(main_dict)):
        field = k[i]
        v = main_dict[k[i]]
        true_positive = v["tp"]
        false_positive = v["fp"]
        false_negative = v["fn"]
        true_negative = v["tn"]
        del_keys = ["tp", "fp", "fn", "tn"]
        for d_key in del_keys:
            del v[d_key]
        score_json = str(v).replace("'", '"').replace("f1-score", "f1_score")
        try:
            jsons_class = (
                "{"
                + '"model_name":"'
                + str(model_name)
                + '","job_id":"'
                + str(job_id)
                + '","processor_version_id":"'
                + str(processor_version_id)
                + '","model_id":"'
                + str(processor_id)
                + '","version_name":"'
                + str(processor_version_name)
                + '","is_deployed":"'
                + str(is_deployed)
                + '","pipeline_name":"'
                + str(pipeline_name)
                + '","model_region":"'
                + str(region)
                + '","doc_type":"'
                + doc_type
                + '","field":"'
                + field
                + '","true_positive":"'
                + str(true_positive)
                + '","false_positive":"'
                + str(false_positive)
                + '","true_negative":"'
                + str(true_negative)
                + '","false_negative":"'
                + str(false_negative)
                + '","score":{"golden":'
                + score_json
                + "}}"
            )
        except KeyError as error:
            trace = traceback.format_exc()
            logger("ERROR", "unable to create json_class", "500", error, trace)
            raise
        except Exception as error:
            trace = traceback.format_exc()
            logger("ERROR", "unable to create json_class", "500", error, trace)
            raise
        jsons_class = json.loads(jsons_class)
        json_class_list.append(jsons_class)
    bq = bigquery.Client()
    destination_table_class = bq.get_table(
        "{}.{}.{}".format(project_id, dataset_class, table_name_class)
    )
    error_class = bq.insert_rows(destination_table_class, json_class_list)
    if len(error_class) == 0:
        logger(
            "INFO",
            "UpdatetoBq",
            "row added to class table in bq",
        )
    else:
        trace = "error while adding data to BQ"
        logger(
            "ERROR",
            "UpdatetoBq",
            "row not added to class table in bq",
            "500",
            error_class,
            trace,
        )
        raise Exception("unable to add row to table_class")


def write_metrics_to_bq(
    job_id: str,
    processor_id: str,
    project_number: str,
    ref_code_file_version: str,
    doc_type: str,
    is_deployed: str,
    configuration: str,
    project_id: str,
    region: str,
    timestamp: str,
    dataset_model: str,
    table_name_model: str,
    dataset_class: str,
    table_name_class: str,
    data_pipeline_root: str,
    model_name: str,
    pipeline_name: str,
    gcs_path_model: str,
    location: str,
    version_name: Input[Artifact],
    overall_metrics: Input[Metrics],
    class_metrics: Input[Metrics],
):
    """
    function to insert data into bq

    Args:
        model_name: DocAI processor Name/Vertex AI Model name
        job_id: Id of the Training pipeline job on Vertex AI
        ref_code_file_version: Version of the code (commit id)
        doc_type: type of the document
        project_id: GCP project ID
        model_region: Region of the model hosting
        timestamp: time from date time
        dataset_model: dataset name of the bq
        table_name_model: table name of the bq of model
        dataset_class: dataset of class table in bq
        table_name_class: table name of the bq of class
        configuration: Record with hyper-parameter and threshold values
        version_name: Version name of the trained model
        is_deployed: status whether model is deployed or not
        data_pipeline_root: Pipeline root directory
        overall_metrics: Metrics from the model
        classwise_metrics: metrics from the model
        overall_metrics_model: metrics from the model
        pipeline_name: type of the model
        processor_version_id: version ID of the trained model
        gcs_ref_training_data: gcs reference path of training data
        train_test_count: Artifact contain train and test size

    Return:None
    Raises
    TypeError : if the json class or model creation failed cause of
     unexpected input type.
    ZeroDivisionError : if the train + test value is equal to zero

    """
    class_dic = class_metrics.metadata
    overall_dic = overall_metrics.metadata
    processor_version_name = version_name.metadata["version_name"]
    processor_version_id = version_name.metadata["processor_version_id"]
    train_size, test_size = get_train_test_size( \
        project_number, processor_id, location
    )
    dataset_uri = get_train_gcs_uri(project_number, processor_id, location)
    train_percent = (
        train_size // (train_size + test_size)
        if (train_size + test_size) != 0
        else 0
    )
    gcs_path_evaluation_csv = f"{data_pipeline_root}/evaluation_df.csv"
    main_dict, overall_main_dict = get_main_dict_overall_dict(
        class_dic, overall_dic
    )
    add_modelmetrics_tobq(
        model_name,
        job_id,
        processor_version_id,
        processor_id,
        processor_version_name,
        is_deployed,
        pipeline_name,
        region,
        ref_code_file_version,
        train_percent,
        train_size,
        test_size,
        timestamp,
        dataset_uri,
        overall_main_dict,
        gcs_path_evaluation_csv,
        gcs_path_model,
        configuration,
        project_id,
        dataset_model,
        table_name_model,
    )

    add_classmetrics_tobq(
        main_dict,
        model_name,
        job_id,
        processor_version_id,
        processor_id,
        processor_version_name,
        is_deployed,
        pipeline_name,
        region,
        doc_type,
        project_id,
        dataset_class,
        table_name_class,
    )


def executor_main():
    """
    function to pass arguments to the Update to bq component

    """

    parser = argparse.ArgumentParser()
    parser.add_argument("--executor_input", type=str)
    parser.add_argument("--function_to_execute", type=str)
    args, _ = parser.parse_known_args()
    executor_input = json.loads(args.executor_input)
    function_to_execute = globals()[args.function_to_execute]
    executor = Executor(
        executor_input=executor_input, function_to_execute=function_to_execute
    )
    executor.execute()


if __name__ == "__main__":
    executor_main()
