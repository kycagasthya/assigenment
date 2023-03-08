# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

# Copyright 2020 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Creates and runs TF2 object detection models."""

import tensorflow.compat.v2 as tf
import model_lib_v2_mod as model_lib_v2
import argparse
import pandas as pd
import os
from typing import Tuple
from object_detection.utils import config_util
import traceback
from custlogger import ml_logger
from train_eval_utils import file_exist


def config_override(config_path: str, train_tf_rec_path: str,
                    test_tf_rec_path: str, label_map_path: str,
                    out_path: str, num_of_classes=None,
                    finetune_checkpoint=None, number_of_steps=None):
    """
    Override pipeline.config values with user defined values
    Parameters:
    ----------
    config_path : str
        pipeline config path
    label_map_path : str
        labelmap path
    train_tf_rec_path: str
        train_tfrecord path
    test_tf_rec_path: str
        artifact contain val_tfrecord
    out_path: str
        path to write updated config file
    num_of_classes: str
        best checkoint name
    Returns
    -------
    pipeline_config config object
        The produced dataframe
    """
    try:
        stats = file_exist(config_path)
        if not stats:
            message = "Config path doesnt exist, Given Path : {}".format(
                config_path)
            ml_logger(type_log="ERROR", component="Custom OD-train_eval",
                      message=message, status_code="500",
                      traceback="Edge case")
            raise Exception("Config path doesnt exist")
        pipeline_config_dict = config_util.get_configs_from_pipeline_file(
            config_path)
        if num_of_classes:
            meta_architecture = pipeline_config_dict["model"].WhichOneof(
                "model")
            if meta_architecture == "faster_rcnn":
                pipeline_config_dict[
                    "model"].faster_rcnn.num_classes = num_of_classes
            elif meta_architecture == "ssd":
                pipeline_config_dict["model"].ssd.num_classes = num_of_classes
            elif meta_architecture == "center_net":
                pipeline_config_dict[
                    "model"].center_net.num_classes = num_of_classes
        if finetune_checkpoint:
            checkpoint_stats = file_exist(config_path+".index")
            if checkpoint_stats:
                pipeline_config_dict[
                    "train_config"].fine_tune_checkpoint = finetune_checkpoint
            else:
                ml_logger(type_log="ERROR", component="Custom OD-train_eval",
                          message="Fine tune ckpt path doesnt exist",
                          status_code="500",
                          traceback="Edge case")
                raise Exception("Finetune ckpt path doesnt exist")
        if number_of_steps:
            pipeline_config_dict["train_config"].num_steps = number_of_steps
            pipeline_config_dict[
                "train_config"].optimizer.momentum_optimizer.learning_rate.\
                cosine_decay_learning_rate.total_steps = number_of_steps + 5000
        if not finetune_checkpoint:
            checkpoint_stats = file_exist(
                pipeline_config_dict[
                    "train_config"].fine_tune_checkpoint+".index")
            if not checkpoint_stats:
                ml_logger(type_log="ERROR", component="Custom OD-train_eval",
                          message="Default fine tune ckpt path doesnt exist",
                          status_code="500",
                          traceback="Edge case")
                raise Exception("Default fine tune ckpt path doesnt exist")
        label_stats = file_exist(label_map_path)
        if not label_stats:
            ml_logger(type_log="ERROR", component="Custom OD-train_eval",
                      message="label_map_path doesnt exist", status_code="500",
                      traceback="Edge case")
            raise Exception("label_map_path doesnt exist")
        pipeline_config_dict[
            "train_input_config"].label_map_path = label_map_path
        pipeline_config_dict[
            "train_input_config"].tf_record_input_reader.input_path[
            0] = train_tf_rec_path
        pipeline_config_dict[
            "eval_input_config"].label_map_path = label_map_path
        pipeline_config_dict[
            "eval_input_config"].tf_record_input_reader.input_path[
            0] = test_tf_rec_path
        pipeline_config = config_util.create_pipeline_proto_from_configs(
            pipeline_config_dict)
        config_util.save_pipeline_config(pipeline_config, out_path)
        return pipeline_config
    except Exception:
        ml_logger(type_log="ERROR", component="Custom OD-train_eval",
                  message="Exception in config_override",
                  status_code="500", traceback=traceback.format_exc())
        raise


def get_best_step(metric_csv_file: str, delta_map: float,
                  map_col_name: str="DetectionBoxes_Precision/mAP@.50IOU",
                  loss_col_name: str="Loss/total_loss") -> Tuple[
    int, float, float]:
    """
    it will extract the best best step, best loss, best map from trained data
    Parameters:
    ----------
    metric_csv_file : str
        contains all information about train iteration
    delta_map : float
        delta map
    map_col_name: str
        map column name
    loss_col_name: str
        loss column name
    Returns
    -------
    best_step int
        The produced dataframe
    best_loss float
        best loss
    best_map float
        float
    """
    try:
        best_step = -1
        best_loss = 0
        best_map = 0
        if not os.path.isfile(metric_csv_file):
            return best_step, best_loss, best_map
        df = pd.read_csv(metric_csv_file)
        if len(df.index) == 0:
            return best_step, best_loss, best_map
        idx_max_map = df[map_col_name].idxmax()
        idx_lowest_loss = df[loss_col_name].idxmin()
        if df.iloc[idx_max_map][map_col_name] - df.iloc[idx_lowest_loss][
                map_col_name] <= delta_map:
            best_step = df.iloc[idx_lowest_loss]["step"]
            best_loss = df.iloc[idx_lowest_loss][loss_col_name]
            best_map = df.iloc[idx_lowest_loss][map_col_name]
        else:
            best_step = df.iloc[idx_max_map]["step"]
            best_loss = df.iloc[idx_max_map][loss_col_name]
            best_map = df.iloc[idx_max_map][map_col_name]
        return best_step, best_loss, best_map
    except Exception:
        ml_logger(type_log="ERROR", component="Custom OD-train_eval",
                  message="Exception in get_best_step",
                  status_code="500", traceback=traceback.format_exc())
        raise


def train_and_eval(pipeline_config_path, model_dir, checkpoint_dir=None):
    """
    initiate training
    Parameters:
    ----------
    pipeline_config_path : str
        gcs path of pipeline
    model_dir : str
        model directory
    checkpoint_dir: str
        checkpoint directory
    Returns
    -------
    best_ckpt str
        The produced dataframe
    best_step float
        best loss
    best_loss float
        best loss
    best_map float
        float
    """
    try:
        args = argparse.Namespace()
        args.pipeline_config_path = pipeline_config_path
        args.model_dir = model_dir
        args.checkpoint_dir = \
        checkpoint_dir if not checkpoint_dir else model_dir
        args.eval_timeout = 3600
        args.num_train_steps = None
        args.eval_on_train_data = False
        args.sample_1_of_n_eval_examples = None
        args.sample_1_of_n_eval_on_train_examples = 5
        args.use_tpu = False
        args.tpu_name = None
        args.num_workers = 1
        args.checkpoint_every_n = 1000
        args.record_summaries = True
        tf.config.set_soft_device_placement(True)
        if args.use_tpu:
            # TPU is automatically inferred if tpu_name is None and
            # we are running under cloud ai-platform.
            resolver = tf.distribute.cluster_resolver.TPUClusterResolver(
                args.tpu_name)
            tf.config.experimental_connect_to_cluster(resolver)
            tf.tpu.experimental.initialize_tpu_system(resolver)
            strategy = tf.distribute.experimental.TPUStrategy(resolver)
        elif args.num_workers > 1:
            strategy = tf.distribute.experimental.MultiWorkerMirroredStrategy()
        else:
            strategy = tf.compat.v2.distribute.MirroredStrategy()
        with strategy.scope():
            model_lib_v2.train_loop(
                pipeline_config_path=args.pipeline_config_path,
                model_dir=args.model_dir,
                train_steps=args.num_train_steps,
                use_tpu=args.use_tpu,
                checkpoint_every_n=args.checkpoint_every_n,
                checkpoint_max_to_keep=None,
                record_summaries=args.record_summaries)
        model_lib_v2.eval_continuously(
            pipeline_config_path=args.pipeline_config_path,
            model_dir=args.model_dir,
            train_steps=args.num_train_steps,
            sample_1_of_n_eval_examples=args.sample_1_of_n_eval_examples,
            sample_1_of_n_eval_on_train_examples=(
                args.sample_1_of_n_eval_on_train_examples),
            checkpoint_dir=args.checkpoint_dir,
            wait_interval=300, timeout=args.eval_timeout)
        best_step, best_loss, best_map = get_best_step("metrics.csv", 0.05)
        if best_step != -1:
            best_ckpt = int(best_step // args.checkpoint_every_n)
            best_ckpt = best_ckpt + 1  # global_step 14000 is ckpt-15
        else:
            best_ckpt = 0
        best_ckpt = "ckpt-" + str(best_ckpt)
        return best_ckpt, best_step, best_loss, best_map
    except Exception:
        ml_logger(type_log="ERROR", component="Custom OD-train_eval",
                  message="Exception in train_and_eval",
                  status_code="500", traceback=traceback.format_exc())
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pipeline_config_path", type=str, required=True,
                        help="pipeline config path")
    parser.add_argument("--model_dir", type=str, required=True,
                        help="model dir")
    parser.add_argument("--checkpoint_dir", type=str, required=False,
                        default=None, help="checkpoint dir")
    args_main = parser.parse_args()
    train_and_eval(args_main.pipeline_config_path, args_main.model_dir,
                   args_main.checkpoint_dir)
