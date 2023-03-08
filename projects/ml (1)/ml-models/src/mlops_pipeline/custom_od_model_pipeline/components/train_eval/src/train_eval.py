# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# ==============================================================================

"""This module will perform training and evaluation"""
import argparse
import json
import os
from kfp.v2.dsl import Output, Dataset, Input, Metrics, Artifact
from kfp.v2.components.executor import Executor
import traceback
from custlogger import ml_logger
from train_eval_utils import file_exist, delete_blob
import model_main_tf2_mod as model_main


def train_and_eval(
        pipeline_config_path: str,
        label_map_uri: str,
        pipeline_root: str,
        train_tfrecord: Input[Dataset],
        val_tfrecord: Input[Dataset],
        val_metrics: Output[Metrics],
        best_checkpoint: Output[Artifact]
):
    """
    Perform training with given data and informations
    Parameters:
    ----------
    pipeline_config_path : str
        pipeline config path
    label_map_uri : str
        labelmap path
    pipeline_root: str
        path to pipeline root folder
    train_tfrecord: Input[Dataset]
        artifact contain train_tfrecord
    val_tfrecord: Input[Dataset]
        artifact contain val_tfrecord
    val_metrics: Output[Metrics]
        accuracy mmetric of train anf test data
    best_checkpoint: Output[Artifact]
        best checkoint name
    Returns
    -------
    Pandas DataFrame
        The produced dataframe
    """
    try:
        ml_logger(type_log="INFO", component="Custom OD-Training",
                          message="Training Started", status_code="200")
        # config override
        train_tf_rec_path = train_tfrecord.uri
        test_tf_rec_path = val_tfrecord.uri
        train_tf_stats = file_exist(train_tf_rec_path)
        test_tf_stats = file_exist(test_tf_rec_path)
        if not train_tf_stats or not test_tf_stats:
            message = "tf_rec_path doesn't exist, Given Paths train : {} test: \
            {}".format(train_tf_rec_path, test_tf_rec_path)
            ml_logger(type_log="ERROR", component="Custom OD-train_eval",
                      message=message, status_code="500",
                      traceback="Edge case")
            raise Exception("tf record path doesn't exist")
        pipeline_config_dict = model_main.config_override(pipeline_config_path,
                                                          train_tf_rec_path,
                                                          test_tf_rec_path,
                                                          label_map_uri,
                                                          pipeline_root)
        if not pipeline_config_dict:
            raise Exception("config_override failed")
        updated_pipeline_config_path = os.path.join(pipeline_root,
                                                    "pipeline.config")
        model_dir = os.path.join(pipeline_root, "model_dir")
        # call train and eval
        best_ckpt, best_step, _, best_map = model_main.train_and_eval(
            pipeline_config_path=updated_pipeline_config_path,
            model_dir=model_dir, checkpoint_dir=model_dir)
        if best_step == -1:
            ml_logger(type_log="ERROR", component="Custom OD-Training",
                      message="Checkpoints not found",status_code="500",
                      traceback="Edge case")
            raise Exception("Checkpoints not found")
        best_checkpoint.metadata["best_ckpt"] = best_ckpt
        val_metrics.log_metric("best_map", float(best_map))
        try:
            delete_blob(
                train_tf_rec_path.split("/")[2],
                "/".join(train_tf_rec_path.split("/")[3:]))
            delete_blob(
                test_tf_rec_path.split("/")[2],
                "/".join(test_tf_rec_path.split("/")[3:]))
        except Exception:
            ml_logger(
                type_log="ERROR", component="Custom OD-Training",
                message="Exception while deleting tf records",
                status_code="500", traceback=traceback.format_exc())
            raise
        ml_logger(type_log="INFO", component="Custom OD-Training",
                          message="Training Completed", status_code="200")
    except Exception:
        ml_logger(
            type_log="ERROR", component="Custom OD-Training",
            message="Exception in train_and_eval",
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
