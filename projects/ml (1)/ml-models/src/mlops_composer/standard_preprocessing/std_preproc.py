# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

"""standard Preprocessing"""
import io
import pathlib
import logging
import sys
import traceback
import os
import numpy as np
from PIL import Image
import gcsfs
import google.cloud.logging
import pandas as pd


LG_CLIENT = google.cloud.logging.Client()
CLOUD_LOGGER = LG_CLIENT.logger("Standard-Preprocessing-Pipeline")

LG_HANDLER = LG_CLIENT.get_default_handler()
LOGGER = logging.getLogger("cloudLogger")
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(LG_HANDLER)


class StandardPreprocessing:
    """pre-processing"""

    def process(self, src_path, dest_path, timestamp):

        """
        Process flow
        Args:
            src_path: source path
            dest_path: destination path
            timestamp: time stamp
        Return:
            None
        """
        gcs = gcsfs.GCSFileSystem()
        all_image_list = []
        for file in gcs.glob(str(src_path).rstrip("/")+"/*.*"):
            if file.endswith(
                ".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
                temporary_list = []
                image_id = pathlib.Path(f"gs://{file}").stem
                temporary_list.append(image_id)
                with gcs.open(f"gs://{file}", "rb") as image:
                    image_bytes = image.read()
                check = self.check_min_resolution(image_bytes)
                if self.get_dpi(image_bytes):
                    if self.get_dpi(image_bytes) >= 90 and check is True:
                        all_image_list.append(image_id)
                else:
                    if check is True:
                        all_image_list.append(image_id)

        csv_path = os.path.join(
            dest_path, f"standard_preprocessed_images_{timestamp}.csv"
        )
        dframe = pd.DataFrame(all_image_list, columns=["file_name"])
        dframe.to_csv(csv_path, index=False)

    def get_dpi(self, img) -> float:
        """
        Checks DPI metdata in image and returns it.
        Args:
            img: image
        Returns:
            Float value of DPI.
        Raises:
            KeyError: Value not present.
        """
        try:
            i_m = Image.open(io.BytesIO(img))
            dpi_avg = np.average(i_m.info["dpi"])

            CLOUD_LOGGER.log_text("DPI Average")
            CLOUD_LOGGER.log_struct({"dpi_avg": dpi_avg})
            return dpi_avg

        except KeyError as _:
            exc_type, exc_value, exc_tb = sys.exc_info()
            trace_back = traceback.TracebackException(
                exc_type, exc_value, exc_tb
            )
            _ = "".join(trace_back.format_exception_only())

            return None

    def check_min_resolution(
        self, img, min_width: int = 200, min_height: int = 200
    ) -> bool:
        """
        Checks minimum resolution criteria for the image

        Returns:
            bool if image satisfies the minimum resolution criteria

        Raises:
            UnidentifiedImageError: Image cannot be opened and identified.
        """
        i_m = Image.open(io.BytesIO(img))
        width, height = i_m.size
        if width >= min_width and height >= min_height:
            return True
        return False
