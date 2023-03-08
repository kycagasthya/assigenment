# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
"""unittest  cde pipeline"""
from unittest import mock
from datetime import datetime
import sys
import unittest
sys.path.insert(0, "src/mlops_composer/invoke_training")


class Dummy:
    """Class for moking"""
    def __init__(self, val):
        """getting val"""
        self.val = val

    def get(self, key, default_var=""):
        """
        getting key and default var
        """
        return self.val.get(key, default_var)

class TestCdePipeline(unittest.TestCase):
    """unittets for cde pipeline"""
    def test_train(self):
        """cde training"""
        mocked_airflow = mock.MagicMock()
        sys.modules["airflow.models"] = mocked_airflow
        mocked_airflow.Variable.get.return_value = "dev"

        mocked_aiplatform = mock.MagicMock()
        sys.modules["google.cloud.aiplatform"] = mocked_aiplatform
        mocked_aiplatform.PipelineJob.submit.return_value = "submited"
        from cde_training_pipeline_runner import train

        self.assertEqual(
            train(
                config_dict= {
"version": "latest",
"doc_type":"cde_pan",
"parser_keys": ["name","fathers_name", "dob","pan_id", "gcs_uri"],
"processor_id": "60b530fb3aa7e18",
"ground_truth_csv": "gs://ibank-development-transfer-bucket/ML/ \
                    Data/data-buckets/for_parser_q/for_eval/ground_truth.csv",
"timestamp_dag":datetime.now().strftime("%Y%m%d%H%M%S")
}
            ),
            None
        )
