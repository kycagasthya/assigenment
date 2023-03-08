# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

"""Testing ImageOperation"""

import unittest
import numpy as np
from docai.preproc.v1.utils import helpers


class VarPath:
    """Used for defining path of test files"""

    def __init__(self) -> None:
        file_name = "Rajasthan_TC001.png"
        self.path = f"./tests/unit/src/docai-preproc/test_data/{file_name}"
        with open(self.path, "rb") as f:
            self.file_bytes = f.read()


class Test(unittest.TestCase, VarPath):
    """Testing ImageOperation"""

    def __init__(self, *args, **kwargs) -> None:
        """initiating class"""
        super().__init__(*args, **kwargs)
        VarPath.__init__(self)
        self.r = "12345678"
        self.p = "878787878"
        self.operations = helpers.ImageOperation(
            file_bytes=self.file_bytes, request_id=self.r, page_id=self.p
        )

    def test_preprocess_bytes(self) -> None:
        """testing pre_process method"""
        content, _, _ = self.operations.preprocess_bytes(
            gray_scale_flag=True, deskew_scale_flag=True
        )
        arr = np.asarray(bytearray(content))
        self.assertEqual(bytes, type(content))
        self.assertEqual(arr.shape, (374554,))

    def test_get_dpi(self) -> None:
        """testing get_dpi method"""
        dpi_value = self.operations.get_dpi()
        self.assertEqual(None, dpi_value)

    def test_check_min_resolution(self) -> None:
        """testing check_min_resolution method"""
        pixel_flag = self.operations.check_min_resolution()
        self.assertEqual(True, pixel_flag)

