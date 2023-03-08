# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# =============================================================================

"""This module will write evaluation metrics to bq"""

from kfp.v2.components.executor import Executor
from kfp.v2.dsl import Metrics, Artifact, Input
import google.auth
import google.auth.transport.requests
import requests
import custom_logger
from google.cloud import bigquery
import json
import argparse


def get_train_test_size(project_number: str, processor_id: str,location:str):
    """
    Args:
        project_number(str): project number
        processor_id(str):processorid of parser
     Returns:
        train_count(int): train count size
        test_count(int): test_count
    """
    authentication_request = google.auth.transport.requests.Request()
    credentials, _ = google.auth.default()
    credentials.refresh(authentication_request)
    token = credentials.token
    endpoint = f"{location}-documentai.googleapis.com"
    host = f"https://{endpoint}"

    url = f"{host}/uiv1beta3/projects/{project_number}/locations/" \
          f"{location}/processors/{processor_id}/dataset:getAllDatasetSplitStats/"

    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})

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

        custom_logger.ml_logger(
            type_log="INFO",
            component="update_to_bq",
            message="training count :" + str(train_count),
        )
        custom_logger.ml_logger(
            type_log="INFO",
            component="update_to_bq",
            message="test count ----> :" + str(test_count),
        )
    except Exception:
        custom_logger.ml_logger(
            type_log="ERROR",
            component="update_to_bq",
            message="Error while calculating train and test count",
        )
        raise
    return train_count, test_count


def get_train_gcs_uri(
        project_number: str, processor_id: str,location:str
):
    """
    return  gcs uri
    Args:
        project_number(str): project number
        processor_id(str):processor id of parser
     Returns:
        gcs_uri: gcs uri

    """

    authentication_request = google.auth.transport.requests.Request()
    credentials, _ = google.auth.default()
    credentials.refresh(authentication_request)
    token = credentials.token
    endpoint = f"{location}-documentai.googleapis.com"
    host = f"https://{endpoint}"

    url = f"{host}/uiv1beta3/projects/{project_number}/" \
          f"locations/{location}/processors/{processor_id}/dataset"

    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})

    resp_dict = response.json()
    gcs_uri = ""
    try:
        gcs_uri = resp_dict["gcsManagedConfig"]["gcsPrefix"]["gcsUriPrefix"]
        custom_logger.ml_logger(
            type_log="INFO",
            component="update_to_bq",
            message="GCS URI :" + gcs_uri,
        )
    except Exception:
        custom_logger.ml_logger(
            type_log="ERROR",
            component="update_to_bq",
            message="Error: cannot get GCS URI of the training data",
        )
        raise
    return gcs_uri


def get_metadata(version_name, class_metrics, overall_metrics):
    """
    Args:
        version_name: version name
        class_metrics: class metrics
        overall_metrics: overall metrics
     Returns:
        processor_version_name: processor version name
        processor_version_id: processor version id
        class_dic: class dic
        overall_dic: overall dic
    """
    processor_version_name = version_name.metadata[
        "version_name"
    ]
    processor_version_id = version_name.metadata[
        "processor_version_id"
    ]
    class_dic = class_metrics.metadata
    overall_dic = overall_metrics.metadata

    return processor_version_name, processor_version_id, class_dic, overall_dic


def get_class_model_json(
        model_display_name: str,
        job_id: str,
        processor_id: str,
        data_pipeline_root: str,
        project_number: str,
        ref_code_file_version: str,
        doc_type: str,
        region: str,
        timestamp: str,
        pipeline_name: str,
        configuration: str,
        is_deployed: str,
        location:str,
        gcs_path_model:str,
        processor_version_name,
        processor_version_id,
        class_dic,
        overall_dic,
):
    """
    This is the component used to
    update the used data for evaluation
    and training ino BQ
    Args:
        model_display_name(str): model name displayed on UI
        job_id(str):job id
        processor_id(str):doc AI processor id
        data_pipeline_root(str):root of pipeline
        processor_type(str): DOCAI processor type
        project_number(str): project number in GCP
        model_type(str): DOC AI processor model type
        ref_code_file_version(str): repository commit id
        doc_type(str): document type
        project_id(str):docai project id
        region(str):server region
        timestamp(str): timestamp
        dataset_model(str): dataset model name used for BQ
        table_name_model(str): table_namemodel name used for BQ
        dataset_class(str):class used for BQ
        table_name_class(str): table name class used for BQ
        pipeline_name(str): name of the pipeline
        configuration(str): configuration
        is_deployed(str): dlag to check model is deployed
        version_name(Artifact): docai model version name
        overall_metrics(metric):overall metric of golden and test data
        class_metrics(metric):classwise metric score
     Returns:
         jsons_model: model metrics
         json_class_list: class metrics
    """
    train_size, test_size = get_train_test_size(project_number,
                                                processor_id,location)
    pan = {}
    aadhaar = {}
    voter = {}
    passport = {}
    dl = {}
    default_dic = {
        "accuracy": 0,
        "f1-score": 0,
        "precision": 0,
        "recall": 0,
        "tp": 0,
        "tn": 0,
        "fp": 0,
        "fn": 0,
    }

    for key in class_dic.keys():
        doc = key.rsplit("_", 1)
        if doc[0] == "aadhaar_card":
            aadhaar[doc[-1]] = class_dic[key]
        elif doc[0] == "pan_card":
            pan[doc[-1]] = class_dic[key]
        elif doc[0] == "voter_card":
            voter[doc[-1]] = class_dic[key]
        elif doc[0] == "driving_license":
            dl[doc[-1]] = class_dic[key]
        else:
            passport[doc[-1]] = class_dic[key]

    if len(pan) == 0:
        pan = default_dic
    if len(aadhaar) == 0:
        aadhaar = default_dic
    if len(voter) == 0:
        voter = default_dic
    if len(passport) == 0:
        passport = default_dic
    if len(dl) == 0:
        dl = default_dic

    main_dict = {}
    main_dict["aadhaar_card"] = aadhaar
    main_dict["pan_card"] = pan
    main_dict["driving_license"] = dl
    main_dict["passport"] = passport
    main_dict["voter"] = voter

    golden_m = {}
    test_m = {}

    for key in overall_dic.keys():
        doc = key.split("_", 1)
        if doc[0] == "golden":
            golden_m[doc[-1]] = overall_dic[key]
        else:
            test_m[doc[-1]] = overall_dic[key]

    overall_main_dict = {}
    overall_main_dict["golden"] = golden_m
    overall_main_dict["test"] = test_m

    k = list(main_dict.keys())

    json_class_list = []
    model_id = processor_id

    model_region = region
    dataset_uri = get_train_gcs_uri(project_number, processor_id,location)
    train_percent = (
        train_size // (train_size + test_size)
        if (train_size + test_size) != 0
        else 0
    )

    for i in range(len(main_dict)):
        field = k[i]
        true_positive = main_dict[k[i]]["tp"]
        false_positive = main_dict[k[i]]["fp"]
        false_negative = main_dict[k[i]]["fn"]
        true_negative = main_dict[k[i]]["tn"]

        custom_logger.ml_logger(
            type_log="INFO",
            component="update_to_bq",
            message="START: INSERTING DATA IN BQ",
        )

        jsons_class = (
                "{"
                + '"model_name":"'
                + str(model_display_name)
                + '","job_id":"'
                + str(job_id)
                + '","processor_version_id":"'
                + str(processor_version_id)
                + '","model_id":"'
                + str(model_id)
                + '","version_name":"'
                + str(processor_version_name)
                + '","is_deployed":"'
                + str(is_deployed)
                + '","pipeline_name":"'
                + str(pipeline_name)
                + '","model_region":"'
                + str(model_region)
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
                + str(overall_main_dict["golden"]).replace("'", '"')
                + "} }"
        )

        jsons_class = json.loads(jsons_class)

        json_class_list.append(jsons_class)
        gcs_path_evaluation_csv = f"{data_pipeline_root}/evaluation_df.csv"


    jsons_model = (
            "[{"
            + '"model_name":"'
            + str(model_display_name)
            + '","job_id":"'
            + str(job_id)
            + '", "processor_version_id":"'
            + str(processor_version_id)
            + '", "model_id":"'
            + str(model_id)
            + '","version_name":"'
            + str(processor_version_name)
            + '","is_deployed":"'
            + str(is_deployed)
            + '","pipeline_name":"'
            + str(pipeline_name)
            + '","model_region":"'
            + str(model_region)
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
            + str(timestamp)
            + '","deployed_on":"'
            + str(timestamp)
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
    print(json_class_list)
    return jsons_model, json_class_list


def write_metrics_to_bq(
        model_display_name: str,
        job_id: str,
        processor_id: str,
        data_pipeline_root: str,
        project_number: str,
        ref_code_file_version: str,
        doc_type: str,
        project_id: str,
        region: str,
        timestamp: str,
        dataset_model: str,
        table_name_model: str,
        dataset_class: str,
        table_name_class: str,
        pipeline_name: str,
        configuration: str,
        is_deployed: str,
        location:str,
        gcs_path_model:str,
        version_name: Input[Artifact],
        overall_metrics: Input[Metrics],
        class_metrics: Input[Metrics],
):
    """
    Args:
        model_display_name: model display name
        job_id: job id
        processor_id: processor id
        data_pipeline_root: data pipeline root
        project_number: project number
        ref_code_file_version: file version
        doc_type: doc type
        project_id: project id
        region: region
        timestamp: timestamp
        dataset_model: dataset model
        table_name_model: table name model
        dataset_class: dataset class
        table_name_class: table name class
        pipeline_name: pipeline name
        configuration: configuration
        is_deployed: is deployed or not
        version_name: version name
        overall_metrics: overall metrics
        class_metrics: class metrics
    Return:
        error_class: error class
    """
    try:
        (
            processor_version_name,
            processor_version_id,
            class_dic,
            overall_dic,
        ) = get_metadata(version_name, class_metrics, overall_metrics)

        jsons_model, json_class_list = get_class_model_json(
            model_display_name,
            job_id,
            processor_id,
            data_pipeline_root,
            project_number,
            ref_code_file_version,
            doc_type,
            region,
            timestamp,
            pipeline_name,
            configuration,
            is_deployed,
            location,
            gcs_path_model,
            processor_version_name,
            processor_version_id,
            class_dic,
            overall_dic)

        bq = bigquery.Client()
        destination_table_model = bq.get_table(
            "{}.{}.{}".format(project_id, dataset_model, table_name_model)
        )
        bq.insert_rows(destination_table_model, jsons_model)

        destination_table_class = bq.get_table(
            "{}.{}.{}".format(project_id, dataset_class, table_name_class)
        )
        bq.insert_rows(destination_table_class, json_class_list)
    except Exception as e:
        custom_logger.ml_logger(
            type_log="ERROR",
            component="update_to_bq",
            message=f"{e}, EXception occured while updating to BQ ",
        )
        raise

def executor_main():
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
