# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# ==============================================================================

from kfp.v2.dsl import Input, Metrics, Output, Artifact
from kfp.v2.components.executor import Executor
import google.auth
import google.auth.transport.requests
import requests
import json
import gcsfs
from docai.processor.v1.utils import helpers
import time
import pandas as pd
import traceback
from fuzzywuzzy import fuzz
from custom_logger import ml_logger as logger
import argparse
import ast


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
    credentials, _ = google.auth.default()
    credentials.refresh(authentication_request)
    token = credentials.token
    endpoint = f"{location}-documentai.googleapis.com"
    host = f"https://{endpoint}"
    url = f"{host}{url_substring}"
    return url, token


def deploy(project_id, processor_id, location, version_id):
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
        url_substring = f"/uiv1beta3/projects/{project_id}/locations" \
                        f"/{location}/processors/{processor_id}" \
                        f"/processorVersions/{version_id}:deploy"
        url, token = get_url(location, url_substring)
        response = requests.post(
            url, headers={"Authorization": f"Bearer {token}"}
        )
        logger("INFO", "evaluation", str(response.json()))

    except RuntimeError as error:
        trace = traceback.format_exc()
        logger("ERROR", "evaluation", error, "400", response.json(), trace)
    return response


def undeploy(project_id, processor_id, location, version_id):
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
    try:
        url_substring = f"/uiv1beta3/projects/{project_id}/locations/" \
                        f"{location}/processors/{processor_id}/" \
                        f"processorVersions/{version_id}:undeploy"
        url, token = get_url(location, url_substring)
        response = requests.post(
            url, headers={"Authorization": f"Bearer {token}"}
        )
        logger("INFO", "evaluation", str(response.json()))
    except RuntimeError as error:
        trace = traceback.format_exc()
        logger("ERROR", "evaluation", error, "400", response.json(), trace)
    return response


class CdeEvaluate:
    """
    Component to evaluate performance of the version of processor

    Args:
    project_id : The project id
    processor_id : The id of the processor to be trained
    version_id: The version id of the processor
    parser_keys: The keys required by parser
    ground_truth_csv: The csv file which contains the ground truth value
    doc_type:The type of the document(pancard,aadhar card)
    Returns:
    response: The json response generated after deploying

    """

    def __init__(
        self,
        project_id,
        pan_processor_id,
        version_id,
        location,
        parser_keys,
        ground_truth_csv,
        doc_type,
    ) -> None:
        self.project_id = project_id
        self.processor_id = pan_processor_id
        self.version_id = version_id
        self.location = location
        self.parser_keys = parser_keys
        self.ground_truth_csv = ground_truth_csv
        self.doc_type = doc_type

    def evaluate(self):
        """
        evaluate method of cde

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
        data = []
        ground_truth_dict = {}
        self.parser_keys.append("gcs_uri")
        fs = gcsfs.GCSFileSystem()
        with fs.open(self.ground_truth_csv, "r") as f:
            gcs_df = pd.read_csv(f)
            for _ , values in gcs_df.iterrows():
                record = {}
                for j in self.parser_keys:
                    ground_truth_dict[j] = values[j]
                labels = ground_truth_dict
                gcs_uri = labels["gcs_uri"]
                results = self.extract(gcs_uri)
                for key in self.parser_keys:
                    value_actual = labels[key]
                    value_pred = results[key]
                    record[f"{key}_pred"] = value_pred
                    record[f"{key}_actual"] = value_actual
                data.append(record)
            df, overall_metrics, cm_dict, metric_dict = self.get_metrics(data)
            return df, overall_metrics, cm_dict, metric_dict

    def get_metrics(self, data):
        """
        Method to create the metrics dictionary

        Arguments:
            data: the data records with actual and prediction values
        return:
            evaluation_df: evaluation
            overall_metrics: overall metrics
            classwise_metrics: classwise metrics
            cm_metrics: confusion metrics
        """
        df = pd.DataFrame.from_records(data=data)
        df = df.fillna("")
        if "gcs_uri" in self.parser_keys:
            self.parser_keys.remove("gcs_uri")
        for key in self.parser_keys:
            df[f"{key}_match_ratio"] = df[
                [f"{key}_actual", f"{key}_pred"]
            ].apply(self.find_ratio, axis=1)
        if "gcs_uri_pred" in df.columns:
            df.drop(["gcs_uri_pred"], axis=1, inplace=True)
        metric_dict = {}
        cm_dict = {}
        accuracy_list = []
        f1_list = []
        precision_list = []
        recall_list = []
        for i in self.parser_keys:
            metric_dict[i] = {}
            cm_dict[i] = {}
            total, _ = df.shape
            tp = df.query(f"{i}_match_ratio >= 100").shape[0]
            fn = len(df[df[f"{i}_match_ratio"] == ""])
            fp = df.query(f"{i}_match_ratio < 100").shape[0]
            tn = (tp + fn + fp) - (total)
            accuracy = (
                (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) else 0
            )
            accuracy_list.append(accuracy)
            precision = (tp) / (tp + fp) if (tp + fp) else 0
            precision_list.append(precision)
            recall = (tp) / (tp + fn) if (tp + fn) else 0
            recall_list.append(recall)
            cm_dict[i]["true_positive"] = tp
            cm_dict[i]["false_negative"] = fn
            cm_dict[i]["false_positive"] = fp
            cm_dict[i]["true_negative"] = tn
            f1_score = (
                2 * ((precision * recall) / (precision + recall))
                if (precision + recall)
                else 0
            )
            f1_list.append(f1_score)
            metric_dict[i]["true_positive"] = tp
            metric_dict[i]["false_negative"] = fn
            metric_dict[i]["false_positive"] = fp
            metric_dict[i]["true_negative"] = tn
            metric_dict[i]["accuracy"] = accuracy
            metric_dict[i]["precision"] = precision
            metric_dict[i]["recall"] = recall
            metric_dict[i]["f1_score"] = f1_score

        parser_f1 = (
            sum(f1_list) / len(self.parser_keys) if len(self.parser_keys) else 0
        )
        parser_precision = (
            sum(precision_list) / len(self.parser_keys)
            if len(self.parser_keys)
            else 0
        )
        parser_recall = (
            sum(recall_list) / len(self.parser_keys)
            if len(self.parser_keys)
            else 0
        )
        parser_accuracy = (
            sum(accuracy_list) / len(self.parser_keys)
            if len(self.parser_keys)
            else 0
        )
        overall_metrics = {
            "f1_score": parser_f1,
            "precision": parser_precision,
            "recall": parser_recall,
            "accuracy": parser_accuracy,
        }
        return df, overall_metrics, cm_dict, metric_dict

    def extract(self, gcs_uri):
        """
        method to extract predicted values and the confidence score

        Arguments:
            gcs_uri: input gcs uri
        return:
            output_dict: the dictionary with extracted prediction

        """
        fs = gcsfs.GCSFileSystem()
        with fs.open(gcs_uri, "rb") as image:
            image_bytes = image.read()
        pred = helpers.OnlinePred(
            self.project_id,
            self.processor_id,
            self.location,
            request_id="" ,
            page_id="",
            version_id=self.version_id
        )
        output = pred.mlops_predict_cde(image_bytes, self.doc_type)
        output_dict = {}
        conf_dict = {}
        for ent in self.parser_keys:
            output_dict[ent] = None
        for ent in self.parser_keys:
            conf_dict[ent] = 0
        for ent in output:
            if not output_dict[ent["key"]]:
                output_dict[ent["key"]] = ent["value"]
                conf_dict[ent["key"]] = ent["confidence"]
            else:
                if ent["confidence"] > conf_dict[ent["key"]]:
                    output_dict[ent["key"]] = ent["value"]
                    conf_dict[ent["key"]] = ent["confidence"]
        return output_dict
    def find_ratio(self, row):
        """
        method to find ratio of x&Y
        arguements:
        row(int): the row count
        returns:
        fuzz.ratio
        """
        x = str(row[0])
        y = str(row[1])
        return fuzz.ratio(x, y)


def get_test_metrics(project_id, processor_id, location, version_id):
    """
    Method for calling cde_evaluation and to
    get the evaluation metrics

    Args:
        project_id(str): gcp project_id
        processor_id(str) : doc AI processor ID
        location(str): location
        version_id(str): version id of the processor

    Returns:
        test_metrics(dict): metrics of test data of the processor
    """
    url_substring = f"/uiv1beta3/projects/{project_id}/locations/" \
                    f"{location}/processors/{processor_id}" \
                    f"/processorVersions/{version_id}"
    url, token = get_url(location, url_substring)
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    logger("INFO", "evaluation", response.json())
    test_metrics = response.json()["latestEvaluation"]["aggregateMetrics"]
    test_metrics["f1_score"] = test_metrics["f1Score"]
    del test_metrics["f1Score"]
    return test_metrics


def lro(lro_name: str, location: str, check_status_after: str):
    """
    Function to check lro status of deploy job
    Args:
        lro_name (str): lro_name
        location (str):location of the processor
        check_status_after (str):check_status_after
    Returns(string):
        Returns status of the deploy job
    """

    url_substring = f"/uiv1beta3/{lro_name}"
    url, token = get_url(location, url_substring)
    lro_response = requests.get(
        url, headers={"Authorization": f"Bearer {token}"}
    )

    try:
        lro_response_json = lro_response.json()
        status = lro_response_json["metadata"]["commonMetadata"]["state"]
    except Exception as error:
        trace = traceback.format_exc()
        if lro_response.text:
            logger(
                "ERROR",
                "Evaluation",
                error,
                str(lro_response.status_code),
                lro_response.json(),
                trace,
            )
        else:
            logger(
                "ERROR",
                "Evaluation",
                error,
                str(lro_response.status_code),
                traceback=trace,
            )
        raise

    while status not in ["SUCCEEDED"]:
        url, token = get_url(location, url_substring)
        response = requests.get(
            url, headers={"Authorization": f"Bearer {token}"}
        )
        try:
            response_json = response.json()
            status = response_json["metadata"]["commonMetadata"]["state"]
        except Exception as error:
            trace = traceback.format_exc()
            if response.text:
                logger(
                    "ERROR",
                    "Evaluation",
                    error,
                    str(response.status_code),
                    response.json(),
                    trace,
                )
            else:
                logger(
                    "ERROR",
                    "Evaluation",
                    error,
                    str(response.status_code),
                    traceback=trace,
                )
            raise

        if status == "RUNNING":
            logger(
                "INFO",
                "Evaluation",
                "Current state of the deploy-job is : RUNNING",
            )
        elif status == "CANCELLED":
            raise RuntimeError("The Deploy-job has been CANCELLED")
        elif status == "FAILED":
            raise RuntimeError("The Deploy-job has FAILED")
        time.sleep(int(check_status_after))

    return status


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
            url_substring = (
                f"/uiv1beta3/projects/{project_id}/locations/{location}/"
                f"processors/{processor_id}/processorVersions/"
            )
            url, token = get_url(location, url_substring)
            params = {"page_size": 20}
            response = requests.get(
            url, headers={"Authorization": f"Bearer {token}"}, params=params
            )
            res = response.json()

        except TypeError:
            logger("ERROR", "evaluate", "Invalid request for getting Status")

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
    except:
        logger(
            "ERROR",
            "evaluate",
            "Exception Occured while getting status of model",
        )
        raise
    return state

def processor_deployment(project_id: str, processor_id: str, version_id: str,
                         location: str, check_status_after: str,
                         retry_count: int, state: str)->str:
    """
    Function to do deployment based on the state of current deployment

    Args:
        project_id: project number of the processor
        processor_id: ID of the processor
        version_id: version of the model
        location: location of the processor
        check_status_after: to check lro status after every
                            check_status_after secs
        retry_count:The nos of retry attempts
        state: current deployment state
    Returns:
        deployment status of the model with the given version_id
    """
    if state == "UNDEPLOYED":
        try:
            deploy_response = deploy(project_id, processor_id,
                                     location, version_id)
            logger("INFO", "evaluation",
                   f"Deploy Response :{deploy_response.json()}")
            lro_name = deploy_response.json()["name"]
            status = lro(lro_name, location, check_status_after)
            if status == "SUCCEEDED":
                deploy_status = "DEPLOYED"
        except Exception as error:
            trace=traceback.format_exc()
            if deploy_response.text:
                logger("ERROR", "evaluation", error, "400",
                       deploy_response.json(), trace)
            else:
                logger("ERROR", "evaluation", error, "400", "", trace)
            raise
    elif state == "DEPLOYED":
        deploy_status = "DEPLOYED"
    elif state == "DEPLOYING":
        while int(retry_count) != 0:
            deploy_status = check_status(project_id, processor_id,
                                         version_id, location)
            if deploy_status == "DEPLOYED":
                break
            time.sleep(int(check_status_after))
            retry_count = int(retry_count) -1
        if deploy_status != "DEPLOYED":
            logger("ERROR", "evaluate", "Model could not be deployed")
            raise RuntimeError("Model not in deployed state")
    else:
        logger("ERROR", "evaluate", "Model in unknown state")
        raise RuntimeError("Current state of the deploy-job is : FAILED")

    return deploy_status


def evaluation(
    project_id: str,
    processor_id: str,
    location: str,
    data_pipeline_root: str,
    version_name: Input[Artifact],
    parser_keys: str,
    ground_truth_csv: str,
    doc_type: str,
    check_status_after: str,
    retry_count: str,
    overall_metrics: Output[Metrics],
    class_metrics: Output[Metrics],
):
    """
    Evaluation component for CDC

    Args:
        project_id(str): gcp project_id
        processor_id(str) : docai processor id
        location(str): location
        gcs_uri(str): gcs uri of eval df
        data_pipeline_root(str): data pipeline root folder
        parser_keys(str):the parser keys
        ground_truth_csv(str): the ground truth csv
        doc_type(str): the type of the document
        check_status_after(str): the interval for checking the status of
        lro is checked
        retry_count: the nos of retry attempts
        version_name: version name of the processor

    return:
        overall_metrics: overall metrics
        class_metrics: classwise metrics
    """
    try:
        parser_keys = ast.literal_eval(parser_keys)
        v_id = version_name.metadata["processor_version_id"]
        version_name = version_name.metadata["version_name"]
        logger(
        "INFO",
        "evaluation",
        f"processor_id :{processor_id}--location{location}--versionid: {v_id}"
        f"--versionname :{version_name}",
        )

        state = check_status(project_id, processor_id, v_id, location)
        deploy_status = processor_deployment(project_id, processor_id, v_id,
                                             location, check_status_after,
                                             retry_count, state)
        logger("INFO", "evaluate", f"Deploy status : {deploy_status}")

    except Exception as error:
        trace = traceback.format_exc()
        logger("ERROR", "evaluation", error, "400",state, trace)
        undeploy(project_id, processor_id, location, v_id)
        raise
    try:
        test_metrics = get_test_metrics(project_id, processor_id,
                                        location, v_id)
        logger("INFO", "evaluation", f"test_metrics : {test_metrics}")
        cde_eval = CdeEvaluate(
            project_id,
            processor_id,
            v_id,
            location,
            parser_keys,
            ground_truth_csv,
            doc_type,
        )
        (
            evaluation_df,
            golden_metrics,
            cm_metrics,
            classwise_metrics,
        ) = cde_eval.evaluate()
        #logger("INFO", "evaluation", f"golden_metrics : {golden_metrics}")
        logger("INFO", "evaluation", f"cm_metrics : {cm_metrics}")
        logger("INFO", "evaluation", f"classwise_metrics:{classwise_metrics}")

        for key in classwise_metrics:
            class_metrics.log_metric(
                key + "_precision", classwise_metrics[key]["precision"]
            )
            class_metrics.log_metric(
                key + "_f1-score", classwise_metrics[key]["f1_score"]
            )
            class_metrics.log_metric(
                key + "_recall", classwise_metrics[key]["recall"]
            )
            class_metrics.log_metric(
                key + "_accuracy", classwise_metrics[key]["accuracy"]
            )
            class_metrics.log_metric(
                key + "_tp", classwise_metrics[key]["true_positive"]
            )
            class_metrics.log_metric(
                key + "_fn", classwise_metrics[key]["false_negative"]
            )
            class_metrics.log_metric(
                key + "_fp", classwise_metrics[key]["false_positive"]
            )
            class_metrics.log_metric(
                key + "_tn", classwise_metrics[key]["true_negative"]
            )

        overall_metrics_comb = {"test": test_metrics, "golden": golden_metrics}
        for key in overall_metrics_comb:
            overall_metrics.log_metric(
                key + "_precision", overall_metrics_comb[key]["precision"]
            )
            overall_metrics.log_metric(
                key + "_f1-score", overall_metrics_comb[key]["f1_score"]
            )
            overall_metrics.log_metric(
                key + "_recall", overall_metrics_comb[key]["recall"]
            )
        logger("INFO", "evaluation", f"overall_metrics : {overall_metrics}")
        evaluation_df.to_csv(f"{data_pipeline_root}/evaluation_df.csv",\
                             index=False)
    except Exception as error:
        trace = traceback.format_exc()
        logger(
            "ERROR",
            "evaluation",
            "unable to evaluate metrics",
            "500",
            error,
            trace,
        )
        raise
    finally:
        undeploy(project_id, processor_id, location, v_id)


def executor_main():
    """
    Main execution function
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
