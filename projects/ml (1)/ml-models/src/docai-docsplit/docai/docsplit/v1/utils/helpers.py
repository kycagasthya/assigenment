# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

"""This includes valid file extension check, document splitting,
gcs download and upload methods."""


import sys
import traceback
import io

from typing import Tuple, List
import numpy as np
import cv2
import filetype
from PIL import Image, ImageSequence
from google.cloud import storage
import fitz
from qdocai.logger import QDocLogger
from qdocai.utils import DocAIBase, DocAIException
from docai.docsplit.v1.utils import error_code

MIME_TYPE = "image/jpeg"


class Helper(DocAIBase):
    """It include valid file extension check, download and upload to gcs
    methods.

    Helper class includes methods download_from_gcs, validate_file,
    upload_to_gcs

    Attributes:
        download_bucket_name: bucket Name where file is present in gcp.
        gcs_download_filepath: file path where file is located in the
        gcs bucket.
        upload_local_filepath: Local file path to be uploaded.
        destination_file_name: Local filename which needs to be created
        with file extension.
        process_bytes: [True/False] If set to True, will return file bytes.
    """

    def __init__(
        self,
        download_bucket_name: str,
        gcs_download_filepath: str,
        request_id: str,
        page_id: str,
        upload_local_filepath: str = "",
        destination_file_name: str = "",
        process_bytes: bool = True,
    ) -> None:
        """Initiates Helper Class with download_bucket_name and
        gcs_download_filepath"""

        self.download_bucket_name = download_bucket_name
        self.gcs_download_filepath = gcs_download_filepath
        self.destination_file_name = destination_file_name
        self.process_bytes = process_bytes
        self.upload_local_filepath = upload_local_filepath
        self.valid_file_types = ["png", "jpg", "jpeg", "pdf", "tiff", "tif"]
        self.ml_package = "docai-docsplit"
        self.logger = QDocLogger()
        self.error_dict = error_code.Errors.error_codes
        DocAIBase.__init__(self, request_id=request_id, page_id=page_id)

    def download_from_gcs(self) -> bytes:
        """Downloads the file from the gcs using bucketname
        and filepath.
        If process_bytes  is set to False, then will save file
        at destination_file_name

        Returns:
            File data in bytes if process_bytes is set to True,
            otherwise will create a local file.


        """

        # Initialise a client
        storage_client = storage.Client()  # self.projectid
        action = "Downloading file from gcs"
        try:
            # Create a bucket object for our bucket
            bucket = storage_client.get_bucket(
                self.download_bucket_name)
        except Exception as error:
            exc_type, exc_value, exc_tb = sys.exc_info()
            trace_back = traceback.TracebackException(
                exc_type, exc_value, exc_tb)
            error_msg = self.error_dict["ERROR_BUCKET_NOT_FOUND"]["text_desc"]

            self.logger.ml_logger(
                level="ERROR",
                ml_package=self.ml_package,
                action=action,
                message=f"{error_msg} - {trace_back}",
                status_code=self.error_dict["ERROR_BUCKET_NOT_FOUND"]["code"],
                request_id=self.request_id,
                page_id=self.page_id,
            )

            raise DocAIException(
                action=action,
                message=self.error_dict["ERROR_BUCKET_NOT_FOUND"]["text_desc"],
                status_desc=self.error_dict["ERROR_BUCKET_NOT_FOUND"]["desc"],
                status_code=self.error_dict["ERROR_BUCKET_NOT_FOUND"]["code"],
            ) from error

        try:
            # Create a blob object from the filepath
            blob = bucket.blob(self.gcs_download_filepath)
            # Download file as byte
            if self.process_bytes:
                try:
                    bytes_data = blob.download_as_bytes()
                except Exception as error:
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    trace_back = traceback.TracebackException(
                        exc_type, exc_value, exc_tb
                    )
                    error_msg = self.error_dict[
                            "ERROR_DOWNLOAD_FAILED"]["text_desc"]

                    self.logger.ml_logger(
                        level="ERROR",
                        ml_package=self.ml_package,
                        action=action,
                        message=f"{error_msg} - {trace_back}",
                        status_code=self.error_dict[
                            "ERROR_DOWNLOAD_FAILED"]["code"],
                        request_id=self.request_id,
                        page_id=self.page_id,
                    )

                    raise DocAIException(
                        action=action,
                        message=self.error_dict[
                            "ERROR_DOWNLOAD_FAILED"]["text_desc"],
                        status_desc=self.error_dict[
                            "ERROR_DOWNLOAD_FAILED"]["desc"],
                        status_code=self.error_dict[
                            "ERROR_DOWNLOAD_FAILED"]["code"],
                    ) from error
            # Download the file to a destination
            elif self.process_bytes is False:
                blob.download_to_filename(self.destination_file_name)
                return self.destination_file_name

        except Exception as error:
            exc_type, exc_value, exc_tb = sys.exc_info()
            trace_back = traceback.TracebackException(
                exc_type, exc_value, exc_tb)
            error_msg=self.error_dict[
                    "ERROR_BLOB_NOT_FOUND"]["text_desc"]
            self.logger.ml_logger(
                level="ERROR",
                ml_package=self.ml_package,
                action=action,
                message=f"{error_msg} - {trace_back}",
                status_code=self.error_dict[
                    "ERROR_BLOB_NOT_FOUND"]["code"],
                request_id=self.request_id,
                page_id=self.page_id,
            )

            raise DocAIException(
                action=action,
                message=self.error_dict[
                    "ERROR_BLOB_NOT_FOUND"]["text_desc"],
                status_desc=self.error_dict[
                    "ERROR_BLOB_NOT_FOUND"]["desc"],
                status_code=self.error_dict[
                    "ERROR_BLOB_NOT_FOUND"]["code"],
            ) from error

        return bytes_data

    def validate_file(self, bytes_data: bytes) -> Tuple[bool, str]:
        """Identifies correct extention for input bytes.

        Args:
            bytes_data: Bytes for a given input file.

        Returns:
            [True/False] status wrt validity of extention
            and extention.


        """
        # input to the module to guess file extention
        action = "Validation of file type"
        try:
            kind = filetype.guess(bytes_data)
            ext = kind.extension

        except AttributeError as error:
            exc_type, exc_value, exc_tb = sys.exc_info()
            trace_back = traceback.TracebackException(
                exc_type, exc_value, exc_tb)
            error_msg=self.error_dict[
                    "ERROR_ATTRIBUTE_ERROR"]["text_desc"]
            self.logger.ml_logger(
                level="ERROR",
                ml_package=self.ml_package,
                message=f"{error_msg} - {trace_back}",
                action=action,
                status_code=self.error_dict[
                    "ERROR_ATTRIBUTE_ERROR"]["code"],
                request_id=self.request_id,
                page_id=self.page_id,
            )

            raise DocAIException(
                action=action,
                message=self.error_dict[
                    "ERROR_ATTRIBUTE_ERROR"]["text_desc"],
                status_desc=self.error_dict[
                    "ERROR_ATTRIBUTE_ERROR"]["desc"],
                status_code=self.error_dict[
                    "ERROR_ATTRIBUTE_ERROR"]["code"],
            ) from error

        if ext in self.valid_file_types:
            return True, ext
        else:
            # false for an invalid extention not
            # present in predefined extentions
            error_msg = self.error_dict[
                    "ERROR_INVALID_FILE_TYPE"]["text_desc"]
            self.logger.ml_logger(
                level="ERROR",
                ml_package=self.ml_package,
                action=action,
                message=f"{error_msg} - {ext}",
                status_code=self.error_dict[
                    "ERROR_INVALID_FILE_TYPE"]["code"],
                request_id=self.request_id,
                page_id=self.page_id,
            )

            raise DocAIException(
                action=action,
                message=self.error_dict[
                    "ERROR_INVALID_FILE_TYPE"]["text_desc"],
                status_desc=self.error_dict[
                    "ERROR_INVALID_FILE_TYPE"]["desc"],
                status_code=self.error_dict[
                    "ERROR_INVALID_FILE_TYPE"]["code"],
            )

    def upload_to_gcs(
        self,
        bytes_data: bytes,
        upload_bucket_name: str,
        destination_blob_name: str,
        content_type: str = MIME_TYPE,
    ) -> None:
        """
        Uploads a file to the bucket.

        Returns:
            None

        """

        storage_client = storage.Client()  # self.projectid
        try:
            bucket = storage_client.bucket(upload_bucket_name)
            blob = bucket.blob(destination_blob_name)
            if self.process_bytes:
                blob.upload_from_string(bytes_data, content_type=content_type)
            else:
                blob.upload_from_filename(self.upload_local_filepath)

        except FileNotFoundError as error:
            exc_type, exc_value, exc_tb = sys.exc_info()
            trace_back = traceback.TracebackException(
                exc_type, exc_value, exc_tb)
            error_msg = self.error_dict[
                    "ERROR_FILE_NOT_FOUND"]["text_desc"]

            self.logger.ml_logger(
                level="ERROR",
                ml_package=self.ml_package,
                message=f"{error_msg} - {trace_back}",
                status_code=self.error_dict[
                    "ERROR_FILE_NOT_FOUND"]["code"],
                request_id=self.request_id,
                page_id=self.page_id,
            )

            raise DocAIException(
                action="Uploading file from gcs",
                message=self.error_dict[
                    "ERROR_FILE_NOT_FOUND"]["text_desc"],
                status_desc=self.error_dict[
                    "ERROR_FILE_NOT_FOUND"]["desc"],
                status_code=self.error_dict[
                    "ERROR_FILE_NOT_FOUND"]["code"],
            ) from error


class Splitter(DocAIBase):
    """Splitter class can be used to split and save jpg images
    from various inputs such as pdf, tif and png.
    """

    def __init__(self,
                 bytes_data: bytes,
                 request_id: str,
                 page_id: str) -> None:

        self.bytes_data = bytes_data
        self.logger = QDocLogger()
        DocAIBase.__init__(self, request_id=request_id, page_id=page_id)

    def _pdf_split_bytes(self) -> Tuple[List[bytes], str]:
        """Splits the pages of PDF into Images
        Args:
        bytes_data: PDF passed in bytes format

        Returns:
        An array of images in bytes
        """

        try:
            images = fitz.open("pdf", self.bytes_data)
            list_image_bytes = []
            for image in images:
                pix = image.get_pixmap(dpi=150)
                img = Image.frombytes("RGB",
                                      [pix.width, pix.height],
                                      pix.samples)
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format="JPEG")
                img_byte_arr = img_byte_arr.getvalue()
                list_image_bytes.append(img_byte_arr)
            return list_image_bytes, MIME_TYPE

        except KeyError as error:
            exc_type, exc_value, exc_tb = sys.exc_info()
            trace_back = traceback.TracebackException(
                exc_type, exc_value, exc_tb)
            error_msg = self.error_dict[
                    "ERROR_PDF_SPLITTING_FAILED"]["text_desc"]

            self.logger.ml_logger(
                level="ERROR",
                ml_package=self.ml_package,
                action="PDF Splitting",
                message=f"{error_msg} - {trace_back}",
                status_code=self.error_dict[
                    "ERROR_PDF_SPLITTING_FAILED"]["code"],
                request_id=self.request_id,
                page_id=self.page_id,
            )

            raise DocAIException(
                action="PDF Splitting",
                message=self.error_dict[
                    "ERROR_PDF_SPLITTING_FAILED"]["text_desc"],
                status_desc=self.error_dict[
                    "ERROR_PDF_SPLITTING_FAILED"]["desc"],
                status_code=self.error_dict[
                    "ERROR_PDF_SPLITTING_FAILED"]["code"],
            ) from error

    def _tiff_split_bytes(self) -> Tuple[List[bytes], str]:
        """Splits tiff file to images

        Args:
        bytes_data: tiff file data in bytes

        Returns:
        An array of images in bytes

        """

        imagehandler = Image.open(io.BytesIO(self.bytes_data))
        pages = []
        for _, page in enumerate(ImageSequence.Iterator(imagehandler)):
            try:
                page = page.convert("RGB")
                img_byte_arr = io.BytesIO()
                page.save(img_byte_arr, format="JPEG")
                img_byte_arr = img_byte_arr.getvalue()
                pages.append(img_byte_arr)
            except ValueError as error:
                exc_type, exc_value, exc_tb = sys.exc_info()
                trace_back = traceback.TracebackException(
                    exc_type, exc_value, exc_tb)
                error_msg = self.error_dict[
                        "ERROR_TIFF_SPLITTING_FAILED"]["text_desc"]

                self.logger.ml_logger(
                    level="ERROR",
                    ml_package=self.ml_package,
                    message=f"{error_msg} - {trace_back}",
                    action="TIFF Splitting",
                    status_code=self.error_dict[
                        "ERROR_TIFF_SPLITTING_FAILED"]["code"],
                    request_id=self.request_id,
                    page_id=self.page_id,
                )

                raise DocAIException(
                    action="TIFF Splitting",
                    message=self.error_dict[
                        "ERROR_TIFF_SPLITTING_FAILED"]["text_desc"],
                    status_desc=self.error_dict[
                        "ERROR_TIFF_SPLITTING_FAILED"]["desc"],
                    status_code=self.error_dict[
                        "ERROR_TIFF_SPLITTING_FAILED"]["code"],
                ) from error

        return pages, MIME_TYPE

    def _convert_png_bytes(self) -> Tuple[bytes, str]:
        """Converts PNG Image to JPEG Image.

        Args:
        bytes_data: PNG in Bytes

        Returns:
        JPEG in bytes
        """

        try:
            ext = ".jpg"
            img = np.asarray(bytearray(self.bytes_data))
            img = cv2.imdecode(img, cv2.IMREAD_COLOR)
            _, encoded_image = cv2.imencode(ext, img)
            content = encoded_image.tobytes()
            return content, MIME_TYPE
        except ValueError as error:
            exc_type, exc_value, exc_tb = sys.exc_info()
            trace_back = traceback.TracebackException(
                exc_type, exc_value, exc_tb)
            error_msg=self.error_dict[
                "ERROR_CONVERSION_FAILED"]["text_desc"]

            self.logger.ml_logger(
                level="ERROR",
                ml_package=self.ml_package,
                action="PNG Conversion to JPEG",
                message=f"{error_msg} - {trace_back}",
                status_code=self.error_dict["ERROR_CONVERSION_FAILED"]["code"],
                request_id=self.request_id,
                page_id=self.page_id,
            )

            raise DocAIException(
                action="PNG Conversion to JPEG",
                message=self.error_dict["ERROR_CONVERSION_FAILED"]["text_desc"],
                status_desc=self.error_dict["ERROR_CONVERSION_FAILED"]["desc"],
                status_code=self.error_dict["ERROR_CONVERSION_FAILED"]["code"],
            ) from error


class DocSplitting(Helper, Splitter):
    """
    Parent Class inheriting Helper, Splitter

    Attributes:
        gcs_uri: GCS path of the file as per landing bucket structure
            Example: "gs://icici-ia-docai-landing/raw-documents/crm/
            2022/02/07/61765cc88c57f9e85b03bb17.png"
    """

    def __init__(self, gcs_uri: str, request_id: str, page_id: str) -> None:
        # getting the configuration instance
        self.gcs_uri = gcs_uri

        self.year = self.gcs_uri.split("/")[-4]
        self.month = self.gcs_uri.split("/")[-3]
        self.day = self.gcs_uri.split("/")[-2]
        self.req_id = self.gcs_uri.split("/")[-1].split(".")[0]

        self.file_name = self.gcs_uri.split("/")[-1]
        self.download_bucket_name = self.gcs_uri.split("/")[2]
        self.gcs_download_filepath = self.gcs_uri.replace(
            f"gs://{self.download_bucket_name}/", ""
        )

        Helper.__init__(
            self,
            self.download_bucket_name,
            self.gcs_download_filepath,
            request_id,
            page_id,
        )
        self.bytes_data = self.download_from_gcs()
        Splitter.__init__(self, self.bytes_data, request_id, page_id)

    def run(self) -> Tuple[int, List[bytes]]:
        """ "run method to execute preocess for one file
        Returns:
            No. of pages, List of images.
        """
        action = "Docsplitting main method"
        try:
            _, file_ext = self.validate_file(self.bytes_data)
            if file_ext == "pdf":
                list_img, mime_type = self._pdf_split_bytes()

            if file_ext == "tif":
                list_img, mime_type = self._tiff_split_bytes()

            if file_ext == "png":
                file_bytes, mime_type = self._convert_png_bytes()
                list_img = [file_bytes]

            if file_ext == "jpg":
                list_img = [self.bytes_data]
                mime_type = MIME_TYPE

            num_pages = len(list_img)

            self.logger.ml_logger(
                level="INFO",
                ml_package="docai-docsplit",
                action=action,
                message="Successfully completed",
                status_code=200,
                request_id=self.request_id,
                page_id=self.page_id,
            )

            return num_pages, list_img, mime_type

        except ValueError as error:
            exc_type, exc_value, exc_tb = sys.exc_info()
            trace_back = traceback.TracebackException(
                exc_type, exc_value, exc_tb)
            error_msg = self.error_dict["ERROR_VALUE_ERROR"]["text_desc"]


            self.logger.ml_logger(
                level="ERROR",
                ml_package=self.ml_package,
                action="Image Bytes Processed from DocAI Docsplit",
                message=f"{error_msg} - {trace_back}",
                status_code=self.error_dict["ERROR_VALUE_ERROR"]["code"],
                request_id=self.request_id,
                page_id=self.page_id,
            )

            raise DocAIException(
                action=action,
                message=self.error_dict["ERROR_VALUE_ERROR"]["text_desc"],
                status_desc=self.error_dict["ERROR_VALUE_ERROR"]["desc"],
                status_code=self.error_dict["ERROR_VALUE_ERROR"]["code"],
            ) from error

        except DocAIException as error:
            raise DocAIException(
                action=error.get_exception()["action"],
                message=error.get_exception()["message"],
                status_desc=error.get_exception()["status_desc"],
                status_code=error.get_exception()["status_code"],
            ) from error

        except Exception as error:
            exc_type, exc_value, exc_tb = sys.exc_info()
            trace_back = traceback.TracebackException(
                exc_type, exc_value, exc_tb)
            error_msg = self.error_dict[
                "ERROR_UNIDENTIFIED_ERROR"]["text_desc"]

            self.logger.ml_logger(
                level="ERROR",
                ml_package=self.ml_package,
                action=action,
                message=f"{error_msg} - {trace_back}",
                status_code=self.error_dict["ERROR_UNIDENTIFIED_ERROR"]["code"],
                request_id=self.request_id,
                page_id=self.page_id,
            )

            raise DocAIException(
                action=action,
                message=self.error_dict[
                    "ERROR_UNIDENTIFIED_ERROR"]["text_desc"],
                status_desc=self.error_dict["ERROR_UNIDENTIFIED_ERROR"]["desc"],
                status_code=self.error_dict["ERROR_UNIDENTIFIED_ERROR"]["code"],
            ) from error
