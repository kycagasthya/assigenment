# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# =============================================================================
import os
import traceback
from kfp.v2.components.executor import Executor
from kfp.v2.dsl import Input, Metrics
from google.cloud import bigquery
import gcsfs
import json
from custlogger import ml_logger
import argparse


def get_classwise_metrics(
    overall_metrics: dict, classwise_metrics: dict, overall_metrics_model: dict
):
    """
    function to get the classwise_json and metrics_json
    :param overall_metrics: metrics of the model
    :param classwise_metrics: metrics for each class of the model
    :param overall_metrics_model: map of the model
    :return: classwise_json_path_data, metrics_json_path_data
    """

    metrics_json_path_data = {
        "test": {"map": overall_metrics_model.metadata["best_map"]},
        "golden": {
            "f1_score": overall_metrics.metadata["f1_score"],
            "precision": overall_metrics.metadata["precision"],
            "recall": overall_metrics.metadata["recall"],
            "accuracy": overall_metrics.metadata["accuracy"],
        },
    }

    # loading value from classwise_metrics
    classwise_json_path_data = {
        "primary_sign": {
            "TP": classwise_metrics.metadata["primary_tp"],
            "FN": classwise_metrics.metadata["primary_fn"],
            "FP": classwise_metrics.metadata["primary_fp"],
            "TN": classwise_metrics.metadata["primary_tn"],
            "accuracy": classwise_metrics.metadata["primary_accuracy"],
            "precision": classwise_metrics.metadata["primary_precision"],
            "recall": classwise_metrics.metadata["primary_recall"],
            "f1_score": classwise_metrics.metadata["primary_f1_score"],
        },
        "holder1_sign": {
            "TP": classwise_metrics.metadata["holder1_tp"],
            "FN": classwise_metrics.metadata["holder1_fn"],
            "FP": classwise_metrics.metadata["holder1_fp"],
            "TN": classwise_metrics.metadata["holder1_tn"],
            "accuracy": classwise_metrics.metadata["holder1_accuracy"],
            "precision": classwise_metrics.metadata["holder1_precision"],
            "recall": classwise_metrics.metadata["holder1_recall"],
            "f1_score": classwise_metrics.metadata["holder1_f1_score"],
        },
        "holder2_sign": {
            "TP": classwise_metrics.metadata["holder2_tp"],
            "FN": classwise_metrics.metadata["holder2_fn"],
            "FP": classwise_metrics.metadata["holder2_fp"],
            "TN": classwise_metrics.metadata["holder2_tn"],
            "accuracy": classwise_metrics.metadata["holder2_accuracy"],
            "precision": classwise_metrics.metadata["holder2_precision"],
            "recall": classwise_metrics.metadata["holder2_recall"],
            "f1_score": classwise_metrics.metadata["holder2_f1_score"],
        },
    }

    return classwise_json_path_data, metrics_json_path_data


def get_json_class(
    model_name: str,
    job_id: str,
    doc_type: str,
    model_region: str,
    model_id: str,
    version_name: str,
    is_deployed: str,
    classwise_json_path_data: dict,
    pipeline_name: str,
    processor_version_id: str,
):
    """

    :param model_name: Name of the model
    :param job_id: id of the job
    :param doc_type: doc parser type
    :param model_region: region of the model
    :param model_id: id of the model
    :param version_name: version of the trained model
    :param is_deployed: is model deployed or not
    :param classwise_json_path_data: json of the class of model
    :param pipeline_name: name of the pipeline
    :param processor_version_id: version id of the processor
    :return: json_class_list
    """

    k = list(classwise_json_path_data.keys())

    json_class_list = []
    for i in range(len(classwise_json_path_data)):
        field = k[i]
        v = classwise_json_path_data[k[i]]
        true_positive = v["TP"]
        false_positive = v["FP"]
        false_negative = v["FN"]
        true_negative = v["TN"]
        score_json = str(dict(list(v.items())[4:])).replace("'", '"')
        json_class = {}
        try:
            json_class = (
                "{"
                + '"model_name":"'
                + str(model_name)
                + '","job_id":"'
                + str(job_id)
                + '","processor_version_id":"'
                + str(processor_version_id)
                + '","model_id":"'
                + str(model_id)
                + '","version_name":"'
                + str(version_name)
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
                + score_json
                + "} }"
            )
        except TypeError as e:
            ml_logger(
                type_log="ERROR",
                component="od_bq",
                message="unable to create json_class",
                status_code="500",
                json_response={"ml_logger": str(e)},
                traceback=str(traceback.format_exc()),
            )
            raise "unable to create json_class"

        json_class = json.loads(json_class)
        json_class_list.append(json_class)

    return json_class_list


def get_train_test_size(train_test_count):
    """
    :param train_test_count: train and test count from metrics
    :return: train_size, test_size
    """
    train_size = int(train_test_count["train_size"])
    test_size = int(train_test_count["test_size"])

    return train_size, test_size


def get_json_model(
    model_name: str,
    job_id: str,
    ref_code_file_version: str,
    model_region: str,
    timestamp: str,
    gcs_path_model: str,
    configuration: str,
    model_id: str,
    version_name: str,
    is_deployed: str,
    gcs_path_evaluation_csv: str,
    pipeline_name: str,
    processor_version_id: str,
    gcs_ref_training_data: str,
    metrics_json_path_data: dict,
    train_size: int,
    test_size: int,
):
    """

    :param model_name: Name of the model
    :param job_id: id of the job
    :param ref_code_file_version: reference of the file version
    :param model_region: region of the model
    :param timestamp: time stamp in human-readable format.
    :param gcs_path_model: storage location of the model
    :param configuration: configuration of the model
    :param model_id: id of the model
    :param version_name: version of the model
    :param is_deployed:is model deployed or not
    :param gcs_path_evaluation_csv:location of csv
    :param pipeline_name: name of the pipeline
    :param processor_version_id: version of the processor
    :param gcs_ref_training_data: storage location of training data.
    :param metrics_json_path_data: json from the metrics
    :param train_size: size of train data
    :param test_size: size of test data
    :return:json file called json_model
    """

    if (train_size + test_size) == 0:
        raise ZeroDivisionError("check train_size and test_size")
    train_percent = int(train_size / (train_size + test_size) * 100)

    json_model = {}
    try:
        json_model = (
            "[{"
            + '"model_name":"'
            + str(model_name)
            + '","job_id":"'
            + str(job_id)
            + '","processor_version_id":"'
            + str(processor_version_id)
            + '","model_id":"'
            + str(model_id)
            + '",'
            '"version_name":"'
            + str(version_name)
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
            + str(gcs_ref_training_data)
            + '","trained_on":"'
            + str(timestamp)
            + '","deployed_on":"'
            + str(timestamp)
            + '","score":'
            + str(metrics_json_path_data).replace("'", '"')
            + ',"gcs_path_evaluation_csv":"'
            + str(gcs_path_evaluation_csv)
            + '","gcs_path_model":"'
            + str(gcs_path_model)
            + '","configuration":"'
            + str(configuration).replace('"', "'")
            + '"}]'
        )
    except TypeError as e:
        ml_logger(
            type_log="ERROR",
            component="od_bq",
            message="unable to create json_model",
            status_code="500",
            json_response={"ml_logger": str(e)},
            traceback=str(traceback.format_exc()),
        )
        raise "unable to create json_model"
    json_model = json.loads(json_model)

    return json_model


def write_metrics_to_bq(
    model_name: str,
    job_id: str,
    ref_code_file_version: str,
    doc_type: str,
    project_id: str,
    model_region: str,
    timestamp: str,
    dataset_model: str,
    table_name_model: str,
    dataset_class: str,
    table_name_class: str,
    configuration: str,
    model_id: str,
    version_name: str,
    is_deployed: str,
    data_pipeline_root: str,
    overall_metrics: Input[Metrics],
    classwise_metrics: Input[Metrics],
    overall_metrics_model: Input[Metrics],
    pipeline_name: str,
    processor_version_id: str,
    gcs_ref_training_data: str,
):

    """

    :param model_name: Name of the model
    :param job_id:id of the job
    :param ref_code_file_version:reference of the file version
    :param doc_type: type of the document parser
    :param project_id: id of the processor
    :param model_region: region of the model
    :param timestamp:time stamp in human-readable format.
    :param dataset_model: dataset of the model in bq
    :param table_name_model: table of the model in bq
    :param dataset_class:dataset of the class in bq
    :param table_name_class:table of the class in bq
    :param configuration: configuration of the model
    :param model_id: id of the model
    :param version_name: name of the version
    :param is_deployed:is model deployed or not
    :param data_pipeline_root: root folder of csv
    :param overall_metrics: overall metrics of the model
    :param classwise_metrics: class wise metrics of the model
    :param overall_metrics_model: overall metrics of the model
    :param pipeline_name: name of the pipeline
    :param processor_version_id: id of the processor version
    :param gcs_ref_training_data: location of training data
    :param train_test_count: compined data count
    :return: None
    """
    fs = gcsfs.GCSFileSystem()
    train_test_count_path = os.path.join(data_pipeline_root, "data_count.json")
    with fs.open(train_test_count_path, "r") as fp:
        train_test_count = json.load(fp)
    gcs_path_evaluation_csv = os.path.join(
        data_pipeline_root, "raw_predictions.csv"
    )
    gcs_path_model = os.path.join(data_pipeline_root, "bytes_model")

    train_size, test_size = get_train_test_size(train_test_count)

    classwise_json_path_data, metrics_json_path_data = get_classwise_metrics(
        overall_metrics, classwise_metrics, overall_metrics_model
    )

    json_class_list = get_json_class(
        model_name,
        job_id,
        doc_type,
        model_region,
        model_id,
        version_name,
        is_deployed,
        classwise_json_path_data,
        pipeline_name,
        processor_version_id,
    )

    json_model = get_json_model(
        model_name,
        job_id,
        ref_code_file_version,
        model_region,
        timestamp,
        gcs_path_model,
        configuration,
        model_id,
        version_name,
        is_deployed,
        gcs_path_evaluation_csv,
        pipeline_name,
        processor_version_id,
        gcs_ref_training_data,
        metrics_json_path_data,
        train_size,
        test_size,
    )

    bq = bigquery.Client()
    destination_table_model = bq.get_table(
        "{}.{}.{}".format(project_id, dataset_model, table_name_model)
    )
    error_model = bq.insert_rows(destination_table_model, json_model)
    if len(error_model) == 0:
        ml_logger(
            type_log="INFO",
            component="od_bq",
            message="row added to model table in bq",
            status_code="200",
        )
    if len(error_model) != 0:
        ml_logger(
            type_log="ERROR",
            component="od_bq",
            message="row not added to model table in bq",
            status_code="500",
            json_response={"ml_logger": str(error_model)},
            traceback=str("error while adding data to BQ"),
        )
        raise Exception("unable to add row to table_model")
    destination_table_class = bq.get_table(
        "{}.{}.{}".format(project_id, dataset_class, table_name_class)
    )
    error_class = bq.insert_rows(destination_table_class, json_class_list)
    if len(error_class) == 0:
        ml_logger(
            type_log="INFO",
            component="od_bq",
            message="row added to class table in bq",
            status_code="200",
        )
    if len(error_class) != 0:
        ml_logger(
            type_log="ERROR",
            component="od_bq",
            message="row not added to class table in bq",
            status_code="500",
            json_response={"ml_logger": str(error_class)},
            traceback=str("error while adding data to BQ"),
        )
        raise Exception("unable to add row to table_class")


def executor_main():
    """
    main function to execute write_metrics_to_bq function
    return:
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
