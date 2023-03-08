# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

"""std preproc"""
import sys
import unittest
import time
from unittest.mock import patch
from glob import glob
from os.path import dirname, abspath
sys.path.insert(0, "src/mlops_composer/standard_preprocessing")
from std_preproc import StandardPreprocessing
current_dir = abspath(dirname(__file__))

class TestStdPreproc(unittest.TestCase):
    """unittest std preproc"""
    def setUp(self):
        """setup function"""
        self.stdpreproc = StandardPreprocessing()

    @patch("std_preproc.gcsfs.GCSFileSystem")
    def test_process(self, mock_gcs_file):
        """ test process"""
        mock_gcs_file().glob.return_value = glob(
            f"{current_dir}/test_data/test_img.jpg")
        with open(f"{current_dir}/test_data/test_img.jpg", "rb") as test_img:

            mock_gcs_file().open.return_value = test_img
            self.assertEqual(
                self.stdpreproc.process(
                    src_path=f"{current_dir}/test_data/test_img.jpg",
                    dest_path=f"{current_dir}/test_data",
                    timestamp=time.time(),
                ),
                None,
            )

    def test_get_dpi(self):
        """check dpi"""
        with open(f"{current_dir}/test_data/test_img.jpg", "rb") as image:
            read_img = image.read()
            i_m = bytearray(read_img)

        self.assertEqual(self.stdpreproc.get_dpi(img=i_m), None)

    def test_check_min_resolution(self):
        """check min resolution"""
        with open(f"{current_dir}/test_data/test_img.jpg", "rb") as image:
            read_img = image.read()
            i_m = bytearray(read_img)
        self.assertEqual(
            self.stdpreproc.check_min_resolution(
                img=i_m, min_width=200, min_height=200
            ),
            True,
        )
