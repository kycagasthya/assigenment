# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
from google.cloud import aiplatform
import base64
from typing import Dict
from .scf_constants import Constants
from qdocai.logger import QDocLogger
from qdocai.utils import DocAIBase, DocAIException
from docai.models.stay_connected_v3 import error_code
import sys
import traceback


class Predict(DocAIBase):
    def __init__(
        self,
        request_id: str,
        page_id: int,
        project: str,
        endpoint_id: str,
        location: str,
        threshold: float,
    ):
        self.request_id = request_id
        self.page_id = page_id
        self.endpoint_id = endpoint_id
        self.project = project
        self.api_endpoint = (
            f"projects/{project}/locations/{location}/endpoints/{endpoint_id}"
        )
        self.endpoint = aiplatform.Endpoint(self.api_endpoint)
        self.prediction_threshold = threshold
        self.idx2label = Constants.idx2label
        self.logger = QDocLogger()
        self.error_dict = error_code.Errors.error_codes
        super().__init__(request_id, page_id)

    def prediction(self, file_content: bytes) -> Dict:
        """
        object detetction prediction
        Args:
            file_content: image file
        Returns:
            refined_results: tfod predictions
        Raise:
            Exception
        """
        try:
            serving_input = "bytes_inputs"
            file_content = base64.b64encode(file_content).decode("utf-8")
            instances_list = [{serving_input: {"b64": file_content}}]
            instances = [
                json_format.ParseDict(s, Value()) for s in instances_list
            ]
            results = self.endpoint.predict(instances=instances)
            prediction_results = results.predictions[0]
            refined_results = self.format_tf_od_predictions(
                prediction_results, self.prediction_threshold
            )
            return refined_results
        except Exception as error:
            exc_type, exc_value, exc_tb = sys.exc_info()
            trace_back = traceback.TracebackException(
                exc_type, exc_value, exc_tb
            )
            self.logger.ml_logger(
                level="ERROR",
                ml_package="docai-models-stayconnected",
                action="predication failed",
                status_code=self.error_dict["ERROR_TFOD_PREDICTION"]["code"],
                message=self.error_dict["ERROR_TFOD_PREDICTION"]["text_desc"]
                + trace_back,
                request_id=self.request_id,
                page_id=self.page_id,
            )
            raise DocAIException(
                action="prediction",
                message=self.error_dict["ERROR_TFOD_PREDICTION"]["text_desc"],
                status_desc=self.error_dict["ERROR_TFOD_PREDICTION"]["desc"],
                status_code=self.error_dict["ERROR_TFOD_PREDICTION"]["code"],
            ) from error

    def format_tf_od_predictions(
        self, output_dict: Dict, threshold: float
    ) -> Dict:
        """
        object detetction classwise prediction
        Args:
            output_dict: object detetction dictionary
            threshold: threshold for prediction
        Returns:
            detections: dictionary of class and bounding box
        """
        try:
            predictions = [
                output_dict["detection_boxes"],
                output_dict["detection_scores"],
                output_dict["detection_classes"],
                output_dict["num_detections"],
            ]
            (boxes, scores, classes, num_detections) = predictions
            display_labels = []
            bboxes = []
            detections = {}
            for i in range(int(num_detections)):
                score = scores[i]
                obj_class = self.idx2label.get(int(classes[i]), "other")
                if score >= threshold:
                    y1, x1, y2, x2 = boxes[i]
                    display_labels.append(obj_class)
                    bboxes.append([x1, x2, y1, y2])
            detections = {"displayNames": display_labels, "bboxes": bboxes}
            self.logger.ml_logger(
                level="INFO",
                ml_package="docai-models-stayconnected",
                message=f"Object Detection prediction:{detections}",
                request_id=self.request_id,
                page_id=self.page_id,
            )
            return detections
        except Exception as error:
            exc_type, exc_value, exc_tb = sys.exc_info()
            trace_back = traceback.TracebackException(
                exc_type, exc_value, exc_tb
            )
            self.logger.ml_logger(
                level="ERROR",
                ml_package="docai-models-stayconnected",
                action=f"formated tfod predictions {detections}",
                status_code=self.error_dict["ERROR_FORMATED_TFOD_PREDICTION"][
                    "code"
                ],
                message=self.error_dict["ERROR_FORMATED_TFOD_PREDICTION"][
                    "text_desc"
                ]
                + trace_back,
                request_id=self.request_id,
                page_id=self.page_id,
            )
            raise DocAIException(
                action="format_tf_od_predictions",
                message=self.error_dict["ERROR_FORMATED_TFOD_PREDICTION"][
                    "text_desc"
                ],
                status_desc=self.error_dict["ERROR_FORMATED_TFOD_PREDICTION"][
                    "desc"
                ],
                status_code=self.error_dict["ERROR_FORMATED_TFOD_PREDICTION"][
                    "code"
                ],
            ) from error
