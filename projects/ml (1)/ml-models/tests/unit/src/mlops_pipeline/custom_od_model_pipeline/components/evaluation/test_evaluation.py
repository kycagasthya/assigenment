# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# =============================================================================
import unittest
from unittest import mock
import json
from unittest.mock import patch
import sys
import constants_test as c
sys.path.insert(
    0, "src/mlops_pipeline/custom_od_model_pipeline/components/evaluation/src")
mocked_prediction = mock.MagicMock()
sys.modules["prediction_bytes_array"] = mocked_prediction
import evaluation
from scf_parser import SignatureParser
from helper import SignParserHelper

class Blob:
    name = "dummy.jpg"


class SavedModel:
    path = "dummy path"


class Overall:
    def log_metric(self, dummy_2, dummy_3):
        pass


class Classwise:
    def log_metric(self, dummy_2, dummy_3):
        pass

class SignatureParserDummy:
    def extract(self, fl_bytes, cdc_json):
        fl_bytes = cdc_json
        fl_bytes = (True, False, False, 0.6, 0.7, 0.8)
        return fl_bytes


class TestEvaluation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.metric_calc_actual = c.metric_calc_actual
        cls.metric_calc_pred = c.metric_calc_pred
        cls.metric_cal_result = c.metric_cal_result
        cls.bucket_name = c.bucket_name
        cls.prefix = c.prefix
        cls.gs_path = c.gs_path
        cls.file_list = c.file_list
        cls.saved_model = SavedModel()
        cls.threshold = 0.3
        cls.test_data_path = c.test_data_path
        cls.dummy_filepaths = c.dummy_filepaths
        cls.out_csv_path = c.out_csv_path
        cls.overall = Overall()
        cls.classwise = Classwise()
        cls.hlp = SignParserHelper()
        # cls.scf_object = SignatureParser(c.model_path, 0.2)
        cls.cdc_json_path = c.cdc_json_path
        cls.key_words_actual = c.key_words_actual
        with open(cls.cdc_json_path, "r") as fp:
            cls.cdc_json = json.load(fp)
        cls.img_path_scf = c.img_path_scf
        with open(cls.img_path_scf, "rb") as f:
            cls.img_bytes = f.read()
        cls.all_response = cls.hlp.cdc_ocr_wrap(cls.cdc_json)
        cls.applicants_key_actual = c.applicants_key_actual
        cls.bounding_box_dict = c.bounding_box_dict

    def test_metric_calculation(self):
        metric_pred = evaluation.metric_calculation(self.metric_calc_actual,
                                                    self.metric_calc_pred)
        self.assertEqual(metric_pred, self.metric_cal_result)

    @patch("evaluation.storage.Client")
    def test_list_blobs(self, mock_storage_client):
        mock_storage_client().list_blobs.return_value = [Blob(), Blob()]
        files = evaluation.list_blobs(self.bucket_name, self.prefix)
        self.assertEqual(files, self.file_list)

    @patch("evaluation.storage.Client")
    def test_filepath_extraction(self, mock_storage_client):
        mock_storage_client().list_blobs.return_value = [Blob(), Blob()]
        files = evaluation.filepath_extraction(self.gs_path)
        self.assertEqual(files, self.file_list)

    @patch("evaluation.SignatureParser")
    @patch("evaluation.filepath_extraction")
    @patch("evaluation.gcsfs.GCSFileSystem")
    @patch("evaluation.json.load")
    def test_start_evaluation(
            self, mock_json, mock_gcs_filesystem, mock_filepath_extraction,
            mock_signature_parser):
        mock_signature_parser.return_value = SignatureParserDummy()
        mock_filepath_extraction.return_value = self.dummy_filepaths
        mock_gcs_filesystem().open.return_value = open(c.img_path_scf, "rb")
        mock_json.return_value = json.dumps({"dummy": "dummy"})
        evaluation.start_evaluation(self.saved_model, self.threshold,
                                    self.test_data_path,
                                    self.out_csv_path, self.overall,
                                    self.classwise)

    def test_key_word_extraction(self):
        key_words = SignatureParser.key_word_extraction(
            self, all_response=self.all_response)
        self.assertEqual(
            key_words, self.key_words_actual)

    def test_key_word_extraction_of_applicants(self):
        applicants_key = SignatureParser.key_word_extraction_of_applicants(
            self, all_response=self.all_response)
        self.assertEqual(
            applicants_key, self.applicants_key_actual)

    @patch("scf_parser.Prediction")
    def test_extract(self, mock_predict):
        # mocked_prediction = mock.MagicMock()
        # sys.modules["prediction_bytes_array"] = mocked_prediction
        scf_object = SignatureParser(c.model_path, 0.2)
        with open(c.img_path_scf,
                  "rb") as f:
            img_byte = f.read()
        mock_predict().test_model_bytes.return_value = self.bounding_box_dict
        mock_predict().preprocess.return_value = "dummy"
        mock_predict().encode_image.return_value = "dummy"
        result = scf_object.extract(img_byte, self.cdc_json)
        self.assertEqual(result, c.extract_result)

    # helper
    def test_cdc_ocr_cleaning(self):
        self.assertEqual(
            len(self.hlp.cdc_ocr_cleaning(document=self.cdc_json)),2)

    def test_cdc_ocr_wrap(self):
        self.assertEqual(
            len(self.hlp.cdc_ocr_wrap(raw_ocr=self.cdc_json)), 497)

    def test_resize_image(self):
        self.assertEqual(
            self.hlp.resize_image(im_bytes=self.img_bytes), "resize_temp.jpg")

    def test_extract_word_coordinates(self):
        self.assertEqual(
            self.hlp.extract_word_coordinates(
                all_response=self.all_response,
                primary_fuzz="Primary",
                applicant_fuzz="Applicant",
                joint_fuzz="Joint",
                holder_fuzz="Holder",
            ),
            (None, None, None),
        )

    def test_extract_word_roi_coordinates(self):
        self.assertEqual(
            len(
                self.hlp.extract_word_roi_coordinates(
                    all_response=self.all_response,
                    customer_fuzz="CUSTOMER",
                    declaration_fuzz="DECLARATION",
                    branch_fuzz="BRANCH",
                    only_fuzz="ONLY",
                )
            ),
            2,
        )

    def test_extract_combined_word_roi_coordinates(self):
        roi_coordinates = self.hlp.extract_combined_word_roi_coordinates(
            combine_list=c.combine_list)
        self.assertEqual(roi_coordinates, c.roi_coordinates_actual)

    def test_mid_point_bb(self):
        self.assertEqual(
            self.hlp.mid_point_bb(
                signature_start=(500, 1074), signature_end=(760, 1110)
            ),
            (630, 1092),
        )
