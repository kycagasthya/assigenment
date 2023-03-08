# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

from fuzzywuzzy import fuzz
from PIL import Image
from qdocai.logger import QDocLogger
from qdocai.utils import DocAIBase, DocAIException
from io import BytesIO
from typing import Dict, List, Tuple, Union, Optional
from numpy import ndarray
import traceback
from scipy.spatial import distance
from docai.models.stay_connected_v3 import error_code
import time

class SignParserHelper(DocAIBase):
    def __init__(self, request_id: str, page_id: str, project: str):
        self.request_id = request_id
        self.page_id = page_id
        self.logger = QDocLogger()
        self.project = project
        self.error_dict = error_code.Errors.error_codes
        super().__init__(request_id, page_id)

    def cdc_ocr_cleaning(self, document: Dict) -> Tuple[List, List]:
        """
        gives list co-ordinates and list of words
        Args:
            document: row ocr dictionary
        Returns:
            li_cord: list of co-ordinate
            li_word: list of words
        """
        try:
            li_cord = []
            li_word = []
            full_txt = document["text"]
            for val in document["pages"][0]["tokens"]:
                if val["layout"]["textAnchor"]:
                    for string in val["layout"]["textAnchor"]["textSegments"]:
                        start_idx = (
                            int(string["startIndex"])
                            if string["startIndex"]
                            else 0
                        )
                        end_idx = (
                            int(string["endIndex"]) if string["endIndex"] else 0
                        )
                        text = full_txt[start_idx:end_idx]
                        li_cord.append(
                            val["layout"]["boundingPoly"]["vertices"]
                        )
                        li_word.append(text)
            return li_cord, li_word
        except Exception as error:
            self.logger.ml_logger(
                level="ERROR",
                ml_package="docai-models-stayconnected",
                action="cdc ocr cleaning falied",
                status_code=self.error_dict["ERROR_CLEANING_OCR"]["code"],
                message=self.error_dict["ERROR_CLEANING_OCR"]["text_desc"],
                request_id=self.request_id,
                page_id=self.page_id,
            )
            raise DocAIException(
                action="bytes_detect_text",
                message=self.error_dict["ERROR_CLEANING_OCR"]["text_desc"],
                status_desc=self.error_dict["ERROR_CLEANING_OCR"]["desc"],
                status_code=self.error_dict["ERROR_CLEANING_OCR"]["code"],
            ) from error

    def cdc_ocr_wrap(self, raw_ocr: Dict) -> List:
        """
        get all response
        Args:
            raw_ocr: cdc ocr as input
        Returns:
            all_response: all cleaned response
        """
        try:
            all_response = []
            cords, words = self.cdc_ocr_cleaning(raw_ocr)
            for cordinate, word in zip(cords, words):
                temp_main = {}
                temp_main["description"] = word
                temp_main["boundingPoly"] = {"vertices": cordinate}
                all_response.append(temp_main)
            return all_response
        except Exception as error:
            self.logger.ml_logger(
                level="ERROR",
                ml_package="docai-models-stayconnected",
                action="cdc ocr extract failed",
                status_code=self.error_dict["ERROR_OCR_WRAP"]["code"],
                message=self.error_dict["ERROR_OCR_WRAP"]["text_desc"],
                request_id=self.request_id,
                page_id=self.page_id,
            )
            raise DocAIException(
                action="bytes_detect_text",
                message=self.error_dict["ERROR_OCR_WRAP"]["text_desc"],
                status_desc=self.error_dict["ERROR_OCR_WRAP"]["desc"],
                status_code=self.error_dict["ERROR_OCR_WRAP"]["code"],
            ) from error

    def resize_image(self, im_bytes: bytes) -> Union[str, None]:
        """
        resizing the image
        Args:
            im_bytes: image bytes
        return:
            temp_compressed_img: compressed image
        """
        try:
            stream = BytesIO(im_bytes)
            image = Image.open(stream).convert("RGB")
            stream.close()
            temp_compressed_img = f"{time.time()}.jpg"
            image.save(temp_compressed_img, optimize=True, quality=3)
            return temp_compressed_img
        except Exception as error:
            self.logger.ml_logger(
                level="ERROR",
                ml_package="docai-models-stayconnected",
                action="resized image extraction failed",
                status_code=self.error_dict["ERROR_RESIZED_IMAGE"]["code"],
                message=self.error_dict["ERROR_RESIZED_IMAGE"]["text_desc"],
                request_id=self.request_id,
                page_id=self.page_id,
            )
            raise DocAIException(
                action="resize_image",
                message=self.error_dict["ERROR_RESIZED_IMAGE"]["text_desc"],
                status_desc=self.error_dict["ERROR_RESIZED_IMAGE"]["desc"],
                status_code=self.error_dict["ERROR_RESIZED_IMAGE"]["code"],
            ) from error

    def bounding_box_extract(
        self, bounding_roi: List, image: ndarray
    ) -> Union[Tuple[Tuple[int, int], Tuple[int, int]], Tuple[Tuple, Tuple]]:
        """
        bounding box co-ordinates
        Args:
            bounding_roi: list of bounding box co-ordinates
            image: full image
        Returns:
            start_point_roi: starting point of roi
            end_point_roi: ending point of roi
        """
        try:
            h, w = image.shape[0], image.shape[1]
            xmin = int(bounding_roi[0] * w)
            xmax = int(bounding_roi[1] * w)
            ymin = int(bounding_roi[2] * h)
            ymax = int(bounding_roi[3] * h)
            start_point_roi = (xmin, ymin)
            end_point_roi = (xmax, ymax)
            return start_point_roi, end_point_roi
        except Exception as error:
            self.logger.ml_logger(
                level="ERROR",
                ml_package="docai-models-stayconnected",
                action=f"Bounding box coordinate start and end point:\
                {start_point_roi}, {end_point_roi}",
                status_code=self.error_dict["ERROR_BOUNDING_BOX_EXTRACTION"][
                    "code"
                ],
                message=self.error_dict["ERROR_BOUNDING_BOX_EXTRACTION"][
                    "text_desc"
                ],
                request_id=self.request_id,
                page_id=self.page_id,
            )
            raise DocAIException(
                action="bounding_box_extract",
                message=self.error_dict["ERROR_BOUNDING_BOX_EXTRACTION"][
                    "text_desc"
                ],
                status_desc=self.error_dict["ERROR_BOUNDING_BOX_EXTRACTION"][
                    "desc"
                ],
                status_code=self.error_dict["ERROR_BOUNDING_BOX_EXTRACTION"][
                    "code"
                ],
            ) from error

    def extract_word_coordinates(
        self,
        all_response: List[Dict],
        primary_fuzz: str,
        applicant_fuzz: str,
        joint_fuzz: str,
        holder_fuzz: str,
    ) -> Tuple[List, List, List]:
        """
        extratcting word co-ordinate from ocr
        Args:
            all_response: ocr response
            primary_fuzz: fuzzy word for primary account holder
            applicant_fuzz: fuzzy word for applicant
            joint_fuzz: fuzzy word for joint
            holder_fuzz: fuzzy word for holder
        Returns:
            primary_li: primary applicant co-ordinate
            joint_holder_1: joint holder 1 co-ordinate
            joint_holder_2: joint holder 2 co-ordinate

        """
        try:
            joint_combine = []
            holder_combine = []
            primary_cord = None
            applicant_cord = None
            joint_cord = None
            holder_cord = None
            for x in all_response:
                if x["description"] == primary_fuzz:
                    primary_cord = x["boundingPoly"]
            for x in all_response:
                if x["description"] == applicant_fuzz:
                    applicant_cord = x["boundingPoly"]
            for x in all_response:
                if x["description"] == joint_fuzz:
                    joint_cord = x["boundingPoly"]
                    joint_combine.append(joint_cord)
            for x in all_response:
                if x["description"] == holder_fuzz:
                    holder_cord = x["boundingPoly"]
                    holder_combine.append(holder_cord)
            if (primary_cord is not None) and (applicant_cord is not None):
                primary_li = (
                    primary_cord["vertices"] + applicant_cord["vertices"]
                )
            else:
                primary_li = None
            if (joint_cord is not None) and (holder_cord is not None):
                joint_1 = joint_combine[0]
                holder_1 = holder_combine[0]
                joint_holder_1 = joint_1["vertices"] + holder_1["vertices"]
            else:
                joint_holder_1 = None
            if (joint_cord is not None) and (holder_cord is not None):
                joint_2 = joint_combine[-1]
                holder_2 = holder_combine[-1]
                joint_holder_2 = joint_2["vertices"] + holder_2["vertices"]
            else:
                joint_holder_2 = None
            return primary_li, joint_holder_1, joint_holder_2
        except Exception as error:
            self.logger.ml_logger(
                level="ERROR",
                ml_package="docai-models-stayconnected",
                action=f"static word cordinates primary_app,holder_1,holder_2:\
                {primary_li},{joint_holder_1},{joint_holder_2}",
                status_code=self.error_dict["ERROR_EXTRACTION_WORD_CORD"][
                    "code"
                ],
                message=self.error_dict["ERROR_EXTRACTION_WORD_CORD"][
                    "text_desc"
                ],
                request_id=self.request_id,
                page_id=self.page_id,
            )
            raise DocAIException(
                action="extract_word_coordinates",
                message=self.error_dict["ERROR_EXTRACTION_WORD_CORD"][
                    "text_desc"
                ],
                status_desc=self.error_dict["ERROR_EXTRACTION_WORD_CORD"][
                    "desc"
                ],
                status_code=self.error_dict["ERROR_EXTRACTION_WORD_CORD"][
                    "code"
                ],
            ) from error

    def extract_combined_word_coordinates(
        self, combine_list: List[Dict]
    ) -> Tuple[Tuple, Tuple]:
        """
        Extracting combine word co-ordinates
        Args:
            combine_list: combine static words co-ordinates
        Returns:
            start_point_word: starting point of word
            end_point_word: ending point of word
        """
        try:
            if combine_list is not None:
                x = [points["x"] for points in combine_list]
                y = [points["y"] for points in combine_list]
                x.sort()
                y.sort()
                x_min = x[0]
                y_min = y[0]
                x_max = x[-1]
                y_max = y[-1]
                start_point_word = (x_min, y_min)
                end_point_word = (x_max, y_max)
            else:
                start_point_word = None
                end_point_word = None
            return start_point_word, end_point_word
        except Exception as error:
            self.logger.ml_logger(
                level="ERROR",
                ml_package="docai-models-stayconnected",
                action=f"combine static word co-ordinates strat and end point:\
                {start_point_word},{end_point_word}",
                status_code=self.error_dict[
                    "ERROR_COMBINE_WORD_EXTRACTION_FAILED"
                ]["code"],
                message=self.error_dict["ERROR_COMBINE_WORD_EXTRACTION_FAILED"][
                    "text_desc"
                ],
                request_id=self.request_id,
                page_id=self.page_id,
            )
            raise DocAIException(
                action="extract_combined_word_coordinates",
                message=self.error_dict["ERROR_COMBINE_WORD_EXTRACTION_FAILED"][
                    "text_desc"
                ],
                status_desc=self.error_dict[
                    "ERROR_COMBINE_WORD_EXTRACTION_FAILED"
                ]["desc"],
                status_code=self.error_dict[
                    "ERROR_COMBINE_WORD_EXTRACTION_FAILED"
                ]["code"],
            ) from error

    def extract_word_roi_coordinates(
        self,
        all_response: List[Dict],
        customer_fuzz: str,
        declaration_fuzz: str,
        branch_fuzz: str,
        only_fuzz: str,
    ) -> Tuple[List, List]:
        """
        extratcting word co-ordinate from ocr
        Args:
            all_response: ocr response
            customer_fuzz: fuzzy word for customer account only
            declaration_fuzz: fuzzy word for declaration
            branch_fuzz: fuzzy word for branch
            only_fuzz: fuzzy word for only
        Returns:
            customer_decl: customer declaration co-ordinate
            branch_only: branch only 1 co-ordinate
        """
        try:
            customer_cord = None
            declaration_cord = None
            branch_cord = None
            only_cord = None
            for x in all_response:
                x["description"] = x["description"].replace("\n", "").strip()
                if x["description"] == customer_fuzz:
                    customer_cord = x["boundingPoly"]
                elif x["description"] == declaration_fuzz:
                    declaration_cord = x["boundingPoly"]
                elif x["description"] == branch_fuzz:
                    branch_cord = x["boundingPoly"]
                elif x["description"] == only_fuzz:
                    only_cord = x["boundingPoly"]
            if (customer_cord is not None) and (declaration_cord is not None):
                customer_decl = (
                    customer_cord["vertices"] + declaration_cord["vertices"]
                )
            else:
                customer_decl = None
            if (branch_cord is not None) and (only_cord is not None):
                branch_only = branch_cord["vertices"] + only_cord["vertices"]
            else:
                branch_only = None
            return customer_decl, branch_only
        except Exception as error:
            self.logger.ml_logger(
                level="ERROR",
                ml_package="docai-models-stayconnected",
                action=f"customer declaration and branch use roi cordinate:\
                {customer_decl},{branch_only}",
                message=self.error_dict["ERROR_EXTRACTION_WORD_ROI_FAILED"][
                    "text_desc"
                ],
                status_code=self.error_dict["ERROR_EXTRACTION_WORD_ROI_FAILED"][
                    "code"
                ],
                request_id=self.request_id,
                page_id=self.page_id,
            )
            raise DocAIException(
                action="extract_word_roi_coordinates",
                message=self.error_dict["ERROR_EXTRACTION_WORD_ROI_FAILED"][
                    "text_desc"
                ],
                status_desc=self.error_dict["ERROR_EXTRACTION_WORD_ROI_FAILED"][
                    "desc"
                ],
                status_code=self.error_dict["ERROR_EXTRACTION_WORD_ROI_FAILED"][
                    "code"
                ],
            ) from error

    def extract_combined_word_roi_coordinates(
        self, combine_list: List[Dict]
    ) -> Tuple[Tuple, Tuple]:
        """
        Extracting combine word co-ordinates
        Args:
            combine_list: combine static words co-ordinates
        Returns:
            start_point_word: starting point of word
            end_point_word: ending point of word
        """
        try:
            if combine_list is not None:
                x = [points["x"] for points in combine_list]
                y = [points["y"] for points in combine_list]
                x.sort()
                y.sort()
                x_min = x[0]
                y_min = y[0]
                x_max = x[-1]
                y_max = y[-1]
                start_point_word = (x_min, y_min)
                end_point_word = (x_max, y_max)
            else:
                start_point_word = None
                end_point_word = None
            return start_point_word, end_point_word
        except Exception as error:
            self.logger.ml_logger(
                level="ERROR",
                ml_package="docai-models-stayconnected",
                action=f"extract combine word cord start point, end point:\
                {start_point_word},{end_point_word}",
                message=self.error_dict["ERROR_COMBINE_WORD_ROI_FAILED"][
                    "text_desc"
                ],
                status_code=self.error_dict["ERROR_COMBINE_WORD_ROI_FAILED"][
                    "code"
                ],
                request_id=self.request_id,
                page_id=self.page_id,
            )
            raise DocAIException(
                action="extract_combined_word_roi_coordinates",
                message=self.error_dict["ERROR_COMBINE_WORD_ROI_FAILED"][
                    "text_desc"
                ],
                status_desc=self.error_dict["ERROR_COMBINE_WORD_ROI_FAILED"][
                    "desc"
                ],
                status_code=self.error_dict["ERROR_COMBINE_WORD_ROI_FAILED"][
                    "code"
                ],
            ) from error

    def mid_point_bb(
        self, signature_start: Tuple, signature_end: Tuple
    ) -> Union[Tuple[Optional[int], Optional[int]], Tuple[None, None]]:
        """
        mid point of bounding box
        Args:
            signature_start: start point of signature
            signature_end: ending point of signature
        Returns:
            pt_x: x co-ordinate
            pt_y: y co-ordinate
        """
        try:
            if (signature_start is not None) and (signature_end is not None):
                width = signature_end[0] - signature_start[0]
                height = signature_end[1] - signature_start[1]
                pt_x = signature_start[0] + width / 2
                pt_y = signature_start[1] + height / 2
                pt_x = int(pt_x)
                pt_y = int(pt_y)
            else:
                pt_x = None
                pt_y = None
            return pt_x, pt_y
        except Exception as error:
            message = traceback.format_exc()
            self.logger.ml_logger(
                level="ERROR",
                ml_package="docai-models-stayconnected",
                action="Internal Error",
                message=self.error_dict["ERROR_MID_POINT_EXTRACTION_FAILED"][
                    "text_desc"
                ]
                - {message},
                status_code=self.error_dict[
                    "ERROR_MID_POINT_EXTRACTION_FAILED"
                ]["code"],
                request_id=self.request_id,
                page_id=self.page_id,
            )
            raise DocAIException(
                action="mid_point_bb",
                message=self.error_dict["ERROR_MID_POINT_EXTRACTION_FAILED"][
                    "text_desc"
                ],
                status_desc=self.error_dict[
                    "ERROR_MID_POINT_EXTRACTION_FAILED"
                ]["desc"],
                status_code=self.error_dict[
                    "ERROR_MID_POINT_EXTRACTION_FAILED"
                ]["code"],
            ) from error

    def left_mid_point_bb(
        self, signature_start: Tuple, signature_end: Tuple
    ) -> Union[Tuple[Optional[int], Optional[int]], Tuple[None, None]]:
        """
        left mid point of bounding box
        Args:
            signature_start: start point of signature
            signature_end: ending point of signature
        Returns:
            pt_x: x co-ordinate
            pt_y: y co-ordinate
        """
        try:
            if (signature_start is not None) and (signature_end is not None):
                height = signature_end[1] - signature_start[1]
                pt_x = signature_start[0]
                pt_y = signature_start[1] + height / 2
                pt_x = int(pt_x)
                pt_y = int(pt_y)
            else:
                pt_x = None
                pt_y = None
            return pt_x, pt_y
        except Exception as error:
            self.logger.ml_logger(
                level="ERROR",
                ml_package="docai-models-stayconnected",
                action="left mid point failed",
                status_code=self.error_dict["ERROR_LEFT_MID_POINT_FAILED"][
                    "code"
                ],
                message=self.error_dict["ERROR_LEFT_MID_POINT_FAILED"][
                    "text_desc"
                ],
                request_id=self.request_id,
                page_id=self.page_id,
            )
            raise DocAIException(
                action="left_mid_point_bb",
                message=self.error_dict["ERROR_LEFT_MID_POINT_FAILED"][
                    "text_desc"
                ],
                status_desc=self.error_dict["ERROR_LEFT_MID_POINT_FAILED"][
                    "desc"
                ],
                status_code=self.error_dict["ERROR_LEFT_MID_POINT_FAILED"][
                    "code"
                ],
            ) from error

    def generate_ngrams(self, sentence: str, ngram_range: Tuple) -> List:
        """
        To get the ngrams from a sentence within a given range

        Args:
            sentence: text from the OCR json response.
            ngram_range: the range of ngrams to be extracted.

        Returns:
            grams_list: List of ngrams within a range from the sentence.
        """
        try:
            sentence = sentence.split()
            grams_list = []
            for num in range(ngram_range[0], ngram_range[1] + 1):
                grams = [
                    " ".join(sentence[i : i + num])
                    for i in range(len(sentence) - num + 1)
                ]
                grams_list += grams
            return grams_list
        except Exception as error:
            self.logger.ml_logger(
                level="ERROR",
                ml_package="docai-models-stayconnected",
                action="Internal Error",
                status_code=self.error_dict["ERROR_NGRAM_FAILED"]["code"],
                message=self.error_dict["ERROR_NGRAM_FAILED"]["text_desc"],
                request_id=self.request_id,
                page_id=self.page_id,
            )
            raise DocAIException(
                action="generate_ngrams",
                message=self.error_dict["ERROR_NGRAM_FAILED"]["text_desc"],
                status_desc=self.error_dict["ERROR_NGRAM_FAILED"]["desc"],
                status_code=self.error_dict["ERROR_NGRAM_FAILED"]["code"],
            ) from error

    def norm_distance(self, pt1_x: int,
                      pt1_y: int, pt2_x: int, pt2_y: int,
                      img_w: int, img_h: int
                     )-> float:
        """
        To get Normalized Distance
        Args:
            pt1_x: x1 point
            pt1_y: y1 point
            pt2_x: x1 point
            pt2_y: y2 point
            img_w: image width
            img_h: image height
        Returns:
            distance.euclidean : euclidean distance
        """
        try:
            a = (pt1_x / img_w, pt1_y / img_h)
            b = (pt2_x / img_w, pt2_y / img_h)
            return distance.euclidean(a, b)
        except Exception as error:
            self.logger.ml_logger(
                level="ERROR",
                ml_package="docai-models-stayconnected",
                action="euclidean distance failed",
                status_code=self.error_dict["ERROR_EUCLIDEAN_DISTANCE_FAILED"][
                    "code"
                ],
                message=self.error_dict["ERROR_EUCLIDEAN_DISTANCE_FAILED"][
                    "text_desc"
                ],
                request_id=self.request_id,
                page_id=self.page_id,
            )
            raise DocAIException(
                action="Euclidean distance",
                message=self.error_dict["ERROR_EUCLIDEAN_DISTANCE_FAILED"][
                    "text_desc"
                ],
                status_desc=self.error_dict["ERROR_EUCLIDEAN_DISTANCE_FAILED"][
                    "desc"
                ],
                status_code=self.error_dict["ERROR_EUCLIDEAN_DISTANCE_FAILED"][
                    "code"
                ],
            ) from error

    def fuzzy_match(
        self,
        possible_values: List,
        string: str,
        threshold: int = 75,
        ngram_range: Tuple = (1, 1),
        lower_flag: bool = True,
    ) -> Union[Tuple[str, str], Tuple[None, None]]:
        """
        This function is used to get the fuzzy matched word from string

        Args:
            possible_values: words to match,
            string: text from the OCR json response,
            threshold: to set a confidence for fuzzy matching,
            ngram_range: the range of ngrams to be extracted.
            lower_flag: indicate whether to lower the key while matching
        Returns:
            key_name: ngram that fuzzy match the given possible_values.
            value: value within possible values that fuzzy match with key_name.
        """
        try: #pylint: disable=R1702
            final_dict = {}
            ngrams_string = self.generate_ngrams(
                string.replace("\n", " "), ngram_range=ngram_range
            )
            for value in possible_values:
                for ngram in ngrams_string:
                    if lower_flag:
                        score = fuzz.ratio(value.lower(), ngram.lower())
                    else:
                        score = fuzz.ratio(value, ngram)
                    if score >= threshold:
                        if ngram in final_dict:
                            if score > final_dict[ngram][0]:
                                final_dict[ngram] = score, value
                        else:
                            final_dict[ngram] = score, value
            if final_dict:
                key_name = max(final_dict, key=lambda x: final_dict[x][0])
                value = final_dict[key_name][1]
            else:
                key_name = None
                value = None
            return key_name, value
        except Exception as error:
            self.logger.ml_logger(
                level="ERROR",
                ml_package="docai-models-stayconnected",
                action="fuzzy match failed",
                status_code=self.error_dict["ERROR_FUZZY_MATCH_FAILED"]["code"],
                message=self.error_dict["ERROR_FUZZY_MATCH_FAILED"][
                    "text_desc"
                ],
                request_id=self.request_id,
                page_id=self.page_id,
            )
            raise DocAIException(
                action="fuzzy_match",
                message=self.error_dict["ERROR_FUZZY_MATCH_FAILED"][
                    "text_desc"
                ],
                status_desc=self.error_dict["ERROR_FUZZY_MATCH_FAILED"]["desc"],
                status_code=self.error_dict["ERROR_FUZZY_MATCH_FAILED"]["code"],
            ) from error
