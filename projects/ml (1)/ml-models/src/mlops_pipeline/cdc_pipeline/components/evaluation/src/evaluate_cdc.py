# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# =============================================================================

"""This module will perform evaluation on golden dataset
and test data for cdc processor"""

from kfp.v2.dsl import Input, Metrics, Output, Artifact
from kfp.v2.components.executor import Executor
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from docai.processor.v1.utils import helpers
import gcsfs
import time
import pandas as pd
import traceback
import numpy as np
from custom_logger import ml_logger as logger
import google.auth
import google.auth.transport.requests
import requests
import argparse
import json

def get_url(location: str, url_substring: str)-> (str, str):
    """
    Function to return url and authentication token
    Args:
        location: location of the processor
        url_substring: url substring

    Returns:
        url: url for post/get request
        token: authentication token for post/get request
    """
    authentication_request = google.auth.transport.requests.Request()
    credentials, _ = google.auth.default()
    credentials.refresh(authentication_request)
    token = credentials.token
    endpoint = f"{location}-documentai.googleapis.com"
    host = f"https://{endpoint}"
    url = f"{host}{url_substring}"
    return url, token


def deploy(project_id: str, processor_id: str, location: str, version_id: str):
    """
    Component to deploy the version of processor
    Args:
        project_id : The project id
        processor_id : The id of the processor to be trained
        location : The location for the processor
        version_id: The version id of the processor

    Returns:
        response: The json response generated after deploying
    """
    try:
        url_substring = f"/uiv1beta3/projects/\
{project_id}/locations/{location}/\
processors/{processor_id}/processorVersions/{version_id}:deploy"
        url, token = get_url(location, url_substring)
        response = requests.post(
            url, headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except Exception:
        logger("ERROR", "evaluate", "Exception Occured while deploying")
        raise


def undeploy(
    project_id: str, processor_id: str, location: str, version_id: str
):
    """
    Component to undeploy the version of processor
    Args:
        project_id : The project id
        processor_id : The id of the processor to be trained
        location : The location for the processor
        version_id: The version id of the processor

    Returns:
        response: The json response generated after undeploying
    """

    url_substring = f"/uiv1beta3/projects/{project_id}/\
locations/{location}/processors/\
{processor_id}/processorVersions/{version_id}:undeploy"
    url, token = get_url(location, url_substring)
    response = requests.post(url, headers={"Authorization": f"Bearer {token}"})
    return response


def check_status(
    project_id: str, processor_id: str, version_id: str, location: str
) -> str:
    """
    checking status
    Arguments:
        project_id: input project id
        processor_id: input processor id
        version_id: input project version id
        location: input location
    return:
        state: return state
    """
    try:
        try:
            url_substring = f"/uiv1beta3/projects/{project_id}/\
locations/{location}/processors/\
{processor_id}/processorVersions/"
            url, token = get_url(location, url_substring)
            params = {"page_size": 20}
            response = requests.get(
                url, headers={"Authorization": f"Bearer {token}"}, params=params
            )
            res = response.json()

        except TypeError:
            logger("ERROR", "evaluate", "Invalid request for getting Status")
            raise
        loop = False
        version_list = []
        state = "UNDEPLOYED"

        for version in response.json()["processorVersions"]:
            version_list.append(version)
        if "nextPageToken" in res.keys():
            loop = True
        for _, val in enumerate(version_list):
            split = val["name"].rsplit("/")[-1]
            if split == version_id:
                loop = False
                state = val["state"]

        while loop is True:
            params = {"page_size": 20, "page_token": res["nextPageToken"]}
            response = requests.get(
                url, headers={"Authorization": f"Bearer {token}"}, params=params
            )
            res = response.json()
            if "nextPageToken" not in res.keys():
                loop = False
            for version in response.json()["processorVersions"]:
                version_list.append(version)

            for _, val in enumerate(version_list):
                split = val["name"].rsplit("/")[-1]
                if split == version_id:
                    loop = False
                    state = val["state"]
    except Exception:
        logger("ERROR", "evaluate",
               "Exception Occured while getting status of model")
        raise
    return state


def evaluate_cdc(
    project_id: str,
    processor_id: str,
    version_id: str,
    location: str,
    gcs_uri: str,
):
    """
    evaluation of cdc

    Arguments:
        project_id: input project id
        processor_id: input processor id
        version_id: input project version id
        location: input location
        gcs_uri: input gcs uri
    return:
        evaluation_df: evaluation
        overall_metrics: overall metrics
        classwise_metrics: classwise metrics
        cm_metrics: confusion metrics
    """
    try:
        fs = gcsfs.GCSFileSystem()
        evaluation_df = pd.read_csv(gcs_uri)
        predicted = []
        confidence = []
        path_list = evaluation_df["gcs_uri"].to_list()
        for file in path_list:
            with fs.open(file, "rb") as image:
                image_bytes = image.read()
            pred = helpers.OnlinePred(
                project_id,
                processor_id,
                location,
                request_id="",
                page_id="",
                version_id=version_id
            )
            output,conf,_  = pred.predict_cdc(image_bytes)
            predicted.append(output)
            confidence.append(conf)
            time.sleep(5)
        evaluation_df.loc[:, "predicted"] = predicted
        evaluation_df.loc[:, "confidence"] = confidence
        accuracy = accuracy_score(
            evaluation_df["ground_truth"], evaluation_df["predicted"]
        )
        report = classification_report(
            evaluation_df["ground_truth"],
            evaluation_df["predicted"],
            output_dict=True,
        )
        overall_metrics = {}
        overall_metrics["accuracy"] = accuracy
        overall_metrics["precision"] = report["macro avg"]["precision"]
        overall_metrics["recall"] = report["macro avg"]["recall"]
        overall_metrics["f1_score"] = report["macro avg"]["f1-score"]
        del report["accuracy"]
        del report["macro avg"]
        del report["weighted avg"]
        for key in report:
            df = evaluation_df[evaluation_df["ground_truth"] == key]
            if len(df) == 0:
                report[key]["accuracy"] = 0
            else:
                report[key]["accuracy"] = accuracy_score(
                    df["ground_truth"], df["predicted"]
                )
            del report[key]["support"]
        classwise_metrics = report
        cm = confusion_matrix(
            evaluation_df["ground_truth"], evaluation_df["predicted"]
        )
        fp = cm.sum(axis=0) - np.diag(cm)
        fn = cm.sum(axis=1) - np.diag(cm)
        tp = np.diag(cm)
        tn = cm.sum() - (fp + fn + tp)
        cm_metrics = {}
        for i, label in enumerate(report):
            cm_metrics[label] = {
                "true_positives": int(tp[i]),
                "true_negatives": int(tn[i]),
                "false_positives": int(fp[i]),
                "false_negatives": int(fn[i]),
            }
        return evaluation_df, overall_metrics, classwise_metrics, cm_metrics
    except Exception:
        logger("ERROR", "evaluate",
               "Exception Occured while calculating metrics")
        raise


def lro(lro_name, location, check_status_after):
    """
    Function to check lro status of deploy job

    Args:
        lro_name (str): lro_name
        location (str):location of the processor
        check_status_after (str): time interval in millisecs
                                after which status is checked
    Returns(string):
        status: Returns status of the deploy job
    """
    try:
        if lro_name is not None:
            url_substring = f"/uiv1beta3/{lro_name}"
            url, token = get_url(location, url_substring)
            response = requests.get(
                url, headers={"Authorization": f"Bearer {token}"}
            )
            status = response.json()["metadata"]["commonMetadata"]["state"]
            while status not in ["SUCCEEDED"]:
                url, token = get_url(location, url_substring)
                response = requests.get(
                    url, headers={"Authorization": f"Bearer {token}"}
                ).json()
                status = response["metadata"]["commonMetadata"]["state"]
                if status == "RUNNING":
                    logger("INFO", "evaluate",
                           "Current state of the deploy-job is : RUNNING")
                elif status == "CANCELLED":
                    logger("ERROR", "evaluate",
                           "Current state of the deploy-job is : CANCELLED")
                    raise RuntimeError(
                        "Current state of the deploy-job is : CANCELLED"
                    )
                elif status == "FAILED":
                    logger("ERROR", "evaluate",
                           "Current state of the deploy-job is : FAILED")
                    raise RuntimeError(
                        "Current state of the deploy-job is : FAILED"
                    )
                time.sleep(int(check_status_after))
            logger("INFO", "evaluate", "MODEL GOT DEPLOYED")
        else:
            logger("ERROR", "evaluate", "LRO name is null ,could not evaluate")
            raise RuntimeError("Could not fetch lro name")
        return status
    except RuntimeError:
        logger("ERROR", "evaluate", "failed fetch lro")
        raise


def get_test_metrics(
    project_id: str, processor_id: str, location: str, version_id: str
):
    """
    Method for calling cdc_evaluation and to
    get the evaluation metrics

    Args:
        project_id(str): gcp project_id
        processor_id(str) : doc AI processor ID
        location(str): location
        version_id(str): version id of the processor

    Returns:
        test_metrics(dict): metrics of test data of the processor
    """
    url_substring = f"/uiv1beta3/projects/{project_id}/locations/{location}/\
processors/{processor_id}/processorVersions/{version_id}"
    url, token = get_url(location, url_substring)
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    test_metrics = response.json()["latestEvaluation"]["aggregateMetrics"]
    test_metrics["f1_score"] = test_metrics["f1Score"]
    del test_metrics["f1Score"]
    return test_metrics

def processor_deployment(project_id: str, processor_id: str, version_id: str,
                     location: str, check_status_after: str,
                         retry_count:int, status: str)->str:
    """
    Function to do deployment based on the status of current deployment

    Args:
        project_id: project number of the processor
        processor_id: ID of the processor
        version_id: version of the model
        location: location of the processor
        check_status_after: to check lro status after every
                            check_status_after secs
        retry_count:the nos of retry attempts
        status: current deployment status
    Returns:
        deployment status of the model with the given version_id
    """
    try:
        if status == "UNDEPLOYED":
            deploy_response = deploy(
                project_id, processor_id, location, version_id
            )
            deploy_response_json = deploy_response.json()
            if "error" in deploy_response_json.keys():
                if "status" in deploy_response_json["error"].keys():
                    if deploy_response_json["error"]["status"] == "NOT_FOUND":
                        logger("ERROR", "evaluate", "unknown", "",
                               deploy_response_json)
                        raise RuntimeError("processor Id could not be found")
            lro_name = None
            if "name" in deploy_response_json.keys():
                lro_name = deploy_response_json["name"]
            else:
                raise RuntimeError("Something went wrong with deploy request")
            status = lro(lro_name, location, check_status_after)
            if status == "SUCCEEDED":
                deploy_status = "DEPLOYED"
        elif status == "DEPLOYING":
            while int(retry_count) != 0:
                deploy_status = check_status(
                    project_id, processor_id, version_id, location
                )
                if deploy_status == "DEPLOYED":
                    break
                time.sleep(int(check_status_after))
                retry_count = int(retry_count) - 1
            if deploy_status != "DEPLOYED":
                logger("ERROR", "evaluate", "Model could not be deployed")
                raise RuntimeError("Model not in deployed state")
        elif status == "DEPLOYED":
            deploy_status = "DEPLOYED"
        else:
            logger("ERROR", "evaluate", "Model in unknown state")
            raise RuntimeError("Current state of the deploy-job is : FAILED")
    except RuntimeError as error:
        trace = traceback.format_exc()
        logger("ERROR", "evaluate", error, traceback=trace)
        raise
    except Exception as error:
        trace = traceback.format_exc()
        logger("ERROR", "evaluate", error, traceback=trace)
        raise

    return deploy_status


def evaluation(
    project_id: str,
    processor_id: str,
    location: str,
    gcs_uri: str,
    data_pipeline_root: str,
    check_status_after: str,
    retry_count: int,
    input_version_id: Input[Artifact],
    overall_metrics: Output[Metrics],
    class_metrics: Output[Metrics],
):

    """
    Evaluation component for CDC

    Args:
        project_id(str): gcp project_id
        processor_id(str) : doc AI processor ID
        location(str): location
        gcs_uri(str): gcs uri of eval df
        data_pipeline_root(str): data pipeline root
        check_status_after(str): time interval in millisecs
                                after which status is checked
        retry_count: the retry attempts
        input_version_id(str): version id

    return:
        overall_metrics: overall metrics
        class_metrics: classwise metrics
    """
    logger("INFO", "evaluate", "Calling CDC evaluation method")

    try:
        version_id = input_version_id.metadata["processor_version_id"]
        status = check_status(project_id, processor_id, version_id, location)
        deploy_status = processor_deployment(project_id, processor_id,
                                             version_id, location,
                                             check_status_after,
                                             retry_count,status)
        logger("INFO", "evaluate", f"Deploy status : {deploy_status}")

        test_metrics = get_test_metrics(
            project_id, processor_id, location, version_id
        )
        logger("INFO", "evaluate", f"test_metrics: {test_metrics}")
        (
            evaluation_df,
            golden_metrics,
            classwise_metrics,
            cm_metrics,
        ) = evaluate_cdc(
            project_id, processor_id, version_id, location, gcs_uri
        )
        logger("INFO", "evaluate", f"golden_metrics: {golden_metrics}")
        logger("INFO", "evaluate", f"classwise_metrics: {classwise_metrics}")
        logger("INFO", "evaluate", f"cm_metrics: {cm_metrics}")
        for key in classwise_metrics:
            class_metrics.log_metric(
                key + "_precision", classwise_metrics[key]["precision"]
            )
            class_metrics.log_metric(
                key + "_f1-score", classwise_metrics[key]["f1-score"]
            )
            class_metrics.log_metric(
                key + "_recall", classwise_metrics[key]["recall"]
            )
            class_metrics.log_metric(
                key + "_accuracy", classwise_metrics[key]["accuracy"]
            )

        for key in cm_metrics:
            class_metrics.log_metric(
                key + "_tp", cm_metrics[key]["true_positives"]
            )
            class_metrics.log_metric(
                key + "_tn", cm_metrics[key]["true_negatives"]
            )
            class_metrics.log_metric(
                key + "_fp", cm_metrics[key]["false_positives"]
            )
            class_metrics.log_metric(
                key + "_fn", cm_metrics[key]["false_negatives"]
            )
        overall_metrics_comb = {"test": test_metrics, "golden": golden_metrics}
        for key in overall_metrics_comb:
            overall_metrics.log_metric(
                key + "_precision", overall_metrics_comb[key]["precision"]
            )
            overall_metrics.log_metric(
                key + "_f1_score", overall_metrics_comb[key]["f1_score"]
            )
            overall_metrics.log_metric(
                key + "_recall", overall_metrics_comb[key]["recall"]
            )
            if key == "golden":
                overall_metrics.log_metric(
                    key + "_accuracy", overall_metrics_comb[key]["accuracy"]
                )
        evaluation_df.to_csv(
            f"{data_pipeline_root}/evaluation_df.csv", index=False
        )
    except RuntimeError:
        trace = traceback.format_exc()
        logger("ERROR", "evaluate", traceback=trace)
        raise
    finally:
        undeploy(project_id, processor_id, location, version_id)


def executor_main():
    """
    The main executor function
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
