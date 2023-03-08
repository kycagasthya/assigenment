# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

"""Testing DocSplitting and download, upload files with
extention validation"""

import unittest
import json
from unittest.mock import patch
from docai.processor.v1.utils import helpers as documentai_helper
from docai.processor.v1.utils import post_processing
from google.cloud import documentai_v1 as documentai


class VarPath:
    """ Used for defining path of test files """
    def __init__(self) -> None:
        self.path = "./tests/unit/src/docai-processor/test_data/"
        self.sample_png = f"{self.path}sample.png"
        self.json_path_cdc = f"{self.path}sample_cdc_output.json"
        self.json_path_cde = f"{self.path}sample_cde_output.json"
        self.sample_json = f"{self.path}sample_output.json"

class TestDocSplit(unittest.TestCase,
    VarPath
    ):
    """ Testing Helper, Splitter """

    def __init__(self, *args, **kwargs) -> None:
        """ testing Helper class methods """
        super().__init__(*args, **kwargs)
        VarPath.__init__(self)
        self.project_id = "ibank-development"
        self.location = "us"
        self.request_id = ""
        self.page_id = ""
        self.map_endpoint = {
            "aadhaar_card": "92f81d5b03c2e2bb",
            "pan_card": "12c6c01f2fb2d7f6",
            "passport": "c7a11222875a7973",
            "driving_license": "41acda8c9dd97ff7",
            "voter_card": "958c5e49b53cc3d0",
            "classification": "5fe6a19795a0d87b"
        }


    @staticmethod
    def read_file(path: str) -> bytes:
        """reading file from config with key_name"""
        with open(path, "rb") as f:
            file_bytes = f.read()
        f.close()
        return file_bytes


    @patch("docai.processor.v1.utils.helpers.documentai.DocumentProcessorServiceClient.process_document") #pylint: disable=line-too-long
    def test_cde_success(self, mock_cde_response) -> None:
        """testing DOC AI Parser"""
        with open(self.json_path_cdc, "r") as fp:
            sample_json = json.load(fp)
        pred = "driving_license"
        document = sample_json["document"]

        with open(self.json_path_cde, "r") as fp:
            sample_json = json.load(fp)
        out_document = documentai.types.document_processor_service.ProcessResponse.from_json(json.dumps(sample_json)) #pylint: disable=line-too-long
        mock_cde_response().return_value = out_document

        cde_obj = documentai_helper.OnlinePred(
            project=self.project_id,
            endpoint_id=self.map_endpoint[pred],
            location=self.location,
            request_id=self.request_id,
            page_id=self.project_id)

        pred = cde_obj.predict_cde(document, doc_type=pred)
        self.assertEqual(list, type(pred))


    @patch("docai.processor.v1.utils.helpers.OnlinePred.predict")
    def test_cdc_success(self, mock_cdc_response) -> None:
        """testing DOC AI Classifier"""

        with open(self.json_path_cdc, "r") as fp:
            sample_json = json.load(fp)
        out_document = documentai.types.document_processor_service.ProcessResponse.from_json(json.dumps(sample_json)) #pylint: disable=line-too-long

        cdc_obj = documentai_helper.OnlinePred(
            project=self.project_id,
            endpoint_id=self.map_endpoint["classification"],
            location=self.location,
            request_id=self.request_id,
            page_id=self.project_id)
        mock_cdc_response.return_value = out_document.document.entities, out_document #pylint: disable=line-too-long

        pred, conf, _ = cdc_obj.predict_cdc(
            self.read_file(self.sample_png))
        self.assertEqual(pred, "driving_license")
        self.assertEqual(round(conf), 1)

    @patch("docai.processor.v1.utils.helpers.OnlinePred.predict")
    def test_predict(self, mock_cdc_response) -> None:
        """testing DOC AI Classifier"""

        with open(self.json_path_cdc, "r") as fp:
            sample_json = json.load(fp)
        out_document = documentai.types.document_processor_service.ProcessResponse.from_json(json.dumps(sample_json)) #pylint: disable=line-too-long

        cdc_obj = documentai_helper.OnlinePred(
            project=self.project_id,
            endpoint_id=self.map_endpoint["classification"],
            location=self.location,
            request_id=self.request_id,
            page_id=self.project_id)
        mock_cdc_response.return_value = out_document.document.entities, out_document #pylint: disable=line-too-long
        pred, _ = cdc_obj.predict(
            self.read_file(self.sample_png))

        self.assertEqual(pred[0].type_, "aadhaar_card")


    def test_postprocessing(self) -> None:
        """testing DOC AI Parser"""
        with open(self.sample_json, "r") as fp:
            sample_json = json.load(fp)

        post_process_obj = post_processing.PostProcessing()
        output_list = post_process_obj.post_process_entities(
            doc_type="aadhaar_card", cde_response=sample_json
        )

        post_process_obj = post_processing.PostProcessing()
        output_list = post_process_obj.post_process_entities(
            doc_type="passport", cde_response=sample_json
        )

        post_process_obj = post_processing.PostProcessing()
        output_list = post_process_obj.post_process_entities(
            doc_type="driving_license", cde_response=sample_json
        )

        post_process_obj = post_processing.PostProcessing()
        output_list = post_process_obj.post_process_entities(
            doc_type="voter_card", cde_response=sample_json
        )
        self.assertEqual(list, type(output_list))

    @patch("docai.processor.v1.utils.helpers.OnlinePred.mlops_predict_cde")
    def test_mlops_cde(self, mock_cde_response) -> None:
        """testing DOC AI Classifier"""

        with open(self.sample_json, "r") as fp:
            sample_json = json.load(fp)

        cde_obj = documentai_helper.OnlinePred(
            project=self.project_id,
            endpoint_id=self.map_endpoint["passport"],
            location=self.location,
            request_id=self.request_id,
            page_id=self.project_id)
        mock_cde_response.return_value = sample_json
        output_list = cde_obj.mlops_predict_cde(
            self.read_file(self.sample_png))
        self.assertEqual(list, type(output_list))
