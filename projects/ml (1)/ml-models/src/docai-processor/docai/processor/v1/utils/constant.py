# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

"""Constants that are used in all parsers"""


class Constant:
    regex = {
        "dob": r"(?:[0-9]{2}(?:/|-)){2}[0-9]{4}",
        "issue_date": r"(?:[0-9]{2}(?:/|-)){2}[0-9]{4}",
        "validity_date": r"(?:[0-9]{2}(?:/|-)){2}[0-9]{4}",
        "expiry_date": r"(?:[0-9]{2}(?:/|-)){2}[0-9]{4}",
        "voter_id": r"[A-Z]{3}[0-9]{7}",
        "passport_id": r"[a-zA-Z][0-9]{7}",
        "pan_id": r"[A-Z]{4,5}\d{4,5}[A-Z]{1}",
        "aadhaar_no": r"[0-9]{4}[^\S\r\n][0-9]{4}[^\S\r\n][0-9]{4}",
        "blood_group": r"(?:AB|A|B|O)[-+]\s",
    }

    address_keywords = ["Address"]
    dl_address_keywords = ["Add :", "Add:", "Add", "PIN :", "PIN:", "PIN"]
    relation_name_keywords = [
        "Fathers Name",
        "Mothers Name",
        "Husbands Name",
        "Relations Name",
    ]
