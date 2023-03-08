# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# ==============================================================================
"""This module will detect primary, holder1 and holder2 signatures from stay
connected form"""

import os
import logging
import sys
import traceback
from typing import List, Tuple
import numpy as np
import cv2
from helper import SignParserHelper
from prediction_bytes_array import Prediction
from numpy import ndarray
from custlogger import ml_logger

logging.basicConfig(level=logging.INFO)


class SignatureParser():
    """
    class SignatureParser for extracting signatures

    Args:
            model_path: gcs path of model
            threshold: minimum threshold for detection
    """
    def __init__(self, model_path: str, threshold: float):
        """Inits SignatureParser with args"""
        self.hlp = SignParserHelper()
        self.pred = Prediction(model_path, threshold)

    def key_word_extraction(
            self, all_response: List) -> Tuple[str, str, str, str]:
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
            li_customer = []
            li_declaration = []
            li_branch = []
            li_only = []
            for word in all_response:
                customer = self.hlp.fuzzy_match(
                    ["CUSTOMER"], word["description"],
                    ngram_range=(1, 2), lower_flag=False)
                declaration = self.hlp.fuzzy_match(
                    ["DECLARATION)"], word["description"],
                    ngram_range=(1, 2), lower_flag=False)
                branch = self.hlp.fuzzy_match(
                    ["BRANCH"], word["description"],
                    ngram_range=(1, 1), lower_flag=False)
                only = self.hlp.fuzzy_match(
                    ["ONLY"], word["description"],
                    ngram_range=(1, 1), lower_flag=False)
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
            return customer_fuzz, declaration_fuzz, branch_fuzz, only_fuzz
        except Exception:
            ml_logger(type_log="ERROR", component="Custom OD-Evaluation",
                      message="exception in key_word_extraction",
                      status_code="500", traceback=traceback.format_exc())
            raise

    def key_word_extraction_of_applicants(
            self, all_response: List) -> Tuple[str, str, str, str]:
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
            for word in all_response:
                primary = self.hlp.fuzzy_match(
                    ["(Primary"], word["description"], ngram_range=(1, 3))
                applicant = self.hlp.fuzzy_match(
                    ["Applicant)"], word["description"], ngram_range=(1, 3))
                joint = self.hlp.fuzzy_match(
                    ["(joint"], word["description"], ngram_range=(1, 3))
                holder = self.hlp.fuzzy_match(
                    ["Holder"], word["description"], ngram_range=(1, 3))
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
            return primary_fuzz, applicant_fuzz, holder_fuzz, joint_fuzz
        except Exception:
            ml_logger(type_log="ERROR", component="Custom OD-Evaluation",
                      message="exception in key_word_extraction_of_applicants",
                      status_code="500", traceback=traceback.format_exc())
            raise

    def extract_count_of_signature(
            self, all_response: List, roi_shape_w: int, roi_shape_h: int,
            bounding_box_coordinate: List[List],
            comp_img: ndarray, pt_y_customer: int,
            confidence_scores: List) -> Tuple[
        int, int, int, float, float, float]:
        """
        extracting the count of signature present on the form
        Args:
            all_response: response form ocr
            roi_shape_w: width of roi
            roi_shape_h: height of roi
            bounding_box_coordinate: co-ordinates of bounding box
            comp_img: compressed image
            pt_y_customer: y coordinate of customer key word
            confidence_scores: List of prediction confidence score
        Retruns:
            primary_holder_count: count of primary signature
            joint_holder1_count: count of holder 1
            joint_holder2_count: count of holder2
            primary_confidence: confidence of primary signature prediction
            holder1_confidence: confidence of holder1 signature prediction
            holder2_confidence: confidence of holder2 signature prediction
        """
        try:
            primary_holder_count = 0
            joint_holder1_count = 0
            joint_holder2_count = 0
            primary_confidence = 0
            holder1_confidence = 0
            holder2_confidence = 0
            primary_fuzz, applicant_fuzz, holder_fuzz, joint_fuzz = \
                self.key_word_extraction_of_applicants(all_response)
            primary_holder, holder_1, holder_2 = \
                self.hlp.extract_word_coordinates(
                    all_response, primary_fuzz,
                    applicant_fuzz, joint_fuzz, holder_fuzz)
            start_point_p, end_point_p = \
                self.hlp.extract_combined_word_coordinates(
                    combine_list=primary_holder)
            start_point_jh1, end_point_jh1 = \
                self.hlp.extract_combined_word_coordinates(
                    combine_list=holder_1)
            start_point_jh2, end_point_jh2 = \
                self.hlp.extract_combined_word_coordinates(
                    combine_list=holder_2)
            pt_x_primary, pt_y_primary = self.hlp.mid_point_bb(
                start_point_p, end_point_p)
            pt_x_holder1, pt_y_holder1 = self.hlp.mid_point_bb(
                start_point_jh1, end_point_jh1)
            pt_x_holder2, pt_y_holder2 = self.hlp.mid_point_bb(
                start_point_jh2, end_point_jh2)
            for count, _ in enumerate(bounding_box_coordinate):
                coordinate = bounding_box_coordinate[count]
                start_point_sign, end_point_sign = \
                    self.hlp.bounding_box_extract(coordinate, comp_img)
                pt_x_sign, pt_y_sign = self.hlp.mid_point_bb(
                    start_point_sign, end_point_sign)
                if (pt_x_sign in range(0, roi_shape_w)) and (
                        pt_y_sign in range(pt_y_customer, roi_shape_h)):
                    distance_primary = self.hlp.distance_btn_points(
                        pt_x_primary, pt_y_primary, pt_x_sign, pt_y_sign)
                    distance_holder1 = self.hlp.distance_btn_points(
                        pt_x_holder1, pt_y_holder1, pt_x_sign, pt_y_sign)
                    distance_holder2 = self.hlp.distance_btn_points(
                        pt_x_holder2, pt_y_holder2, pt_x_sign, pt_y_sign)
                    if distance_primary is not None and distance_primary <= \
                            250 and pt_y_primary > pt_y_sign:
                        primary_holder_count += 1
                        primary_confidence = confidence_scores[count]
                    else:
                        pass
                    if distance_holder1 is not None and distance_holder1 <= \
                            250 and pt_y_holder1 > pt_y_sign:
                        joint_holder1_count += 1
                        holder1_confidence = confidence_scores[count]
                    else:
                        pass
                    if distance_holder2 is not None and distance_holder2 <= \
                            250 and pt_y_holder2 > pt_y_sign:
                        joint_holder2_count += 1
                        holder2_confidence = confidence_scores[count]
                    else:
                        pass
            return primary_holder_count, joint_holder1_count,\
        joint_holder2_count, primary_confidence, holder1_confidence,\
        holder2_confidence
        except Exception:
            ml_logger(type_log="ERROR", component="Custom OD-Evaluation",
                      message="exception in extract_count_of_signature",
                      status_code="500", traceback=traceback.format_exc())
            raise

    def extract(self, file_bytes: bytes, cdc_ocr) -> Tuple[
        int, int, int, float, float, float]:
        """
        extract count of signatures from stay connected forms
        Args:
            file_bytes: Image file in bytes
            cdc_ocr: ocr response from cdc
        Returns:
            primary_holder_count: count of Primary Holder signature
            joint_holder1_count: count of Holder 1 Signature
            joint_holder2_count: count of Holder 2 Signature
            primary_confidence: confidence of primary signature prediction
            holder1_confidence: confidence of holder1 signature prediction
            holder2_confidence: confidence of holder2 signature prediction
        Raise:
            Exception
        """
        primary_holder_count = 0
        joint_holder1_count = 0
        joint_holder2_count = 0
        primary_confidence = 0
        holder1_confidence = 0
        holder2_confidence = 0
        img_bytes = file_bytes
        resize_flag = False
        try:
            if sys.getsizeof(img_bytes) / 1000000 > 1:
                resize_flag = True
                resize_name = self.hlp.resize_image(file_bytes)
                with open(resize_name, "rb") as file_pointer:
                    img_bytes = file_pointer.read()
                    comp_img = np.frombuffer(img_bytes, np.uint8)
                    comp_img = cv2.imdecode(comp_img, cv2.IMREAD_COLOR)
                    img_h, img_w, _ = comp_img.shape
            if not resize_flag:
                comp_img = np.frombuffer(file_bytes, np.uint8)
                comp_img = cv2.imdecode(comp_img, cv2.IMREAD_COLOR)
                img_h, img_w, _ = comp_img.shape
            bounding_box_dict = self.pred.test_model_bytes(img_bytes=img_bytes,
                                                           input_size=(
                                                           640, 640))
            if bounding_box_dict and "signature" \
                    in bounding_box_dict["displayNames"]:
                all_response = self.hlp.cdc_ocr_wrap(cdc_ocr)
                customer_fuzz, declaration_fuzz, only_fuzz, branch_fuzz = \
                    self.key_word_extraction(all_response)
                customer_decl, branch_only = \
                    self.hlp.extract_word_roi_coordinates(
                        all_response, customer_fuzz,
                        declaration_fuzz, branch_fuzz, only_fuzz)
                start_point_cd, end_point_cd = \
                    self.hlp.extract_combined_word_roi_coordinates(
                        combine_list=customer_decl)
                start_point_bo, end_point_bo = \
                    self.hlp.extract_combined_word_roi_coordinates(
                        combine_list=branch_only)
                _, pt_y_customer = self.hlp.mid_point_bb(
                    start_point_cd, end_point_cd)
                _, pt_y_only = self.hlp.mid_point_bb(
                    start_point_bo, end_point_bo)
                if pt_y_customer is None:
                    pt_y_customer = img_h // 2
                if pt_y_only is None:
                    pt_y_only = img_h
                if pt_y_customer >= pt_y_only:
                    pt_y_customer = img_h // 2
                signature_codinates = []
                confidence_scores = []
                for ind, label in enumerate(
                        bounding_box_dict["displayNames"]):
                    if label == "signature":
                        signature_codinates.append(
                            bounding_box_dict["bboxes"][ind])
                        confidence_scores.append(
                            bounding_box_dict["confidence"][ind])
                roi_shape_w = img_w
                roi_shape_h = pt_y_only
                primary_holder_count, joint_holder1_count, \
                joint_holder2_count, primary_confidence, holder1_confidence,\
                holder2_confidence = self.extract_count_of_signature(
                    all_response, roi_shape_w, roi_shape_h,
                    signature_codinates, comp_img, pt_y_customer,
                    confidence_scores)
                if resize_flag:
                    os.remove(resize_name)
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
            return primary_holder_final, joint_holder1_final,\
        joint_holder2_final, primary_confidence, holder1_confidence,\
        holder2_confidence
        except Exception:
            ml_logger(type_log="ERROR", component="Custom OD-Evaluation",
                      message="exception in extract",
                      status_code="500", traceback=traceback.format_exc())
            raise
