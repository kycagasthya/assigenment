# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

"""Error codes for docai-processor"""


class Errors:
    error_codes = {
        "ERROR_CLIENT_CONNECTION_FAILED": {
            "code": "1301",
            "desc": "PROCESSING_FAILED",
            "text_desc": "Document AI Client connection failed",
        },
        "ERROR_BAD_RESPONSE": {
            "code": "1302",
            "desc": "PROCESSING_FAILED",
            "text_desc": "Bad response from Document AI Processor",
        },
        "ERROR_BAD_PARAMS": {
            "code": "1303",
            "desc": "PROCESSING_FAILED",
            "text_desc": "Wrong/Bad parameters for Document AI Processor",
        },
        "ERROR_NULL_RESPONSE": {
            "code": "1304",
            "desc": "PROCESSING_FAILED",
            "text_desc": "CDC - Null response from Document AI Processor",
        },
        "ERROR_CDC_OUTPUT": {
            "code": "1305",
            "desc": "PROCESSING_FAILED",
            "text_desc": "CDC - Error in output",
        },
        "ERROR_CDE_OUTPUT": {
            "code": "1306",
            "desc": "PROCESSING_FAILED",
            "text_desc": "CDE - Error in output",
        },
        "ERROR_CDE_REQUEST_FAILED": {
            "code": "1307",
            "desc": "PROCESSING_FAILED",
            "text_desc": "CDE - Request Failed",
        },
    }
