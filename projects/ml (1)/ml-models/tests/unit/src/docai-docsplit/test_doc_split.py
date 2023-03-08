# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

"""Testing DocSplitting and download, upload files with
extention validation"""

import unittest
from docai.docsplit.v1.utils import helpers


class VarPath:
    """Used for defining path of test files"""

    def __init__(self) -> None:
        self.path = "./tests/unit/src/docai-docsplit/test_data/"
        self.sample_png = f"{self.path}sample.png"
        self.sample_pdf = f"{self.path}SSRN-id3928966.pdf"
        self.sample_tif = f"{self.path}multipage_tif_example.tif"


class TestDocSplit(unittest.TestCase,
                   helpers.Helper, helpers.Splitter, VarPath):
    """Testing Helper, Splitter"""

    def __init__(self, *args, **kwargs) -> None:
        """testing Helper class methods"""
        super().__init__(*args, **kwargs)
        self.download_bucket_name = ""
        self.gcs_download_filepath = ""
        self.num_pdf_pages = 59
        self.num_tiff_pages = 10

        helpers.Helper.__init__(
            self,
            self.download_bucket_name,
            self.gcs_download_filepath,
            "12345678",
            "878787878",
        )
        helpers.Splitter.__init__(self, "", "12345678", "878787878")
        VarPath.__init__(self)

    @staticmethod
    def read_file(path: str) -> bytes:
        """reading file from config with key_name"""
        with open(path, "rb") as f:
            file_bytes = f.read()
        f.close()
        return file_bytes

    def test_validate(self) -> None:
        """validating file extention"""
        file_bytes = self.read_file(self.sample_png)
        _, file_ext = self.validate_file(file_bytes)
        self.assertEqual("png", file_ext)

    def test_pdf_split_bytes(self) -> None:
        """testing pdf split"""
        self.bytes_data = self.read_file(self.sample_pdf)
        list_img, _ = self._pdf_split_bytes()
        self.assertEqual(list, type(list_img))
        self.assertEqual(self.num_pdf_pages, len(list_img))

    def test_tiff_split_bytes(self) -> None:
        """testing tiff split"""
        self.bytes_data = self.read_file(self.sample_tif)
        list_img, _ = self._tiff_split_bytes()
        self.assertEqual(list, type(list_img))
        self.assertEqual(self.num_tiff_pages, len(list_img))

    def test_convert_png_bytes(self) -> None:
        """testing conversion of png to jpg"""
        self.bytes_data = self.read_file(self.sample_png)
        result, _ = self._convert_png_bytes()
        self.assertEqual(bytes, type(result))
