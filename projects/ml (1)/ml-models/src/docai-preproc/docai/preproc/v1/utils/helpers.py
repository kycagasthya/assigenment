# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

"""This helpers could be used for image pre-processing step"""

import io
import sys
import traceback
import time
from typing import Tuple

import cv2
import numpy as np
from deskew import determine_skew
from PIL import Image, UnidentifiedImageError, TiffImagePlugin
from skimage.transform import rotate
from qdocai.logger import QDocLogger
from qdocai.utils import DocAIBase, DocAIException
from docai.preproc.v1.utils import error_code


class ImageOperation(DocAIBase):
    """Can be used for image normalisation, deskewing,
    processing image byte to produce ocr json

    Pre-processing fucntion (preprocess_bytes) takes
    image bytes and performs open-cv operations on it.

    bytes_detect_text uses vision OCR API to detect
    text in image.

    Args:
        file_bytes: Image in bytes
        request_id: This request id is used to track
        the complete request.
        page_id: The page no is represented as page_id

    Returns:
        None

    """

    def __init__(self,
                 file_bytes: bytes,
                 request_id: str,
                 page_id: str) -> None:
        """Initialises file bytes

        Returns:
            None
        """
        self.img = file_bytes
        self.logger = QDocLogger()
        self.error_dict = error_code.Errors.error_codes
        self.ml_package = "docai-preproc"
        DocAIBase.__init__(self, request_id=request_id, page_id=page_id)

    def normlaization(self,
                      norm_img_size: Tuple[int, int] = (800, 800)
                     ) -> bytes:
        """Used for Image Normalisation
        Args:
            norm_img_size: image size for normalisation
        Returns:
            bytes
        """
        norm_img = np.zeros(norm_img_size)
        self.img = cv2.normalize(self.img,
                                 norm_img, 0, 255, cv2.NORM_MINMAX)
        return self.img

    def gray_scale(self) -> bytes:
        """Convert coloured image to greyscale

        Returns:
            bytes"""
        self.img = cv2.cvtColor(self.img,
                                cv2.COLOR_BGR2GRAY)
        return self.img

    def deskew(self) -> bytes:
        """Removes skew from the image

        Returns:
            bytes
        """
        try:
            angle = determine_skew(self.img)
            rotated = rotate(self.img, angle,
                             resize=True) * 255
            rotation = rotated.astype(np.uint8)
            self.img = rotation
            return self.img

        except Exception as error:
            exc_type, exc_value, exc_tb = sys.exc_info()
            trace_back = traceback.TracebackException(
                exc_type, exc_value, exc_tb)
            error_msg = self.error_dict[
                    "ERROR_DESKEW_FAILED"]["text_desc"]

            self.logger.ml_logger(
                level="ERROR",
                ml_package=self.ml_package,
                action="Deskew Operation",
                message=f"{error_msg} - {trace_back}",
                status_code=self.error_dict[
                    "ERROR_DESKEW_FAILED"]["code"],
                request_id=self.request_id,
                page_id=self.page_id,
            )

            raise DocAIException(
                action="Deskew Operation",
                message=self.error_dict[
                    "ERROR_DESKEW_FAILED"]["text_desc"],
                status_desc=self.error_dict[
                    "ERROR_DESKEW_FAILED"]["desc"],
                status_code=self.error_dict[
                    "ERROR_DESKEW_FAILED"]["code"],
            ) from error

    def preprocess_bytes(
        self,
        ext: str = ".jpg",
        min_width: int = 200,
        min_height: int = 200,
        gray_scale_flag: bool = False,
        deskew_scale_flag: bool = False,
    ) -> Tuple[bytes, int, bool]:
        """
        Pre-processing the images, takes image bytes
        and performs open-cv operations on it.

        Args:
            ext: (default: jpg)file type of bytes passed.
            min_width: Width used in pixel resolution method.
            min_height: Height used in pixel resolution method
            gray_scale_flag: "True" if you want image in gray scale,
            "False" if you want image in color
            deskew_scale_flag: "True" will deskew the image,
            and "False" will pass it unaffected.


        Returns:
            content: Image Bytes
            dpi_value: DPI value of the image
            pixel_flag: Returns True or False as per resolution
            satisfaction of image above threshold
        """
        try:
            start_time = time.time()
            dpi_value = self.get_dpi()
            pixel_flag = self.check_min_resolution(min_width, min_height)

            self.img = np.asarray(bytearray(self.img))
            self.img = cv2.imdecode(self.img, cv2.IMREAD_COLOR)
            if (gray_scale_flag and deskew_scale_flag):
                self.img = self.normlaization()
                self.img = self.gray_scale()
                self.img = self.deskew()
            else:
                if deskew_scale_flag:
                    self.img = self.normlaization()
                    self.img = self.deskew()
                else:
                    if gray_scale_flag:
                        self.img = self.normlaization()
                        self.img = self.gray_scale()


            _, encoded_image = cv2.imencode(ext, self.img)
            content = encoded_image.tobytes()

            self.logger.ml_logger(
                level="INFO",
                ml_package=self.ml_package,
                action="Image Bytes Preprocessed",
                message=f"Processing Completed Successfully - [TIME] Total \
                Time taken for image preprocessing is\
                {time.time()-start_time} seconds.",
                status_code=200,
                request_id=self.request_id,
                page_id=self.page_id,
            )

        except Exception as error:
            exc_type, exc_value, exc_tb = sys.exc_info()
            trace_back = traceback.TracebackException(
                exc_type, exc_value, exc_tb)
            error_msg = self.error_dict[
                    "ERROR_PREPROCESSING_FAILED"]["text_desc"]

            self.logger.ml_logger(
                level="ERROR",
                ml_package=self.ml_package,
                action="Image Bytes Preprocessing",
                message=f"{error_msg} - {trace_back}",
                status_code=self.error_dict[
                    "ERROR_PREPROCESSING_FAILED"]["code"],
                request_id=self.request_id,
                page_id=self.page_id,
            )

            raise DocAIException(
                action="Image Bytes Preprocessing",
                message=self.error_dict[
                    "ERROR_PREPROCESSING_FAILED"]["text_desc"],
                status_desc=self.error_dict[
                    "ERROR_PREPROCESSING_FAILED"]["desc"],
                status_code=self.error_dict[
                    "ERROR_PREPROCESSING_FAILED"]["code"]
            ) from error
        return content, dpi_value, pixel_flag

    def get_dpi(self) -> float:
        """
        Checks DPI metdata in image and returns it.

        Returns:
            Float value of DPI.

        """
        try:
            im = Image.open(io.BytesIO(self.img))
            dpi_value = im.info["dpi"]
            if type(dpi_value[0]) == TiffImagePlugin.IFDRational:
                num1 = dpi_value[0]._numerator/dpi_value[0]._denominator
                num2 = dpi_value[1]._numerator/dpi_value[1]._denominator
                dpi_value = (num1, num2)
            dpi_avg = np.average(dpi_value)
            return dpi_avg

        except KeyError as _:
            exc_type, exc_value, exc_tb = sys.exc_info()
            trace_back = traceback.TracebackException(
                exc_type, exc_value, exc_tb)
            error_msg = self.error_dict[
                    "ERROR_NO_DPI"]["text_desc"]

            self.logger.ml_logger(
                level="WARNING",
                ml_package=self.ml_package,
                action="DPI Validation",
                message=f"{error_msg} - {trace_back}",
                status_code=self.error_dict[
                    "ERROR_NO_DPI"]["code"],
                request_id=self.request_id,
                page_id=self.page_id,
            )
            return None

    def check_min_resolution(self,
                             min_width: int = 200,
                             min_height: int = 200) -> bool:
        """
        Checks minimum resolution criteria for the image

        Returns:
            bool if image satisfies the minimum resolution criteria


        """
        try:
            im = Image.open(io.BytesIO(self.img))
            width, height = im.size
            if width >= min_width and height >= min_height:
                return True
            return False

        except UnidentifiedImageError as error:
            exc_type, exc_value, exc_tb = sys.exc_info()
            trace_back = traceback.TracebackException(
                exc_type, exc_value, exc_tb)
            error_msg = self.error_dict[
                    "ERROR_PIXEL_CALCULATION_FAILED"]["text_desc"]

            self.logger.ml_logger(
                level="ERROR",
                ml_package=self.ml_package,
                action="Pixel Calculation",
                message=f"{error_msg} - {trace_back}",
                status_code=self.error_dict[
                    "ERROR_PIXEL_CALCULATION_FAILED"]["code"],
                request_id=self.request_id,
                page_id=self.page_id,
            )

            raise DocAIException(
                action="Pixel Calculation",
                message=f"{error_msg} - {trace_back}",
                status_desc=self.error_dict[
                    "ERROR_PIXEL_CALCULATION_FAILED"]["desc"],
                status_code=self.error_dict[
                    "ERROR_PIXEL_CALCULATION_FAILED"]["code"]
            ) from error
