# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
"""testing cdc training pipeline"""
from unittest import mock
from datetime import datetime
import sys
import unittest
sys.path.insert(0, "src/mlops_composer/invoke_training")

class Dummy:
    """
    class for moking
    """
    def __init__(self, val):
        """
        getting value
        """
        self.val = val

    def get(self, key, default_var=""):
        """
        getting  key and default var "
        """
        return self.val.get(key, default_var)


class TestCdcPipeline(unittest.TestCase):
    """
    testing cdc pipeline
    """
    def test_train(self):
        """
        testing train cdc
        """
        mocked_airflow = mock.MagicMock()
        sys.modules["airflow.models"] = mocked_airflow
        mocked_airflow.Variable.get.return_value = "dev"

        mocked_aiplatform = mock.MagicMock()
        sys.modules["google.cloud.aiplatform"] = mocked_aiplatform
        mocked_aiplatform.PipelineJob.submit.return_value = "submited"
        from cdc_training_pipeline_runner import train
        self.assertEqual(
            train(
                config_dict={
"processor_id": "4fd83649b68e0f12",
"gcs_uri": "gs://ibank-development-transfer-bucket/ML/evaluation/ \
                    cdc/20220412133453/eval_df.csv",
"version" : "latest",
"timestamp_dag":datetime.now().strftime("%Y%m%d%H%M%S")
}
            ),
            None
        )
