# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
"""unittest cutom od training"""
from unittest import mock
from datetime import datetime
import sys
import unittest
sys.path.insert(0, "src/mlops_composer/invoke_training")


class Dummy:
    """class for moking"""
    def __init__(self, val):
        """getting val"""
        self.val = val

    def get(self, key, default_var=""):
        """
        getting val and default var
        """
        return self.val.get(key, default_var)

    def dummy(self):
        """dummy"""
        return True


class TestCustomPipeline(unittest.TestCase):
    """unitest for custom od"""
    def test_train(self):
        """
        test for custom od train
        """
        mocked_airflow = mock.MagicMock()
        sys.modules["airflow.models"] = mocked_airflow
        mocked_airflow.Variable.get.return_value = "dev"

        mocked_aiplatform = mock.MagicMock()
        sys.modules["google.cloud.aiplatform"] = mocked_aiplatform
        mocked_aiplatform.PipelineJob.submit.return_value = "submited"
        from custom_training_pipeline_runner import train
        self.assertEqual(
            train(
                config_dict= {"train_path":"gs:// \
                              asia-south1-docai-mlops-com-4dda2ed4-bucket/ \
                              od-mlops/preprocess_data/scf_data/train",
"validation_path":"gs://asia-south1-docai-mlops-com-4dda2ed4-bucket/ \
                              od-mlops/preprocess_data/scf_data/test",
"label_path":"gs://asia-south1-docai-mlops-com-4dda2ed4-bucket/ \
                              od-mlops/preprocess_data/label_map_class.pbtxt",
"pipeline_config_path":"gs://ibank-development-transfer-bucket/ \
                              ML/Data/data-buckets/ \
                              for_parser_q/mohsin/training/configs/ \
                              ssd_mobilenet_v1_fpn_640x640_ \
                              coco17_tpu-8-test_mk6.config",
"timestamp_dag":datetime.now().strftime("%Y%m%d%H%M%S")
}
            ),
            None
       )
