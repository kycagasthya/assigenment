# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

"""Error codes for docai-processor"""


class Errors:
    error_codes = {
        "ERROR_BUCKET_NOT_FOUND": {
            "code": "1101",
            "desc": "DOWNLOADING_FAILED",
            "text_desc": "Bucket Not Found Error",
        },
        "ERROR_DOWNLOAD_FAILED": {
            "code": "1102",
            "desc": "DOWNLOADING_FAILED",
            "text_desc": "File Download Failed",
        },
        "ERROR_BLOB_NOT_FOUND": {
            "code": "1103",
            "desc": "DOWNLOADING_FAILED",
            "text_desc": "Blob not found",
        },
        "ERROR_ATTRIBUTE_ERROR": {
            "code": "1104",
            "desc": "VALIDATION_FAILED",
            "text_desc": "Attribute error",
        },
        "ERROR_INVALID_FILE_TYPE": {
            "code": "1105",
            "desc": "VALIDATION_FAILED",
            "text_desc": "Invalid file type",
        },
        "ERROR_FILE_NOT_FOUND": {
            "code": "1106",
            "desc": "UPLOADING_FAILED",
            "text_desc": "File not found error",
        },
        "ERROR_PDF_SPLITTING_FAILED": {
            "code": "1107",
            "desc": "SPLITTING_FAILED",
            "text_desc": "PDF Splitting Failed",
        },
        "ERROR_TIFF_SPLITTING_FAILED": {
            "code": "1108",
            "desc": "SPLITTING_FAILED",
            "text_desc": "TIFF Splitting Failed",
        },
        "ERROR_CONVERSION_FAILED": {
            "code": "1109",
            "desc": "CONVERSION_FAILED",
            "text_desc": "PDF to JPG Conversion Failed",
        },
        "ERROR_VALUE_ERROR": {
            "code": "1110",
            "desc": "PROCESS_FAILED",
            "text_desc": "Value Error - Process Failed",
        },
        "ERROR_UNIDENTIFIED_ERROR": {
            "code": "1111",
            "desc": "PROCESS_FAILED",
            "text_desc": "Unidentified Error - Process Failed",
        },
    }
