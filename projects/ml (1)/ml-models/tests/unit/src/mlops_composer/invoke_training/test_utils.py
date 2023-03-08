# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

"""unittest Utils"""
from utils import list_files, \
                retrieve_spec_file, \
                check_params_exist, \
                remove_params, \
                check_update_timestamp
from unittest.mock import patch
import sys
import unittest
sys.path.insert(0, "src/mlops_composer/invoke_training")


class Elements:
    """check"""
    name = "ajinkya"

class Blob:
    """mocking """
    def list_blobs(self,prefix):
        """blob mocking"""
        prefix = [Elements(),Elements(),Elements()]
        return prefix

    def upload_from_filename(self,file_name):
        """upload from file mock"""
        file_name = True
        return file_name

class Bucket:
    """blob mocking"""
    def blob(self,dummy_para):
        """blob"""
        dummy_para = Blob()
        return dummy_para



class TestUtils(unittest.TestCase):
    """Utils testing"""
    @patch("utils.storage.Client")
    def test_list_files(self, mock_storageclient):
        """list files"""
        mock_storageclient().get_bucket.return_value= Blob()
        self.assertEqual(
            list_files(
                bucket_name="dummy",
                bucket_folder="jibin"
            ),
            ["gs://dummy/ajinkya","gs://dummy/ajinkya","gs://dummy/ajinkya"]
        )

    @patch("utils.list_files")
    def test_retrieve_spec_file(self,test_retrive):
        """retrive spec file"""
        test_retrive.return_value = ["dummy_retrive.json"]

        self.assertEqual(
            retrieve_spec_file(
                bucket_path= "gs://training_data/ml_model/data",
                file_version= "latest"
            ),
            "dummy_retrive.json"
        )

    def test_check_params_exist(self):
        """check paramters exist"""
        self.assertEqual(
            check_params_exist(
                params_dict={"train_path":"dummy_train_path",
                             "val_path":"dummy_cal_path"},
                params_list= ["train_path"]
            ),
            None
        )

    def test_remove_params(self):
        """remove paramters"""
        self.assertEqual(
            remove_params(
                params_dict={"train_path":"dummy_train_path",
                             "val_path":"dummy_cal_path"},
                params_to_remove=["train_path"]
            ),
            {"val_path": "dummy_cal_path"}
        )

    def test_check_update_timestamp(self):
        """check update timestamp"""
        self.assertEqual(
            check_update_timestamp(
                config_dict= {"timestamp_dag":"20240520061000"},
                params_dict= {"timestamp_hr" : ""}
            ),
            {"timestamp_hr": "2024-05-20 06:10:00"}
        )

    # def test_update_params_timestamp(self):
    #     """update para timestamp"""
    #     self.assertEqual(
    #         update_params_timestamp(
    #             params_dict={"job_id":"dummy_id","data_pipeline_root":"",
    #                          "pipeline_root":"dummy_pipelineroot"},
    #             params_list={"job_id":"dummy_id","data_pipeline_root":""},
    #             timestamp="20240520061000"
    #         ),
    #         {"job_id": "dummy_id-20240520061000",
    #          "data_pipeline_root": "dummy_pipelineroot/ \
    #          data_pipeline_root/20240520061000",
    #          "pipeline_root": "dummy_pipelineroot"}
    #     )
 