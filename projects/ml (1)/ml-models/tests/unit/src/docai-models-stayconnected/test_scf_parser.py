# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

import unittest
from os.path import dirname, abspath
import json
from docai.models.stay_connected_v3.scf_parser import SignatureParser
from docai.models.stay_connected_v3.helper import SignParserHelper
from docai.models.stay_connected_v3.prediction import Predict
from cdc_op import (
    request_id,
    page_id,
    project,
    endpoint_id,
    scf_location,
    threshold,
)
import gcsfs
from qdocai.logger import QDocLogger


class TestScfParser(unittest.TestCase):
    def setUp(self):
        self.threshold = threshold
        self.endpoint_id = endpoint_id
        self.project = project
        self.request_id = request_id
        self.page_id = page_id
        self.location = scf_location
        self.hlp = SignParserHelper(request_id, page_id, project)
        self.pred = Predict(
            request_id, page_id, project, endpoint_id, scf_location, threshold
        )
        self.logger = QDocLogger()
        self.scfparserobj = SignatureParser(
            request_id, page_id, project, endpoint_id, scf_location, threshold
        )
        self.scfprediction = Predict(
            request_id, page_id, project, endpoint_id, scf_location, threshold
        )

        fs = gcsfs.GCSFileSystem()
        bk_name = "ibank-development-transfer-bucket"
        s_path = "ML/Data/data-buckets/for_parser_q/scf_updated/SCF/"
        p_path = "dummy_test_scf/augmented"
        file_3 = f"gs://{bk_name}/{s_path}{p_path}/new_updated_from.jpg"
        with fs.open(file_3, "rb") as fp:
            self.img_bytes = fp.read()
        current_dir = abspath(dirname(__file__))
        with open(f"{current_dir}/test_data/json_response.json") as f:
            self.cdcop = json.load(f)

    # scf_parser
    def test_extract(self):
        self.assertEqual(
            self.scfparserobj.extract(
                file_bytes=self.img_bytes, cdc_ocr=self.cdcop),
            (True, False, False),
        )

    def test_key_word_extraction_of_applicants(self):

        self.assertEqual(
            self.scfparserobj.key_word_extraction_of_applicants(
                all_response=self.hlp.cdc_ocr_wrap(raw_ocr=self.cdcop)
            ),
            ("Primary", "Applicant", "Holder", "Joint"),
        )

    def test_key_word_extraction(self):
        self.assertEqual(
            self.scfparserobj.key_word_extraction(
                all_response=self.hlp.cdc_ocr_wrap(raw_ocr=self.cdcop)
            ),
            ("CUSTOMER", "DECLARATION", "BRANCH", "ONLY"),
        )


    # prediction
    def test_prediction(self):
        self.assertEqual(
            len(self.scfprediction.prediction(file_content=self.img_bytes)), 2
        )

    # helper
    def test_cdc_ocr_cleaning(self):
        self.assertEqual(len(self.hlp.cdc_ocr_cleaning(document=self.cdcop)), 2)

    def test_cdc_ocr_wrap(self):
        self.assertEqual(len(self.hlp.cdc_ocr_wrap(raw_ocr=self.cdcop)), 507)


    def test_extract_word_coordinates(self):
        self.assertEqual(
            self.hlp.extract_word_coordinates(
                all_response=self.hlp.cdc_ocr_wrap(raw_ocr=self.cdcop),
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
                    all_response=self.hlp.cdc_ocr_wrap(raw_ocr=self.cdcop),
                    customer_fuzz="CUSTOMER",
                    declaration_fuzz="DECLARATION",
                    branch_fuzz="BRANCH",
                    only_fuzz="ONLY",
                )
            ),
            2,
        )

    def test_extract_combined_word_roi_coordinates(self):
        # for customer declaration
        self.assertEqual(
            self.hlp.extract_combined_word_roi_coordinates(
                combine_list=[
                    {"x": 500, "y": 1074},
                    {"x": 609, "y": 1075},
                    {"x": 609, "y": 1110},
                    {"x": 500, "y": 1109},
                    {"x": 619, "y": 1074},
                    {"x": 760, "y": 1075},
                    {"x": 760, "y": 1110},
                    {"x": 619, "y": 1109},
                ]
            ),
            ((500, 1074), (760, 1110)),
        )

    def test_mid_point_bb(self):
        self.assertEqual(
            self.hlp.mid_point_bb(
                signature_start=(500, 1074), signature_end=(760, 1110)
            ),
            (630, 1092),
        )
