# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.


class Errors:
    error_codes = {
        "ERROR_KEYWORD_EXTRACTION_ROI_FAILED": {
            "code": "1401",
            "desc": "PROCESSING_FAILED",
            "text_desc": "keyoword extraction failed",
        },
        "ERROR_KEYWORD_EXTRACTION_STATICWORD_FAILED": {
            "code": "1402",
            "desc": "PROCESSING_FAILED",
            "text_desc": "keyoword extraction of applicant failed",
        },
        "ERROR_SIGNATURE_COUNT_FAILED": {
            "code": "1403",
            "desc": "SIGNATURE_COUNT_FAILED",
            "text_desc": "extraction for count of signature failed",
        },
        "ERROR_EXTRACTION_FAILED": {
            "code": "1404",
            "desc": "EXTRACTION_FAILED",
            "text_desc": "extract function failed",
        },
        "ERROR_TFOD_PREDICTION": {
            "code": "1405",
            "desc": "PREDICTION_FAILED",
            "text_desc": "prediction failed",
        },
        "ERROR_FORMATED_TFOD_PREDICTION": {
            "code": "1406",
            "desc": "FORMAT_TFOD_FAILED",
            "text_desc": "formated tfod failed",
        },
        "ERROR_CLEANING_OCR": {
            "code": "1407",
            "desc": "CLEANING_OCR_FAILED",
            "text_desc": "cdc ocr cleaning falied",
        },
        "ERROR_OCR_WRAP": {
            "code": "1408",
            "desc": "OCR_WRAP_FAILED",
            "text_desc": "cdc ocr extract falied",
        },
        "ERROR_RESIZED_IMAGE": {
            "code": "1409",
            "desc": "RESIZED_IMAGE_FAILED",
            "text_desc": "resized image falied",
        },
        "ERROR_BOUNDING_BOX_EXTRACTION": {
            "code": "1410",
            "desc": "BOUNDING_BOX_EXTRACTION_FAILED",
            "text_desc": "bounding box extraction failed",
        },
        "ERROR_EXTRACTION_WORD_CORD": {
            "code": "1411",
            "desc": "EXTRACTION_WORD_CORD_FAILED",
            "text_desc": "static word co-ordinate failed",
        },
        "ERROR_COMBINE_WORD_EXTRACTION_FAILED": {
            "code": "1412",
            "desc": "COMBINE_WORD_EXTRACTION_FAILED",
            "text_desc": "combine static word co-ordinates failed",
        },
        "ERROR_EXTRACTION_WORD_ROI_FAILED": {
            "code": "1413",
            "desc": "EXTRACTION_WORD_ROI_FAILED",
            "text_desc": "extract_word_roi_coordinates failed",
        },
        "ERROR_COMBINE_WORD_ROI_FAILED": {
            "code": "1414",
            "desc": "COMBINE_WORD_ROI_FAILED",
            "text_desc": "extract_combined_word_roi_coordinates failed",
        },
        "ERROR_MID_POINT_EXTRACTION_FAILED": {
            "code": "1415",
            "desc": "MID_POINT_EXTRACTION_FAILED",
            "text_desc": "mid point extraction failed",
        },
        "ERROR_LEFT_MID_POINT_FAILED": {
            "code": "1416",
            "desc": "LEFT_MID_POINT_FAILED",
            "text_desc": "left mid point extraction failed",
        },
        "ERROR_NGRAM_FAILED": {
            "code": "1417",
            "desc": "NGRAM_FAILED",
            "text_desc": "ngram failed",
        },
        "ERROR_EUCLIDEAN_DISTANCE_FAILED": {
            "code": "1420",
            "desc": "EUCLIDEAN_DISTANCE_FAILED",
            "text_desc": "Euclidean distance failed",
        },
        "ERROR_FUZZY_MATCH_FAILED": {
            "code": "1419",
            "desc": "FUZZY_MATCH_FAILED",
            "text_desc": "fuzzy match failed",
        },
    }
