# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# ==============================================================================

import os
import argparse
import json
import tensorflow.compat.v2 as tf
from google.protobuf import text_format
from object_detection import exporter_lib_v2
from object_detection.protos import pipeline_pb2
from kfp.v2.dsl import Output, Input, Artifact, Model
from kfp.v2.components.executor import Executor
import ast
from google.cloud import storage
import gcsfs
import traceback
from custlogger import ml_logger
tf.enable_v2_behavior()
client = storage.Client()


def convert_model_input(
        saved_model_path: str, target_path: str, input_size: tuple):
    """
    Convert saved model to accept imagesbytes as input
    Parameters:
    ----------
    saved_model_path : str
        The path containing saved_model.pb
    target_path: str
        Destination path to save converted model
    input_size: tuple
        size of input image
    """
    try:
        model = tf.saved_model.load(saved_model_path)

        def _preprocess(bytes_inputs):
            decoded = tf.io.decode_jpeg(bytes_inputs, channels=3)
            resized = tf.image.resize(decoded, size=input_size)
            return tf.cast(resized, dtype=tf.uint8)

        def _get_serve_image_fn(model):
            @tf.function(input_signature=[tf.TensorSpec([None], tf.string)])
            def serve_image_fn(bytes_inputs):
                decoded_images = tf.map_fn(
                    _preprocess, bytes_inputs, dtype=tf.uint8)
                return model(decoded_images)
            return serve_image_fn
        signatures = {
            "serving_default": _get_serve_image_fn(model).get_concrete_function(
                tf.TensorSpec(shape=[None], dtype=tf.string)
                )
            }
        tf.saved_model.save(model, target_path, signatures=signatures)
    except Exception:
        ml_logger(
            type_log="ERROR", component="Custom OD-Model Export",
            message="Exception in export_model",
            status_code="500", traceback=traceback.format_exc())
        raise

def export_model(
        output_directory: str,
        input_size: str,
        checkpoint: Input[Artifact],
        deployable_model: Output[Model]):
    """
    Function will export ckpt files to saved_model.pb
    Parameters:
    ----------
    input_type : str
        Input type of model
    pipeline_config_path: str
        Path to config file
    trained_checkpoint_dir: str
        Path to trained checkpints
    output_directory: str
        Path to export saved_model.pb
    input_size: tuple
        size of input image
    checkpoint: Input[Artifact]
        contains best check point name
    deployable_model: Output[Model]
        contains uri of converted saved model
    """
    try:
        fs = gcsfs.GCSFileSystem()
        input_type = "image_tensor"
        pipeline_config_path = os.path.join(output_directory, "pipeline.config")
        trained_checkpoint_dir = os.path.join(output_directory, "model_dir")
        ml_logger(type_log="INFO", component="Custom OD-Model Export",
                  message="Model export component started.", status_code="200")
        checkpoint_line = 'model_checkpoint_path : "'+\
        checkpoint.metadata["best_ckpt"]+'"'
        checkpoint_metadata_path = os.path.join(
            trained_checkpoint_dir, "checkpoint")
        train_bucket_name = trained_checkpoint_dir.split("/")[2]
        ckpt_path = os.path.join(
            "/".join(trained_checkpoint_dir.split("/")[3:]),
            checkpoint.metadata["best_ckpt"] + ".index")
        train_bucket = client.bucket(train_bucket_name)
        train_stats = storage.Blob(
            bucket=train_bucket, name=ckpt_path).exists(client)
        if not train_stats:
            ml_logger(
                type_log="ERROR", component="Custom OD-Model Export",
                message="Checkpoint doesnt exist,please check the ckpt dir",
                status_code="500", traceback="Edge case")
            raise Exception("Checkpoint doesnt exist,please check the ckpt dir")
        config_bucket_name = pipeline_config_path.split("/")[2]
        cofig_path = "/".join(pipeline_config_path.split("/")[3:])
        config_bucket = client.bucket(config_bucket_name)
        cofig_stats = storage.Blob(
            bucket=config_bucket, name=cofig_path).exists(client)
        if not cofig_stats:
            ml_logger(
                type_log="ERROR", component="Custom OD-Model Export",
                message="Config file doesnt exist,please check the path",
                status_code="500", traceback="Edge case")
            raise Exception("Config file doesnt exist,please check the path")
        numpy_model_directory = os.path.join(output_directory, "numpy_model")
        bytes_mode_deirectory = os.path.join(output_directory, "bytes_model")
        with fs.open(checkpoint_metadata_path, "w") as f:
            f.write(checkpoint_line)
        input_size = ast.literal_eval(input_size)
        pipeline_config = pipeline_pb2.TrainEvalPipelineConfig()
        with tf.io.gfile.GFile(pipeline_config_path, "r") as f:
            text_format.Merge(f.read(), pipeline_config)
        exporter_lib_v2.export_inference_graph(
            input_type, pipeline_config,
            trained_checkpoint_dir, numpy_model_directory)
        saved_model_path = os.path.join(numpy_model_directory, "saved_model")
        convert_model_input(saved_model_path, bytes_mode_deirectory, input_size)
        deployable_model.path = bytes_mode_deirectory
        ml_logger(type_log="INFO", component="Custom OD-Model Export",
                  message="Model export component Completed.",
                  status_code="200")
    except Exception:
        ml_logger(
            type_log="ERROR", component="Custom OD-Model Export",
            message="Exception in export_model",
            status_code="500", traceback=traceback.format_exc())
        raise


def executor_main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--executor_input", type=str)
    parser.add_argument("--function_to_execute", type=str)
    args, _ = parser.parse_known_args()
    executor_input = json.loads(args.executor_input)
    function_to_execute = globals()[args.function_to_execute]
    executor = Executor(
        executor_input=executor_input, function_to_execute=function_to_execute)
    executor.execute()


if __name__ == "__main__":
    executor_main()
