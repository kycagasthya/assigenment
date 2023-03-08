# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# =============================================================================
import unittest
from unittest.mock  import patch
from unittest import mock
import sys
from os.path import dirname, abspath
current_dir = abspath(dirname(__file__))
sys.path.insert(
    0, "src/mlops_pipeline/custom_od_model_pipeline/components/train_eval/src")
mocked_tf = mock.MagicMock()
mocked_tf_v2 = mock.MagicMock()
mocked_object_detection = mock.MagicMock()
mocked_utils = mock.MagicMock()
mocked_builders = mock.MagicMock()
mocked_core = mock.MagicMock()
mocked_protos = mock.MagicMock()
sys.modules["tensorflow"] = mocked_tf_v2
sys.modules["tensorflow.compat.v2"] = mocked_tf_v2
sys.modules["tensorflow.compat.v1"] = mocked_tf
sys.modules["object_detection"] = mocked_object_detection
sys.modules["object_detection.utils"] = mocked_utils
sys.modules["object_detection.builders"] = mocked_builders
sys.modules["object_detection.core"] = mocked_core
sys.modules["object_detection.protos"] = mocked_protos

import model_main_tf2_mod
import train_eval
from train_eval_utils import file_exist, delete_blob



class TrainTfrecord:
    uri = "gs://dummy_uri/ur"

class ValTfrecord:
    uri = "gs://dummy_uri/urssss"

class ValMetrics:
    def log_metric(self, dummy1, dummy2):
        pass

class BestCheckpoint:
    metadata = {"best_ckpt":""}

class Blob:
    def exists(self, dummy):
        dummy = True
        return dummy

    def delete(self):
        return True

class DummyBucket:
    def blob(self, dummy):
        dummy = Blob()
        return dummy


class TestTrain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config_path = f"{current_dir}/test_data/sample.config"
        cls.train_tf_rec_path = f"{current_dir}/test_data/train.record"
        cls.test_tf_rec_path = f"{current_dir}/test_data/validation.record"
        cls.label_map_path = f"{current_dir}/test_data/label_map.pbtxt"
        cls.out_path = f"{current_dir}/pipeline_out"
        cls.metric_csv_file = f"{current_dir}/test_data/metric.csv"
        cls.model_out_dir = f"{current_dir}/model_out"
        cls.num_classes = 4
        cls.finetune_checkpoint = "dummy fine tune point"
        cls.number_of_steps = 25000
        cls.train_tfrecord = TrainTfrecord()
        cls.val_tfrecord = ValTfrecord()
        cls.val_metrics = ValMetrics()
        cls.best_checkpoint = BestCheckpoint()

    def test_get_best_step(self):
        delta_map = 0.5
        best_step, best_loss, best_map = model_main_tf2_mod.get_best_step(
            self.metric_csv_file, delta_map)
        self.assertEqual((1000.0, 0.1, 0.5), (best_step, best_loss, best_map))

    @patch("train_eval.file_exist")
    @patch("train_eval.model_main")
    @patch("train_eval.delete_blob")
    def test_train_and_eval(
        self, mock_delete, mock_model_main, mock_file_exist):
        mock_file_exist.return_value = True
        mock_model_main.train_and_eval.return_value = (
            "ckpt-3", 2000, 0.2, 0.6)
        train_eval.train_and_eval(
            self.config_path, self.label_map_path, self.model_out_dir,
            self.train_tfrecord, self.val_tfrecord, self.val_metrics,
            self.best_checkpoint)
        mock_delete.return_value = True

    @patch("train_eval.file_exist")
    @patch("train_eval.model_main")
    @patch("train_eval.delete_blob")
    def test_train_and_eval_failure(
        self, mock_delete, mock_model_main, mock_file_exist):
        try:
            mock_file_exist.return_value = False
            mock_model_main.train_and_eval.return_value = (
                "ckpt-3", 2000, 0.2, 0.6)
            train_eval.train_and_eval(
                self.config_path, self.label_map_path, self.model_out_dir,
                self.train_tfrecord, self.val_tfrecord, self.val_metrics,
                self.best_checkpoint)
            mock_delete.return_value = True
        except Exception as e:
            self.assertEqual(str(e), "tf record path doesn't exist")

    @patch("train_eval_utils.storage")
    def test_delete_blob(self, mock_storage):
        mock_storage.Client().bucket.return_value = DummyBucket()
        # mock_storage.Blob.return_value = Blob()
        delete_blob("dummy","dummy")

    @patch("train_eval_utils.storage")
    def test_file_exist(self, mock_storage):
        mock_storage.Client().bucket.return_value = "dummy_bucket"
        mock_storage.Blob.return_value = Blob()
        file_exist("gs://bucket/file")
