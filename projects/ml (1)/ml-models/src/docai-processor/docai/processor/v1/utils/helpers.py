# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

# (TODO): deepak.sen@quantiphi.com - request per minute is more 120.

"""Can be used to access custom document classification and Custom
document extraction model and get predictions"""

from google.cloud import documentai_v1 as documentai
from qdocai.logger import QDocLogger
from qdocai.utils import DocAIBase, DocAIException
import traceback
import sys
import proto
import json
from typing import List
from typing import Tuple
from docai.processor.v1.utils import post_processing
from docai.processor.v1.utils import error_code

ACTION = "Image Bytes Processing from DocAI Processor"


class OnlinePred(DocAIBase):
    """
    OnlinePred is used to predict using Doc-AI Custom Processor model

    Attributes:
        project: name of GCP project
        endpoint_id: endpoint_id of the doc-ai cdc/cde processor
        location: location where processor is deployed(ex: "asia-south1")
        request_id: This request id is used to track
        the complete request.
        page_id: The page no is represented as page_id

    """

    def __init__(
        self,
        project: str,
        endpoint_id: str,
        location: str,
        request_id: str,
        page_id: str,
        version_id: str = "",
    ) -> None:
        """Inits OnlinePred with attributes."""

        self.project_id = project
        self.processor_id = endpoint_id
        self.location = location
        self.logger = QDocLogger()
        self.ml_package = "docai-processor"
        self.error_dict = error_code.Errors.error_codes
        self.version_id = version_id

        super().__init__(request_id, page_id)

    def predict(self, image_bytes: str):
        """
        OnlinePred is used to predict using Doc-AI Custom Document
        Classification/Extraction Processor model

        Attributes:
            image_bytes: Jpeg image in bytes data

        Returns:
            Predictions: (Pre-defined predictions from DOCAI Processor)
            output_json: output json file
        """
        try:
            # Doc-AI processor default endpoint
            opts = {
                "api_endpoint": f"{self.location}-documentai.googleapis.com"
            }
            client = documentai.DocumentProcessorServiceClient(
                client_options=opts
            )
            proj_loc = f"projects/{self.project_id}/locations/{self.location}"
            if len(self.version_id) > 1:
                name = f"{proj_loc}/processors/{self.processor_id}/processorVersions/{self.version_id}" #pylint: disable=line-too-long
            else:
                name = f"{proj_loc}/processors/{self.processor_id}"

            # Image file content
            document = {"content": image_bytes, "mime_type": "image/jpeg"}

            # Configure the process request
            request = {"name": name, "raw_document": document}

            # send request to doc-ai CDC
            try:
                output = client.process_document(request)
            except Exception as error:
                exc_type, exc_value, exc_tb = sys.exc_info()
                trace_back = traceback.TracebackException(
                    exc_type, exc_value, exc_tb
                )
                error_msg = self.error_dict["ERROR_CLIENT_CONNECTION_FAILED"][
                    "text_desc"
                ]

                self.logger.ml_logger(
                    level="ERROR",
                    ml_package=self.ml_package,
                    message=f"{error_msg} - {trace_back}",
                    action=ACTION,
                    status_code=self.error_dict[
                        "ERROR_CLIENT_CONNECTION_FAILED"
                    ]["code"],
                    request_id=self.request_id,
                    page_id=self.page_id,
                )

                raise DocAIException(
                    action=ACTION,
                    message=self.error_dict["ERROR_CLIENT_CONNECTION_FAILED"][
                        "text_desc"
                    ],
                    status_desc=self.error_dict[
                        "ERROR_CLIENT_CONNECTION_FAILED"
                    ]["desc"],
                    status_code=self.error_dict[
                        "ERROR_CLIENT_CONNECTION_FAILED"
                    ]["code"],
                ) from error

            try:
                predictions = output.document.entities
                output_json = json.loads(proto.Message.to_json(output.document))
            except Exception as error:
                exc_type, exc_value, exc_tb = sys.exc_info()
                trace_back = traceback.TracebackException(
                    exc_type, exc_value, exc_tb
                )
                error_msg = self.error_dict["ERROR_BAD_RESPONSE"]["text_desc"]

                self.logger.ml_logger(
                    level="ERROR",
                    ml_package=self.ml_package,
                    message=f"{error_msg} - {trace_back}",
                    action=ACTION,
                    status_code=self.error_dict["ERROR_BAD_RESPONSE"]["code"],
                    request_id=self.request_id,
                    page_id=self.page_id,
                )

                raise DocAIException(
                    action=ACTION,
                    message=self.error_dict["ERROR_BAD_RESPONSE"]["text_desc"],
                    status_desc=self.error_dict["ERROR_BAD_RESPONSE"]["desc"],
                    status_code=self.error_dict["ERROR_BAD_RESPONSE"]["code"],
                ) from error

            self.logger.ml_logger(
                level="INFO",
                ml_package=self.ml_package,
                action=ACTION,
                status_code=200,
                request_id=self.request_id,
                page_id=self.page_id,
            )
            return predictions, output_json

        except Exception as error:
            exc_type, exc_value, exc_tb = sys.exc_info()
            trace_back = traceback.TracebackException(
                exc_type, exc_value, exc_tb
            )
            error_msg = self.error_dict["ERROR_BAD_PARAMS"]["text_desc"]
            self.logger.ml_logger(
                level="ERROR",
                ml_package=self.ml_package,
                action=ACTION,
                message=f"{error_msg} - {trace_back}",
                status_code=self.error_dict["ERROR_BAD_PARAMS"]["code"],
                request_id=self.request_id,
                page_id=self.page_id,
            )

            raise DocAIException(
                action=ACTION,
                message=self.error_dict["ERROR_BAD_PARAMS"]["text_desc"],
                status_desc=self.error_dict["ERROR_BAD_PARAMS"]["desc"],
                status_code=self.error_dict["ERROR_BAD_PARAMS"]["code"],
            ) from error

    def predict_cdc(self, image_bytes: str) -> Tuple[str, str, dict]:
        """
        Prediction from Document classifier.

        Args:
            image_bytes: Jpeg image in bytes data
        Returns:
            class_type: type of class
            confidence: confidence score
            output_json: output json
        """
        try:
            predictions, output_json = self.predict(image_bytes)
            type_list = []
            confidence_list = []
            for pred in predictions:
                type_list.append(pred.type_)
                confidence_list.append(pred.confidence)
            if len(confidence_list) == 0 and len(type_list) == 0:

                self.logger.ml_logger(
                    level="ERROR",
                    ml_package=self.ml_package,
                    message=self.error_dict["ERROR_NULL_RESPONSE"]["text_desc"],
                    action=ACTION,
                    status_code=self.error_dict["ERROR_NULL_RESPONSE"]["code"],
                    request_id=self.request_id,
                    page_id=self.page_id,
                )

                raise DocAIException(
                    action=ACTION,
                    message=self.error_dict["ERROR_NULL_RESPONSE"]["text_desc"],
                    status_desc=self.error_dict["ERROR_NULL_RESPONSE"]["desc"],
                    status_code=self.error_dict["ERROR_NULL_RESPONSE"]["code"],
                )

            confidence, idx = max((v, i) for i, v in enumerate(confidence_list))
            class_type = type_list[idx]
            return class_type, confidence, output_json

        except Exception as error:
            exc_type, exc_value, exc_tb = sys.exc_info()
            trace_back = traceback.TracebackException(
                exc_type, exc_value, exc_tb
            )
            error_msg = self.error_dict["ERROR_CDC_OUTPUT"]["text_desc"]

            self.logger.ml_logger(
                level="ERROR",
                ml_package=self.ml_package,
                message=f"{error_msg} - {trace_back}",
                action=ACTION,
                status_code=self.error_dict["ERROR_CDC_OUTPUT"]["code"],
                request_id=self.request_id,
                page_id=self.page_id,
            )

            raise DocAIException(
                action=ACTION,
                message=self.error_dict["ERROR_CDC_OUTPUT"]["text_desc"],
                status_desc=self.error_dict["ERROR_CDC_OUTPUT"]["desc"],
                status_code=self.error_dict["ERROR_CDC_OUTPUT"]["code"],
            ) from error

    def predict_cde(self, output_json: dict, doc_type: str) -> List:
        """
        Prediction from Document Parsers.

        Args:
            output_json: output json
            doc_type: document type
        Returns:
            output_list: output list of entitiess

        """
        try:
            opts = {
                "api_endpoint": f"{self.location}-documentai.googleapis.com"
            }
            client = documentai.DocumentProcessorServiceClient(
                client_options=opts
            )
            proj_loc = f"projects/{self.project_id}/locations/{self.location}"
            name = f"{proj_loc}/processors/{self.processor_id}"

            # Configure the process request
            out_document = documentai.types.Document.from_json(
                json.dumps(output_json)
            )
            request = {"name": name, "inline_document": out_document}
            output = client.process_document(request)
            predictions = output.document.entities
            temp_dict = {}
            output_list = []
            try:
                for pred in predictions:
                    temp_dict = {}
                    temp_dict["key"] = pred.type_
                    temp_dict["value"] = pred.mention_text
                    temp_dict["confidence"] = pred.confidence
                    output_list.append(temp_dict)

                post_process_obj = post_processing.PostProcessing()
                output_list = post_process_obj.post_process_entities(
                    doc_type=doc_type, cde_response=output_list
                )
            except Exception as error:
                exc_type, exc_value, exc_tb = sys.exc_info()
                trace_back = traceback.TracebackException(
                    exc_type, exc_value, exc_tb
                )
                error_msg = self.error_dict["ERROR_CDE_OUTPUT"]["text_desc"]
                self.logger.ml_logger(
                    level="ERROR",
                    ml_package=self.ml_package,
                    message=f"{error_msg} - {trace_back}",
                    action=ACTION,
                    status_code=self.error_dict["ERROR_CDE_OUTPUT"]["code"],
                    request_id=self.request_id,
                    page_id=self.page_id,
                )

                raise DocAIException(
                    action=ACTION,
                    message=self.error_dict["ERROR_CDE_OUTPUT"]["text_desc"],
                    status_desc=self.error_dict["ERROR_CDE_OUTPUT"]["desc"],
                    status_code=self.error_dict["ERROR_CDE_OUTPUT"]["code"],
                ) from error
            return output_list

        except Exception as error:
            exc_type, exc_value, exc_tb = sys.exc_info()
            trace_back = traceback.TracebackException(
                exc_type, exc_value, exc_tb
            )
            error_msg = self.error_dict["ERROR_CDE_REQUEST_FAILED"]["text_desc"]

            self.logger.ml_logger(
                level="ERROR",
                ml_package=self.ml_package,
                message=f"{error_msg} - {trace_back}",
                action=ACTION,
                status_code=self.error_dict["ERROR_CDE_REQUEST_FAILED"]["code"],
                request_id=self.request_id,
                page_id=self.page_id,
            )

            raise DocAIException(
                action=ACTION,
                message=self.error_dict["ERROR_CDE_REQUEST_FAILED"][
                    "text_desc"
                ],
                status_desc=self.error_dict["ERROR_CDE_REQUEST_FAILED"]["desc"],
                status_code=self.error_dict["ERROR_CDE_REQUEST_FAILED"]["code"],
            ) from error

    def mlops_predict_cde(self, image_bytes: str, doc_type: str) -> List:
        """
        Prediction from Document Parsers.

        Args:
            output_json: output json
            doc_type: document type
        Returns:
            output_list: output list of entitiess

        """
        try:
            predictions, _ = self.predict(image_bytes)
            temp_dict = {}
            output_list = []
            try:
                for pred in predictions:
                    temp_dict = {}
                    temp_dict["key"] = pred.type_
                    temp_dict["value"] = pred.mention_text
                    temp_dict["confidence"] = pred.confidence
                    output_list.append(temp_dict)

                post_process_obj = post_processing.PostProcessing()
                output_list = post_process_obj.post_process_entities(
                    doc_type=doc_type, cde_response=output_list
                )
            except Exception as error:
                exc_type, exc_value, exc_tb = sys.exc_info()
                trace_back = traceback.TracebackException(
                    exc_type, exc_value, exc_tb
                )
                error_msg = self.error_dict["ERROR_CDE_OUTPUT"]["text_desc"]
                self.logger.ml_logger(
                    level="ERROR",
                    ml_package=self.ml_package,
                    message=f"{error_msg} - {trace_back}",
                    action=ACTION,
                    status_code=self.error_dict["ERROR_CDE_OUTPUT"]["code"],
                    request_id=self.request_id,
                    page_id=self.page_id,
                )

                raise DocAIException(
                    action=ACTION,
                    message=self.error_dict["ERROR_CDE_OUTPUT"]["text_desc"],
                    status_desc=self.error_dict["ERROR_CDE_OUTPUT"]["desc"],
                    status_code=self.error_dict["ERROR_CDE_OUTPUT"]["code"],
                ) from error
            return output_list

        except Exception as error:
            exc_type, exc_value, exc_tb = sys.exc_info()
            trace_back = traceback.TracebackException(
                exc_type, exc_value, exc_tb
            )
            error_msg = self.error_dict["ERROR_CDE_REQUEST_FAILED"]["text_desc"]

            self.logger.ml_logger(
                level="ERROR",
                ml_package=self.ml_package,
                message=f"{error_msg} - {trace_back}",
                action=ACTION,
                status_code=self.error_dict["ERROR_CDE_REQUEST_FAILED"]["code"],
                request_id=self.request_id,
                page_id=self.page_id,
            )

            raise DocAIException(
                action=ACTION,
                message=self.error_dict["ERROR_CDE_REQUEST_FAILED"][
                    "text_desc"
                ],
                status_desc=self.error_dict["ERROR_CDE_REQUEST_FAILED"]["desc"],
                status_code=self.error_dict["ERROR_CDE_REQUEST_FAILED"]["code"],
            ) from error
