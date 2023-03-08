# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

"""Error codes for docai-fuzzymatch"""


class Errors:
    error_codes = {
        "ERROR_DATE_FORMAT": {
            "code": "1501",
            "desc": "INVALID_DATE_FORMAT",
            "text_desc": "Input date is not in format dd/mm/yyyy",
        },
        "ERROR_ADDRESS_MATCH": {
            "code": "1502",
            "desc": "ERROR_IN_ADDRESS_MATCH",
            "text_desc": "Error or Exception occured during address match",
        },
        "ERROR_NAME_MATCH": {
            "code": "1503",
            "desc": "ERROR_IN_NAME_MATCH",
            "text_desc": "Error or Exception occured during name match",
        },
    }
