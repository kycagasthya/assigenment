# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# =============================================================================
import sys
import os
import unittest
from unittest.mock  import patch
from google.cloud import storage
from unittest import mock
from os.path import dirname, abspath
sys.path.insert(
    0,
    "src/mlops_pipeline/custom_od_model_pipeline/components/export_model/src")
mocked_tf_v2 = mock.MagicMock()
mocked_object_detection = mock.MagicMock()
mocked_protos = mock.MagicMock()
sys.modules["tensorflow"] = mocked_tf_v2
sys.modules["tensorflow.compat.v2"] = mocked_tf_v2
sys.modules["object_detection"] = mocked_object_detection
sys.modules["object_detection.protos"] = mocked_protos
import export_model
client = storage.Client()
current_dir = abspath(dirname(__file__))

class Checkpoint:
    metadata = {"best_ckpt": "ckpt-1"}

class DeployableModel:
    path = ""

class Blob:
    def exists(self, dummy):
        dummy=True
        return dummy

    def write(self, dummy=True):
        dummy=True
        return dummy

class TestExportModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.output_directory = f"{current_dir}/test_data"
        cls.saved_model = f"{current_dir}/test_data/saved_model"
        cls.target_path = f"{current_dir}/test_data/bytes_model"
        cls.input_size = (640, 640)
        cls.checkpoint = Checkpoint()
        cls.deployable_model = DeployableModel()
        cls.ckpt_path = f"{current_dir}/test_data/sample_checkpoint.txt"


    def test_convert_model_input(self):
        export_model.convert_model_input(
            self.saved_model, self.target_path, self.input_size)
        model = os.path.join(self.target_path, "saved_model.pb")
        conversion_status = os.path.isfile(model)
        self.assertEqual(conversion_status, True)
    @patch("export_model.storage")
    @patch("export_model.exporter_lib_v2.export_inference_graph")
    @patch("export_model.convert_model_input")
    @patch("export_model.gcsfs.GCSFileSystem")
    @patch("export_model.text_format")
    def test_export_model(
            self, mock_text_format, dummy_gcs_filesystem, mock_convert_model,
            mock_exporter, mock_storage):
        mocked_tf_v2.io.gfile.GFile = True
        mock_text_format.Merge.return_value = True
        mock_storage.Client().bucket.return_value = True
        mock_storage.Blob.return_value = Blob()
        mock_exporter.return_value = True
        mock_convert_model.return_value = True
        ckpt_file = open(self.ckpt_path, "w")
        dummy_gcs_filesystem().open.return_value = ckpt_file
        export_model.export_model(
            self.output_directory, str(self.input_size),
            self.checkpoint, self.deployable_model)
        ckpt_file.close()
