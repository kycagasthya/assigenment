from datetime import datetime
import json
import os
from typing import Any, Dict, List, Optional, Union


# JSON schema attributes
FIELDS_COL = "fields"
NAME_COL = "name"
TYPE_COL = "type"
MODE_COL = "mode"
DESC_COL = "description"
POLICY_TAGS_COL = "policyTags"
NAMES_COL = "names"
PUBSUB_MODE_COL = "pubsub_mode"

_BQ_JSON_COLS = [
    NAME_COL,
    TYPE_COL,
    MODE_COL,
    DESC_COL,
    FIELDS_COL,
    POLICY_TAGS_COL,
    NAMES_COL,
]
BQ_JSON_COLS = [col.lower() for col in _BQ_JSON_COLS]

_BQ_NON_UPDATABLE_COLS = [NAME_COL, TYPE_COL, MODE_COL, FIELDS_COL]
BQ_NON_UPDATABLE_COLS = [col.lower() for col in _BQ_NON_UPDATABLE_COLS]

_BQ_CORE_COLS = [NAME_COL, TYPE_COL, MODE_COL]
BQ_CORE_COLS = [col.lower() for col in _BQ_CORE_COLS]

# modes
NULLABLE_MODE = "nullable"
REQUIRED_MODE = "required"
REPEATED_MODE = "repeated"
OPTIONAL_MODE = "optional"

DATE_TIME_FMT = "%Y%m%d_%H%M%S"
EXTENSION = ".json"


def find_key(key: str, d: dict) -> str:
    """
    Case-insensitive key search

    :param key:
    :param d:
    :return: original key from "d" dictionary
    """
    for d_key in d:
        if key.lower() == d_key.lower():
            return d_key

    raise Exception(f"Key '{key}' not found")


def _normalize_key(key: str) -> str:
    """
    Get standardized BQ schema key name

    :param key:
    :return: normalized key name or original key if not found
    """
    for bq_key in _BQ_JSON_COLS:
        if bq_key.lower() == key.lower():
            return bq_key

    return key


def normalize(item: Any) -> Any:
    """
    Normalize key names in "item"

    :param item:
    :return:
    """
    if isinstance(item, dict):
        return {_normalize_key(key): normalize(value) for key, value in item.items()}
    elif isinstance(item, list):
        return [normalize(it) for it in item]
    else:
        return item


def get_latest_file(path: str) -> Optional[str]:
    """
    Get latest schema file name

    :param path: directory with schema files
    :return: latest file name
    """
    if os.path.exists(path):
        files = [
            f
            for f in os.listdir(path)
            if os.path.isfile(os.path.join(path, f)) and f.endswith(EXTENSION)
        ]
        sorted_files = sorted(files, key=get_datetime, reverse=True)
        latest_file = os.path.join(path, sorted_files[0]) if sorted_files else None

        return latest_file
    else:
        return None


def get_datetime(file_name: str) -> datetime:
    """
    Get datetime from file name

    :param file_name:
    :return: datetime
    """
    datetime_str = file_name[: len(file_name) - len(EXTENSION)]
    return datetime.strptime(datetime_str, DATE_TIME_FMT)


def load_json(path: str) -> Union[Dict, List]:
    """
    Load JSON data from path file

    :param path: file path
    :return: dictionary
    """
    with open(path) as in_file:
        try:
            return json.load(in_file)
        except ValueError:
            raise Exception("file content is not valid JSON")


def cleanup(item: Any, allowed_keys: List[str]) -> Any:
    """
    Remove extra keys from collection (dict, list)

    :param item: collection
    :param allowed_keys:
    :return: cleared collection
    """
    if isinstance(item, dict):
        return {
            key: cleanup(value, allowed_keys)
            for key, value in item.items()
            if key.lower() in allowed_keys
        }
    elif isinstance(item, list):
        return [cleanup(it, allowed_keys) for it in item]
    else:
        return item


def get_fields(item: Any, path: str) -> Any:
    """
    Transform schema to the list of (field_path, field_body)

    :param item:
    :param path: field path
    :return:
    """
    if isinstance(item, dict):
        # create field path
        field_path = path + "/" + item[NAME_COL]
        if FIELDS_COL in item:
            # remove nested fields from field_body and call get_fields for them
            return [
                (field_path, cleanup(item, BQ_CORE_COLS)),
                get_fields(item[FIELDS_COL], field_path),
            ]
        else:
            # tuple (field_path, field_body)
            return field_path, item
    elif isinstance(item, list):
        return [get_fields(field, path) for field in item]


def flatten(container):
    """
    Flatten container

    :param container:
    :return:
    """
    for i in container:
        if isinstance(i, list):
            for j in flatten(i):
                yield j
        else:
            yield i
