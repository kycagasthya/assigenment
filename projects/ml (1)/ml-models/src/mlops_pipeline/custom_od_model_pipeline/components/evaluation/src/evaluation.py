# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# ==============================================================================
"""This module will evaluate the trained model on golden dataset"""

import os
import argparse
import json
import pandas as pd
from google.cloud import storage
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from scf_parser import SignatureParser
import gcsfs
from typing import List, Tuple
from kfp.v2.dsl import Output, Input, Model, Metrics
from kfp.v2.components.executor import Executor
import traceback
from custlogger import ml_logger



def list_blobs(bucket_name: str, prefix: str):
    """Lists all the blobs in the bucket

    Parameters:
    ----------
    bucket_name: str
        Name of bucket contains evaluation images
    prefix: str
        Name of directory contains image files
    Returns
    -------
    path_list: List
        List contains gcs uri of images

    """
    storage_client = storage.Client()
    path_list = []
    # Note: Client.list_blobs requires at least package version 1.17.0.
    for blob in storage_client.list_blobs(bucket_name, prefix=prefix):
        if blob.name.endswith(".jpg") or blob.name.endswith(".png"):
            path = f"gs://{bucket_name}/{blob.name}"
            path_list.append(path)
    return path_list


def filepath_extraction(gs_path: str) -> List:
    """Generate file paths of images in evaluation set.

    Parameters:
    ----------
    gs_path : str
        List contains actual values
    Returns
    -------
    files: List
        List contains gcs uri of images
    """
    bucket = gs_path.split("/")[2]
    prefix = "/".join(gs_path.split("/")[3:])
    files = list_blobs(bucket, prefix)
    return files


def metric_calculation(
        actual: List, predicted: List) -> Tuple[
        int, int, int, int, float, float, float]:
    """Extract accuracy metrics from actual and predicted values.
    Parameters:
    ----------
    actual : List
        List contains actual values
    predicted: List
        List contains predicted values
    Returns
    -------
    (tn, fp, fn, tp, precision, recall, f1): Tuple
        Tuple contains accuracy metrics
    """
    confusion_values = confusion_matrix(actual, predicted).ravel()
    if len(confusion_values) == 4:
        tn, fp, fn, tp = confusion_values
    else:
        if actual[0]:
            tp = confusion_values[0]
            fp, fn, tn = 0, 0, 0
        else:
            tn = confusion_values[0]
            tp, fp, fn = 0, 0, 0
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = f1_score(actual, predicted)
    return tn, fp, fn, tp, precision, recall, f1


def start_evaluation(
        saved_model: Input[Model], threshold: str, test_data_path: str,
        out_csv_path: str, overall: Output[Metrics],
        classwise: Output[Metrics]):
    """
    Extract accuracy report from evaluation dataset
    Parameters:
    ----------
    saved_model : Input[Model]
        path to converted saved_model
    threshold: str
        Threshold value for prediction
    test_data_path: str
        Contains path to evaluation data
    Returns
    -------
    overall: Output[Metrics]
        contains overall accuracy metrics
    classwise: Output[Metrics]
        contains classwise accuracy metrics
    """
    try:
        fs = gcsfs.GCSFileSystem()
        ml_logger(type_log="INFO", component="Custom OD-Evaluation",
                  message="Evaluation Started", status_code="200")
        threshold = float(threshold)
        gcs_uris = []
        pred_primary = []
        pred_h1 = []
        pred_h2 = []
        actual_primary = []
        actual_h1 = []
        actual_h2 = []
        primary_confidence = []
        holder1_confidence = []
        holder2_confidence = []
        scf_ob = SignatureParser(saved_model.path, threshold)
        try:
            all_files = filepath_extraction(test_data_path)
        except Exception:
            ml_logger(type_log="ERROR", component="Custom OD-Evaluation",
                      message="Exception while fetching files",
                      status_code="500", traceback=traceback.format_exc())
            raise
        if len(all_files) == 0:
            ml_logger(type_log="ERROR", component="Custom OD-Evaluation",
                      message="No files in given directory",
                      status_code="500", traceback="Edge case: Empty input")
            raise Exception("No files in given directory")
        for fl in all_files:
            if fl.endswith(".jpg") or fl.endswith(".png"):
                if "one_signature" in fl:
                    actual_prime = True
                    actual_holder1 = False
                    actual_holder2 = False
                elif "two_signature" in fl:
                    actual_prime = True
                    actual_holder1 = True
                    actual_holder2 = False
                elif "three_signature" in fl:
                    actual_prime = True
                    actual_holder1 = True
                    actual_holder2 = True
                else:
                    continue
                gcs_uris.append(fl)
                cdc_json_path = fl[:-3] + "json"
                f = fs.open(fl, "rb")
                fl_bytes = f.read()
                js = fs.open(cdc_json_path, "r")
                cdc_json = json.load(js)
                out = scf_ob.extract(fl_bytes, cdc_json)
                pred_primary.append(out[0])
                primary_confidence.append(out[3])
                pred_h1.append(out[1])
                holder1_confidence.append(out[4])
                pred_h2.append(out[2])
                holder2_confidence.append(out[5])
                actual_primary.append(actual_prime)
                actual_h1.append(actual_holder1)
                actual_h2.append(actual_holder2)
        raw_prediction_df = pd.DataFrame(
            data=zip(gcs_uris, actual_primary, pred_primary, primary_confidence,
                     actual_h1, pred_h1, holder1_confidence, actual_h2, pred_h2,
                     holder2_confidence), columns=["gcs_uri", "actual_primary",
                                                   "pred_primary",
                                                   "primary_confidence",
                                                   "actual_h1",
                                                   "pred_h1",
                                                   "holder1_confidence",
                                                   "actual_h2", "pred_h2",
                                                   "holder2_confidence"])
        pred_csv_path = os.path.join(out_csv_path, "raw_predictions.csv")
        raw_prediction_df.to_csv(pred_csv_path, index=False)
        pred_total = pred_primary + pred_h1 + pred_h2
        actual_total = actual_primary + actual_h1 + actual_h2
        accuracy_primary = accuracy_score(actual_primary, pred_primary)
        accuracy_holder1 = accuracy_score(actual_h1, pred_h1)
        accuracy_holder2 = accuracy_score(actual_h2, pred_h2)
        p_tn, p_fp, p_fn, p_tp, p_precision, p_recall, p_f1 = \
            metric_calculation(actual_primary, pred_primary)
        h1_tn, h1_fp, h1_fn, h1_tp, h1_precision, h1_recall, h1_f1 = \
            metric_calculation(actual_h1, pred_h1)
        h2_tn, h2_fp, h2_fn, h2_tp, h2_precision, h2_recall, h2_f1 = \
            metric_calculation(actual_h2, pred_h2)
        tn, fp, fn, tp, model_precision, model_recall, model_f1 = \
            metric_calculation(actual_total, pred_total)
        avg_accuracy = (
            accuracy_primary + accuracy_holder1 + accuracy_holder2) / 3
        overall.log_metric("accuracy", round(float(avg_accuracy), 4))
        overall.log_metric("precision", round(float(model_precision), 4))
        overall.log_metric("recall", round(float(model_recall), 4))
        overall.log_metric("f1_score", round(float(model_f1), 4))
        overall.log_metric("tn", int(tn))
        overall.log_metric("tp", int(tp))
        overall.log_metric("fn", int(fn))
        overall.log_metric("fp", int(fp))
        classwise.log_metric("primary_accuracy",
                             round(float(accuracy_primary), 4))
        classwise.log_metric("primary_precision", round(float(p_precision), 4))
        classwise.log_metric("primary_recall", round(float(p_recall), 4))
        classwise.log_metric("primary_f1_score", round(float(p_f1), 4))
        classwise.log_metric("primary_tn", int(p_tn))
        classwise.log_metric("primary_tp", int(p_tp))
        classwise.log_metric("primary_fn", int(p_fn))
        classwise.log_metric("primary_fp", int(p_fp))
        classwise.log_metric("holder1_accuracy",
                             round(float(accuracy_holder1), 4))
        classwise.log_metric("holder1_precision", round(float(h1_precision), 4))
        classwise.log_metric("holder1_recall", round(float(h1_recall), 4))
        classwise.log_metric("holder1_f1_score", round(float(h1_f1), 4))
        classwise.log_metric("holder1_tn", int(h1_tn))
        classwise.log_metric("holder1_tp", int(h1_tp))
        classwise.log_metric("holder1_fn", int(h1_fn))
        classwise.log_metric("holder1_fp", int(h1_fp))
        classwise.log_metric("holder2_accuracy",
                             round(float(accuracy_holder2), 4))
        classwise.log_metric("holder2_precision", round(float(h2_precision), 4))
        classwise.log_metric("holder2_recall", round(float(h2_recall), 4))
        classwise.log_metric("holder2_f1_score", round(float(h2_f1), 4))
        classwise.log_metric("holder2_tn", int(h2_tn))
        classwise.log_metric("holder2_tp", int(h2_tp))
        classwise.log_metric("holder2_fn", int(h2_fn))
        classwise.log_metric("holder2_fp", int(h2_fp))
        ml_logger(type_log="INFO", component="Custom OD-Evaluation",
                  message="Evaluation Completed", status_code="200")
    except Exception:
        ml_logger(type_log="ERROR", component="Custom OD-Evaluation",
                  message="Exception in start_evaluation",
                  status_code="500", traceback=traceback.format_exc())
        raise


def executor_main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--executor_input", type=str)
    parser.add_argument("--function_to_execute", type=str)
    args, _ = parser.parse_known_args()
    executor_input = json.loads(args.executor_input)
    function_to_execute = globals()[args.function_to_execute]
    executor = Executor(executor_input=executor_input,
                        function_to_execute=function_to_execute)
    executor.execute()


if __name__ == "__main__":
    executor_main()
