# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

import os
import numpy as np
import cv2
from typing import List, Tuple, Dict
from numpy import ndarray
import sys
from qdocai.logger import QDocLogger
from qdocai.utils import DocAIBase, DocAIException
from docai.models.stay_connected_v3 import error_code
from .helper import SignParserHelper
from .prediction import Predict


class SignatureParser(DocAIBase):
    def __init__(
        self,
        request_id: str,
        page_id: str,
        project: str,
        endpoint_id: str,
        location: str,
        threshold: float,
    ):
        self.request_id = request_id
        self.page_id = page_id
        self.hlp = SignParserHelper(request_id, page_id, project)
        self.pred = Predict(
            request_id, page_id, project, endpoint_id, location, threshold
        )
        self.logger = QDocLogger()
        self.error_dict = error_code.Errors.error_codes
        super().__init__(request_id, page_id)

    def key_word_extraction(
        self, all_response: List
    ) -> Tuple[str, str, str, str]:
        """
        extraction of words with fuzzy match
        Args:
            all_response: response of ocr
        Returns:
            customer_fuzz: fuzzy match for customer
            declaration_fuzz: fuzzy match for declaration
            branch_fuzz: fuzzy match for branch
            only_fuzz: fuzzy match for only
        """
        try:
            li_customer = []
            li_declaration = []
            li_branch = []
            li_only = []
            for x in all_response:
                customer = self.hlp.fuzzy_match(
                    ["CUSTOMER"],
                    x["description"],
                    ngram_range=(1, 2),
                    lower_flag=False,
                )
                declaration = self.hlp.fuzzy_match(
                    ["DECLARATION)"],
                    x["description"],
                    ngram_range=(1, 2),
                    lower_flag=False,
                )
                branch = self.hlp.fuzzy_match(
                    ["BRANCH"],
                    x["description"],
                    ngram_range=(1, 1),
                    lower_flag=False,
                )
                only = self.hlp.fuzzy_match(
                    ["ONLY"],
                    x["description"],
                    ngram_range=(1, 1),
                    lower_flag=False,
                )
                if customer != (None, None):
                    li_customer.append(customer)
                if declaration != (None, None):
                    li_declaration.append(declaration)
                if branch != (None, None):
                    li_branch.append(branch)
                if only != (None, None):
                    li_only.append(only)
            if len(li_customer) >= 1:
                customer_fuzz = li_customer[0][0]
            else:
                customer_fuzz = None
            if len(li_declaration) >= 1:
                declaration_fuzz = li_declaration[0][0]
            else:
                declaration_fuzz = None
            if len(li_branch) >= 1:
                branch_fuzz = li_branch[0][0]
            else:
                branch_fuzz = None
            if len(li_only) >= 1:
                only_fuzz = li_only[0][0]
            else:
                only_fuzz = None
            self.logger.ml_logger(
                level="INFO",
                ml_package="docai-models-stayconnected",
                message=f"keyword extraction for ROI: \
            {customer_fuzz}, {declaration_fuzz}, {branch_fuzz}, {only_fuzz}",
                request_id=self.request_id,
                page_id=self.page_id,
            )
            return customer_fuzz, declaration_fuzz, branch_fuzz, only_fuzz
        except Exception as error:
            self.logger.ml_logger(
                level="ERROR",
                ml_package="docai-models-stayconnected",
                action=f"key word is not extracted for ROI: CustomerFuzz-\
                {customer_fuzz},{declaration_fuzz},{branch_fuzz},{only_fuzz}",
                status_code=self.error_dict[
                    "ERROR_KEYWORD_EXTRACTION_ROI_FAILED"
                ]["code"],
                request_id=self.request_id,
                page_id=self.page_id,
            )
            raise DocAIException(
                action="key word extraction",
                message=self.error_dict["ERROR_KEYWORD_EXTRACTION_ROI_FAILED"][
                    "text_desc"
                ],
                status_desc=self.error_dict[
                    "ERROR_KEYWORD_EXTRACTION_ROI_FAILED"
                ]["desc"],
                status_code=self.error_dict[
                    "ERROR_KEYWORD_EXTRACTION_ROI_FAILED"
                ]["code"],
            ) from error

    def key_word_extraction_of_applicants(
        self, all_response: List
    ) -> Tuple[str, str, str, str]:
        """
        extraction of words with fuzzy match
        Args:
            all_response: response of ocr
        Returns:
            primary_fuzz: fuzzy match for primary
            applicant_fuzz: fuzzy match for applicant
            holder_fuzz: fuzzy match for holder
            joint_fuzz: fuzzy match for joint
        """
        try:
            li_primary = []
            li_applicant = []
            li_joint = []
            li_holder = []
            for x in all_response:
                primary = self.hlp.fuzzy_match(
                    ["(Primary"], x["description"], ngram_range=(1, 3)
                )
                applicant = self.hlp.fuzzy_match(
                    ["Applicant)"], x["description"], ngram_range=(1, 3)
                )
                joint = self.hlp.fuzzy_match(
                    ["(joint"], x["description"], ngram_range=(1, 3)
                )
                holder = self.hlp.fuzzy_match(
                    ["Holder"], x["description"], ngram_range=(1, 3)
                )
                if primary[1] == "(Primary":
                    li_primary.append(primary)
                if applicant[1] == "Applicant)":
                    li_applicant.append(applicant)
                if joint[1] == "(joint":
                    li_joint.append(joint)
                if holder[1] == "Holder":
                    li_holder.append(holder)
            if len(li_primary) >= 1:
                primary_fuzz = li_primary[0][0]
            else:
                primary_fuzz = None
            if len(li_applicant) >= 1:
                applicant_fuzz = li_applicant[0][0]
            else:
                applicant_fuzz = None
            if len(li_joint) >= 1:
                joint_fuzz = li_joint[0][0]
            else:
                joint_fuzz = None
            if len(li_holder) >= 1:
                holder_fuzz = li_holder[0][0]
            else:
                holder_fuzz = None
            self.logger.ml_logger(
                level="INFO",
                ml_package="docai-models-stayconnected",
                message=f"keyword extraction for static words: \
            {primary_fuzz}, {applicant_fuzz}, {holder_fuzz}, {joint_fuzz}",
                request_id=self.request_id,
                page_id=self.page_id,
            )
            return primary_fuzz, applicant_fuzz, holder_fuzz, joint_fuzz
        except Exception as error:
            self.logger.ml_logger(
                level="ERROR",
                ml_package="docai-models-stayconnected",
                action=f"key word extraction for static word :\
                {primary_fuzz}{applicant_fuzz}{holder_fuzz}{joint_fuzz}",
                status_code=self.error_dict[
                    "ERROR_KEYWORD_EXTRACTION_STATICWORD_FAILED"
                ]["code"],
                message=self.error_dict[
                    "ERROR_KEYWORD_EXTRACTION_STATICWORD_FAILED"
                ]["text_desc"],
                request_id=self.request_id,
                page_id=self.page_id,
            )
            raise DocAIException(
                action="key word extraction of applicants",
                message=self.error_dict[
                    "ERROR_KEYWORD_EXTRACTION_STATICWORD_FAILED"
                ]["text_desc"],
                status_desc=self.error_dict[
                    "ERROR_KEYWORD_EXTRACTION_STATICWORD_FAILED"
                ]["desc"],
                status_code=self.error_dict[
                    "ERROR_KEYWORD_EXTRACTION_STATICWORD_FAILED"
                ]["code"],
            ) from error

    def extract_count_of_signature(
        self,
        all_response: List,
        roi_shape_w: int,
        roi_shape_h: int,
        bounding_box_coordinate: List[List],
        comp_img: ndarray,
        pt_y_customer: int,
    ) -> Tuple[int, int, int]:
        """
        extracting the count of signature present on the form
        Args:
            all_response: response form ocr
            roi_shape_w: width of roi
            roi_shape_h: height of roi
            bounding_box_coordinate: co-ordinates of bounding box
            comp_img: compressed image
            pt_y_customer: y coordinate of customer key word
        Retruns:
             primary_holder_count: count of primary signature
             joint_holder1_count: count of holder 1
             joint_holder2_count: count of holder2
        """
        try:
            img_h, img_w, _ = comp_img.shape
            primary_holder_count = 0
            joint_holder1_count = 0
            joint_holder2_count = 0
            max_distance = 0.111
            (
                primary_fuzz,
                applicant_fuzz,
                holder_fuzz,
                joint_fuzz,
            ) = self.key_word_extraction_of_applicants(all_response)
            (
                primary_holder,
                holder_1,
                holder_2,
            ) = self.hlp.extract_word_coordinates(
                all_response,
                primary_fuzz,
                applicant_fuzz,
                joint_fuzz,
                holder_fuzz,
            )
            (
                start_point_p,
                end_point_p,
            ) = self.hlp.extract_combined_word_coordinates(
                combine_list=primary_holder
            )
            (
                start_point_jh1,
                end_point_jh1,
            ) = self.hlp.extract_combined_word_coordinates(
                combine_list=holder_1
            )
            (
                start_point_jh2,
                end_point_jh2,
            ) = self.hlp.extract_combined_word_coordinates(
                combine_list=holder_2
            )
            pt_x_primary, pt_y_primary = self.hlp.mid_point_bb(
                start_point_p, end_point_p
            )
            pt_x_holder1, pt_y_holder1 = self.hlp.mid_point_bb(
                start_point_jh1, end_point_jh1
            )
            pt_x_holder2, pt_y_holder2 = self.hlp.mid_point_bb(
                start_point_jh2, end_point_jh2
            )
            for count, _ in enumerate(bounding_box_coordinate):
                coordinate = bounding_box_coordinate[count]
                (
                    start_point_sign,
                    end_point_sign,
                ) = self.hlp.bounding_box_extract(coordinate, comp_img)
                pt_x_sign, pt_y_sign = self.hlp.mid_point_bb(
                    start_point_sign, end_point_sign
                )
                left_mid_x_sign, left_mid_y_sign = self.hlp.left_mid_point_bb(
                    start_point_sign, end_point_sign
                )
                if (pt_x_sign in range(0, roi_shape_w)) and (
                    pt_y_sign in range(pt_y_customer, roi_shape_h)
                ):
                    distance_primary = self.hlp.norm_distance(
                        pt_x_primary,
                        pt_y_primary,
                        pt_x_sign,
                        pt_y_sign,
                        img_h,
                        img_w,
                    )
                    distance_holder1 = self.hlp.norm_distance(
                        pt_x_holder1,
                        pt_y_holder1,
                        pt_x_sign,
                        pt_y_sign,
                        img_h,
                        img_w,
                    )
                    distance_holder2 = self.hlp.norm_distance(
                        pt_x_holder2,
                        pt_y_holder2,
                        pt_x_sign,
                        pt_y_sign,
                        img_h,
                        img_w,
                    )
                    left_mid_distance_primary = self.hlp.norm_distance(
                        pt_x_primary,
                        pt_y_primary,
                        left_mid_x_sign,
                        left_mid_y_sign,
                        img_w,
                        img_h,
                    )
                    left_mid_distance_holder1 = self.hlp.norm_distance(
                        pt_x_holder1,
                        pt_y_holder1,
                        left_mid_x_sign,
                        left_mid_y_sign,
                        img_w,
                        img_h,
                    )
                    left_mid_distance_holder2 = self.hlp.norm_distance(
                        pt_x_holder2,
                        pt_y_holder2,
                        left_mid_x_sign,
                        left_mid_y_sign,
                        img_w,
                        img_h,
                    )
                    if (
                        distance_primary is not None
                        and (
                            distance_primary <= max_distance
                            or left_mid_distance_primary <= max_distance
                        )
                        and pt_y_primary > pt_y_sign
                    ):
                        primary_holder_count += 1
                    else:
                        pass
                    if (
                        distance_holder1 is not None
                        and (
                            distance_holder1 <= max_distance
                            or left_mid_distance_holder1 <= max_distance
                        )
                        and pt_y_holder1 > pt_y_sign
                    ):
                        joint_holder1_count += 1
                    else:
                        pass
                    if (
                        distance_holder2 is not None
                        and (
                            distance_holder2 <= max_distance
                            or left_mid_distance_holder2 <= max_distance
                        )
                        and pt_y_holder2 > pt_y_sign
                    ):
                        joint_holder2_count += 1
                    else:
                        pass
            return (
                primary_holder_count,
                joint_holder1_count,
                joint_holder2_count,
            )
        except Exception as error:
            self.logger.ml_logger(
                level="ERROR",
                ml_package="docai-models-stayconnected",
                action="extraction of signature count failed",
                message=self.error_dict["ERROR_SIGNATURE_COUNT_FAILED"][
                    "text_desc"
                ],
                status_code=self.error_dict["ERROR_SIGNATURE_COUNT_FAILED"][
                    "code"
                ],
                request_id=self.request_id,
                page_id=self.page_id,
            )
            raise DocAIException(
                action="extract count of sign",
                message=self.error_dict["ERROR_SIGNATURE_COUNT_FAILED"][
                    "text_desc"
                ],
                status_desc=self.error_dict["ERROR_SIGNATURE_COUNT_FAILED"][
                    "desc"
                ],
                status_code=self.error_dict["ERROR_SIGNATURE_COUNT_FAILED"][
                    "code"
                ],
            ) from error

    def extract(self, file_bytes: bytes, cdc_ocr: Dict) -> Tuple[int, int, int]:
        """
        extract count of signatures from stay connected forms
        Args:
            file_bytes: Image file in bytes
            cdc_ocr: CDC ocr output
        Returns:
            primary_holder_count: count of Primary Holder signature
            joint_holder1_count: count of Holder 1 Signature
            joint_holder2_count: count of Holder 2 Signature
        Raise:
            Exception
        """
        self.logger.ml_logger(
            level="INFO",
            ml_package="docai-models-stayconnected",
            message="scf module started processing",
            request_id=self.request_id,
            page_id=self.page_id,
        )
        primary_holder_count = 0
        joint_holder1_count = 0
        joint_holder2_count = 0
        img_bytes = file_bytes
        resize_flag = False
        size_in_bytes = 1000000
        try:
            if sys.getsizeof(img_bytes) / size_in_bytes > 1:
                resize_flag = True
                resize_name = self.hlp.resize_image(file_bytes)
                with open(resize_name, "rb") as fp:
                    img_bytes = fp.read()
                    comp_img = np.frombuffer(img_bytes, np.uint8)
                    comp_img = cv2.imdecode(comp_img, cv2.IMREAD_COLOR)
                    img_h, img_w, _ = comp_img.shape
            if not resize_flag:
                comp_img = np.frombuffer(file_bytes, np.uint8)
                comp_img = cv2.imdecode(comp_img, cv2.IMREAD_COLOR)
                img_h, img_w, _ = comp_img.shape
            bounding_box_dict = self.pred.prediction(file_content=img_bytes)
            if (
                bounding_box_dict
                and "signature" in bounding_box_dict["displayNames"]
            ):
                all_response = self.hlp.cdc_ocr_wrap(cdc_ocr)
                (
                    customer_fuzz,
                    declaration_fuzz,
                    only_fuzz,
                    branch_fuzz,
                ) = self.key_word_extraction(all_response)
                (
                    customer_decl,
                    branch_only,
                ) = self.hlp.extract_word_roi_coordinates(
                    all_response,
                    customer_fuzz,
                    declaration_fuzz,
                    branch_fuzz,
                    only_fuzz,
                )
                (
                    start_point_cd,
                    end_point_cd,
                ) = self.hlp.extract_combined_word_roi_coordinates(
                    combine_list=customer_decl
                )
                (
                    start_point_bo,
                    end_point_bo,
                ) = self.hlp.extract_combined_word_roi_coordinates(
                    combine_list=branch_only
                )
                _, pt_y_customer = self.hlp.mid_point_bb(
                    start_point_cd, end_point_cd
                )
                _, pt_y_only = self.hlp.mid_point_bb(
                    start_point_bo, end_point_bo
                )
                if pt_y_customer is None:
                    pt_y_customer = img_h // 2
                if pt_y_only is None:
                    pt_y_only = img_h
                if pt_y_customer >= pt_y_only:
                    pt_y_customer = img_h // 2
                signature_codinates = []
                for ind, label in enumerate(bounding_box_dict["displayNames"]):
                    if label == "signature":
                        signature_codinates.append(
                            bounding_box_dict["bboxes"][ind]
                        )
                roi_shape_w = img_w
                roi_shape_h = pt_y_only
                (
                    primary_holder_count,
                    joint_holder1_count,
                    joint_holder2_count,
                ) = self.extract_count_of_signature(
                    all_response,
                    roi_shape_w,
                    roi_shape_h,
                    signature_codinates,
                    comp_img,
                    pt_y_customer,
                )
                if resize_flag:
                    os.remove(resize_name)
            self.logger.ml_logger(
                level="INFO",
                ml_package="docai-models-stayconnected",
                action="extract signs",
                status_code=200,
                message="scf module completed successfully",
                request_id=self.request_id,
                page_id=self.page_id,
            )
            primary_holder_count = min(primary_holder_count, 1)
            joint_holder1_count = min(joint_holder1_count, 1)
            joint_holder2_count = min(joint_holder2_count, 1)
            primary_holder_final = False
            joint_holder1_final = False
            joint_holder2_final = False
            if primary_holder_count > 0:
                primary_holder_final = True
            if joint_holder1_count > 0:
                joint_holder1_final = True
            if joint_holder2_count > 0:
                joint_holder2_final = True
            self.logger.ml_logger(
                level="INFO",
                ml_package="docai-models-stayconnected",
                action="Extraction Pass",
                status_code=200,
                message="SUCCESS",
                request_id=self.request_id,
                page_id=self.page_id,
            )
            return (
                primary_holder_final,
                joint_holder1_final,
                joint_holder2_final,
            )
        except Exception as error:
            self.logger.ml_logger(
                level="ERROR",
                ml_package="docai-models-stayconnected",
                action="Extraction failed",
                message=self.error_dict["ERROR_EXTRACTION_FAILED"]["text_desc"],
                status_code=self.error_dict["ERROR_EXTRACTION_FAILED"]["code"],
                request_id=self.request_id,
                page_id=self.page_id,
            )
            raise DocAIException(
                action="parse sign from scf sign",
                message=self.error_dict["ERROR_EXTRACTION_FAILED"]["text_desc"],
                status_desc=self.error_dict["ERROR_EXTRACTION_FAILED"]["desc"],
                status_code=self.error_dict["ERROR_EXTRACTION_FAILED"]["code"],
            ) from error
