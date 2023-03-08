# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

"""Constants that are used in fuzzy name and address logic files"""


class Constant:
    """
    REPLACE_LIST_NAME_EXTRAS_WITH_PARANTHESIS: remove special
    words with  brackets such as (MINOR)and (HUF) from names

    REPLACE_LIST_NAME_EXTRAS_NO_PARANTHESIS: remove special
    words with no  brackets such as MINOR and HUF from names

    REPLACE_LIST_ADDRESS : remove special words such Post,c/o
    from address while doing text cleaning

    NAME_SUB_STRING : used in name match text cleaning ,will
    remove words such MRand DR

    """
    REPLACE_LIST_NAME_EXTRAS_WITH_PARANTHESIS = [
        "(MINOR)",
        "(HUF)",
        "(JT1)",
        "(JT2)",
        ".(MINOR)",
        ".(HUF)",
        ".(JT1)",
        ".(JT2)",
    ]
    REPLACE_LIST_NAME_EXTRAS_NO_PARANTHESIS = [
        "MINOR", "HUF", "JT1", "JT2", ".MINOR", ".HUF", ".JT1", ".JT2"]
    REPLACE_LIST_ADDRESS = [
        "PO-",
        "(PO)",
        "ROAD",
        "STREET NO",
        "RD",
        "MARG",
        "LANE",
        "NEAR",
        "BESIDE",
        "OPP",
        "OPPOSITE",
        "BEHIND",
        "ENCLAVE",
        "TOWNSHIP",
        "SOCIETY",
        "TOWERS",
        "BLOCK",
        "S/O",
        "C/O",
        "D/O",
        "W/O",
    ]
    NAME_SUB_STRING = r""" ^mr[\s\n\t\.]+|^dr[\s\n\t\.]+|^ca[\s\n\t\.]|
                         ^mohd[\s\n\t\.]+|^md[\s\n\t\.]+|^mr[\s\n\t\.]+|
                         ^mrs[\s\n\t\.]+|^sri[\s\n\t\.]+|^smt[\s\n\t\.]+|
                         ^major[\s\n\t\.]+|^lt[\s\n\t\.]+|^capt[\s\n\t\.]+|
                         ^mas[\s\n\t\.]+|^ms[\s\n\t\.]+|^m\/s[\s\n\t\.]"""
    DATE_FMT = "%d/%m/%Y"
    COUNTRIES = ["INDIA"]
    SHORTHANDS_PATH = r"shorthands.json"
    STATES_CITIES_PATH = r"state_cities.json"
    FUZZY_MATCH_THRESH = 0.90
    HNO_WEIGHT = 0.0
    PIN_WEIGHT = 0.0
    ADDRESS_WEIGHT = 1.0
