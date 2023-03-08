# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# ==============================================================================

"""This module will predict the location of bounding boxes"""

import tensorflow as tf
import base64
import gcsfs
from typing import Dict, Tuple
from scf_constants import Constants
import traceback
from custlogger import ml_logger
fs = gcsfs.GCSFileSystem()


class Prediction:
    """
    class Prediction will preform inference in images

    Args:
            model_path: str
                gcs path of model
            threshold: float
                minimum threshold for detection
    """
    def __init__(self, model_path: str, threshold: float):
        """Initiates Prediction with args"""
        self.vertex_model = tf.saved_model.load(model_path)
        self.threshold = threshold

    def preprocess(self, bytes_inputs: bytes, input_size: Tuple):
        """
        preform preprocessing in input image
        Args:
            bytes_inputs: bytes
                input image as bytes array for inference
            input_size: Tuple
                required image size
        Returns:
            uint8:
                resized image
        """
        decoded = tf.io.decode_jpeg(bytes_inputs, channels=3)
        resized = tf.image.resize(decoded, size=input_size)
        return tf.cast(resized, dtype=tf.uint8)

    def encode_image(self, image: bytes) -> str:
        """
        preform encoding in input image
        Args:
            image: bytes
                input image for inference
        Returns:
            str:
                encoded string
        """
        encoded_string = base64.urlsafe_b64encode(image).decode("utf-8")
        return encoded_string

    def test_model_bytes(self, img_bytes: bytes, input_size: Tuple) -> Dict:
        """
        object detetction classwise prediction
        Args:
            img_bytes: bytes
                input image for inference
            input_size: Tuple
                size of image
        Returns:
            refined_result: dictionary of class and bounding box
        """
        try:
            ml_logger(type_log="INFO", component="Custom OD-Evaluation",
                      message="Prediction started", status_code="200")
            results = self.vertex_model(
                [self.preprocess(tf.io.decode_base64(
                    self.encode_image(img_bytes)), input_size)])
            refined_result = self.format_tf_od_predictions(
                results, self.threshold)
            ml_logger(type_log="INFO", component="Custom OD-Evaluation",
                      message="Prediction Completed", status_code="200")
            return refined_result
        except Exception:
            ml_logger(type_log="ERROR", component="Custom OD-Evaluation",
                      message="exception in test_model_bytes",
                      status_code="500", traceback=traceback.format_exc())
            raise

    def format_tf_od_predictions(
            self, output_dict: Dict, threshold: float) -> Dict:
        """
        object detetction classwise prediction
        Args:
            output_dict: Dict
                object detetction dictionary
            threshold: float
                threshold for prediction
        Returns:
            detections: dictionary of class and bounding box
        """
        try:
            predictions = [
                output_dict["detection_boxes"].numpy().tolist()[0],
                output_dict["detection_scores"].numpy().tolist()[0],
                output_dict["detection_classes"].numpy().tolist()[0],
                output_dict["num_detections"].numpy().tolist()[0]]
            (boxes, scores, classes, num_detections) = predictions
            display_labels = []
            bboxes = []
            confidence_scores = []
            for i in range(int(num_detections)):
                score = scores[i]
                if score >= threshold:
                    obj_class = Constants.idx2label.get(
                        int(classes[i]), "other")
                    confidence_scores.append(score)
                    y1, x1, y2, x2 = boxes[i]
                    display_labels.append(obj_class)
                    bboxes.append([x1, x2, y1, y2])
            detections = {"displayNames": display_labels, "bboxes": bboxes,
                          "confidence": confidence_scores}
            return detections
        except Exception:
            ml_logger(type_log="ERROR", component="Custom OD-Evaluation",
                      message="exception in format_tf_od_predictions",
                      status_code="500", traceback=traceback.format_exc())
            raise
