import argparse
from datetime import datetime
import json
import os
from typing import Any, Dict, List

from utils.common import OPTIONAL_COLUMNS
from utils.generation import (
    cleanup,
    find_key,
    flatten,
    get_fields,
    get_latest_file,
    load_json,
    normalize,
    BQ_JSON_COLS,
    BQ_NON_UPDATABLE_COLS,
    FIELDS_COL,
    MODE_COL,
    NAME_COL,
)
from utils.generation import (
    DATE_TIME_FMT,
    EXTENSION,
    NULLABLE_MODE,
    REPEATED_MODE,
    REQUIRED_MODE,
)
from utils.validation import validate_config


MESSAGE_SEPARATOR = "-" * 100


def get_datetime_str() -> str:
    """
    Get date time string

    :return: date time string
    """
    return datetime.now().strftime(DATE_TIME_FMT)


def ordered(obj: Any) -> Any:
    """
    Order object

    :param obj:
    :return: ordered object
    """
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def check_deleted_fields(current_fields: Dict, new_fields: Dict):
    """
    Check if there are deleted fields and throw an exception

    :param current_fields:
    :param new_fields:
    """
    deleted_fields = []
    for path in current_fields:
        if path not in new_fields:
            deleted_fields.append(path)

    if deleted_fields:
        raise Exception(f"Found deleted fields: {deleted_fields}")


def check_modified_fields(current_fields: Dict, new_fields: Dict):
    """
    Check fields modifications are legal and throw an exception

    :param current_fields:
    :param new_fields:
    """
    # missing field's attribute
    missing_attributes = []
    for path, field in current_fields.items():
        for key, value in field.items():
            if key not in new_fields[path]:
                missing_attributes.append(f"field '{path}', attribute '{key}'")

    if missing_attributes:
        raise Exception(f"Found deleted attributes: {missing_attributes}")

    # illegal attribute modification and relax mode
    illegal_modifications = []
    relax_mode_fields = []
    for path, field in current_fields.items():
        for key, value in field.items():
            if value.lower() != new_fields[path][key].lower():
                if (
                    key == MODE_COL
                    and value.lower() == REQUIRED_MODE
                    and new_fields[path][key].lower() == NULLABLE_MODE
                ):
                    relax_mode_fields.append(path)
                else:
                    illegal_modifications.append(
                        f"field '{path}', attribute '{key}': '{value}'->'{new_fields[path][key]}'"
                    )

    if illegal_modifications:
        raise Exception(f"Unsupported modifications: {illegal_modifications}")

    if relax_mode_fields:
        print(
            f"Relaxing field's mode from 'REQUIRED' to 'NULLABLE': {relax_mode_fields}"
        )
        print(MESSAGE_SEPARATOR)


def check_new_fields(current_fields: Dict, new_fields: Dict):
    """
    Check new fields' mode and throw an exception

    :param current_fields:
    :param new_fields:
    """
    illegal_mode_fields = []
    added_fields = []
    for path, field in new_fields.items():
        if path not in current_fields:
            added_fields.append(path)
            if field[MODE_COL].lower() not in [NULLABLE_MODE, REPEATED_MODE]:
                illegal_mode_fields.append(f"field '{path}': {field[MODE_COL]}")

    if illegal_mode_fields:
        raise Exception(f"Bad mode for new fields: {illegal_mode_fields}")

    if added_fields:
        print(f"Adding new fields: {added_fields}")
        print(MESSAGE_SEPARATOR)


def validate_bq_update(current: List[Dict], new: List[Dict]):
    """
    Check changes in "new" schema versus "current" are valid according to BigQuery rules

    :param current: current schema
    :param new: new schema
    """
    # remove updatable columns, i.e. "description", "policyTags", we don't validate them
    current = cleanup(current, BQ_NON_UPDATABLE_COLS)
    new = cleanup(new, BQ_NON_UPDATABLE_COLS)

    # convert schema to {field_path: field_body} dictionary
    current_fields = {path: field for path, field in flatten(get_fields(current, ""))}
    new_fields = {path: field for path, field in flatten(get_fields(new, ""))}

    # check deleted fields
    check_deleted_fields(current_fields, new_fields)

    # check fields modifications
    check_modified_fields(current_fields, new_fields)

    # check new fields' mode
    check_new_fields(current_fields, new_fields)


def add_service_cols(document):
    """
    Add default service columns

    :param document:
    """
    # find columns to add
    col_status = {}
    for optional_col in OPTIONAL_COLUMNS:
        col_status[optional_col[NAME_COL]] = False
        # check each column from the document against a service column
        for col in document[FIELDS_COL]:
            if optional_col[NAME_COL] == col[NAME_COL]:
                col_status[optional_col[NAME_COL]] = True

    col_names_to_add = [key for key, value in col_status.items() if not value]
    cols_to_add = [col for col in OPTIONAL_COLUMNS if col[NAME_COL] in col_names_to_add]

    # add columns to document
    for col in cols_to_add:
        document[FIELDS_COL].append(col)
        print(f"Added default service column to source config: {col}")

    print(MESSAGE_SEPARATOR)


def is_diff(current: List[Dict], new: List[Dict]) -> bool:
    """
    Compare "current" and "new" BQ schemas

    :param current: current schema
    :param new: new schema
    :return: "is different" flag
    """
    if not current and new:
        return True  # the very first schema, "current" is empty
    elif not current and not new:
        return False  # both schemas are empty
    else:
        # compare "new" with non-empty "current"
        if ordered(current) != ordered(new):
            validate_bq_update(
                current, new
            )  # schema has changed, validate changes according to BQ rules
            return True
        else:
            return False  # no changes


def run(in_json_file: str, bq_dir: str = None):
    """
    Generate BQ schema file from JSON source config file,
    source config is first cleared and then validated against the current BQ schema

    :param in_json_file: input config JSON file name, file format must be BigQuery JSON schema like
    :param bq_dir: output dir with BQ schema files
    """
    json_config = load_json(in_json_file)

    # validate input config
    validate_config(json_config)

    # add default service columns
    add_service_cols(json_config)

    # read current schema
    current_schema_file = get_latest_file(bq_dir)
    if current_schema_file:
        print(f"found current schema file '{current_schema_file}'")
        current_schema = load_json(current_schema_file)
    else:
        print("no current schema file found")
        current_schema = []
    print(MESSAGE_SEPARATOR)

    # clear new schema, filter out non-BQ attributes
    new_schema = cleanup(json_config[find_key(FIELDS_COL, json_config)], BQ_JSON_COLS)

    # normalize key names
    new_schema = normalize(new_schema)

    # write new schema to the file if there are any changes
    if is_diff(current_schema, new_schema):
        # new schema file name
        new_schema_file = os.path.join(bq_dir, get_datetime_str() + EXTENSION)

        # write new schema to file
        os.makedirs(os.path.dirname(new_schema_file), exist_ok=True)
        with open(new_schema_file, "w") as f:
            json.dump(new_schema, f, indent=2)

            print(f"generated new schema file '{new_schema_file}'")
    else:
        print("no schema file was generated since there were no changes to the schema")


if __name__ == "__main__":
    # parse input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--in_json", required=True, help="Input JSON config file")
    parser.add_argument(
        "--out_bq_dir",
        required=True,
        help="Output directory for BQ schema files",
    )
    args, other = parser.parse_known_args()

    run(args.in_json, args.out_bq_dir)
