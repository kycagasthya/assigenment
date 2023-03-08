# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

"""Error codes for docai-processor"""


class Errors:
    error_codes = {
        "ERROR_DESKEW_FAILED": {
            "code": "1201",
            "desc": "DESKEW_FAILED",
            "text_desc": "Deskew Failed",
        },
        "ERROR_PREPROCESSING_FAILED": {
            "code": "1202",
            "desc": "PREPROCESSING_FAILED",
            "text_desc": "Bad Image/Process Failed",
        },
        "ERROR_NO_DPI": {
            "code": "1203",
            "desc": "NO_DPI_FOUND",
            "text_desc": "DPI value not Found",
        },
        "ERROR_PIXEL_CALCULATION_FAILED": {
            "code": "1204",
            "desc": "PIXEL_CALCULATION_FAILED",
            "text_desc": "Pixel Calculation Failed",
        },
    }
