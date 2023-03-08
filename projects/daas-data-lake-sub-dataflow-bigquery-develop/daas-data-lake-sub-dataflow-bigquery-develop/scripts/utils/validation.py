import json

import cerberus
from cerberus import Validator

from .common import OPTIONAL_COLUMNS
from .generation import flatten, get_fields


INVALID_NAME_PREFIXES = ["_TABLE_", "_FILE_", "_PARTITION"]
MAX_NAME_LENGTH = 300
MAX_DESC_LENGTH = 1024


def name_field_check(field, value, error):
    for prefix in INVALID_NAME_PREFIXES:
        if value.lower().startswith(prefix.lower()):
            error(field, f"bad field name prefix '{prefix}'")


cerberus.schema_registry.add(
    "field_schema",
    {
        "name": {
            "type": "string",
            "required": True,
            "allof": [
                {"maxlength": MAX_NAME_LENGTH},
                {"regex": "[a-z_]+[a-zA-Z0-9_]*"},
                {"check_with": name_field_check},
            ],
        },
        "type": {
            "type": "string",
            "required": True,
            "oneof": [
                {
                    "allowed": [
                        "STRING",
                        "BYTES",
                        "INTEGER",
                        "FLOAT",
                        "NUMERIC",
                        "BIGNUMERIC",
                        "BOOLEAN",
                        "TIMESTAMP",
                        "DATE",
                        "TIME",
                        "DATETIME",
                        "GEOGRAPHY",
                        "JSON",
                    ]
                },
                {"allowed": ["RECORD"], "dependencies": "fields"},
            ],
        },
        "mode": {
            "type": "string",
            "required": True,
            "allowed": ["REQUIRED", "NULLABLE", "REPEATED"],
        },
        "pubsub_mode": {
            "type": "string",
            "allowed": ["REQUIRED"],
            "dependencies": {"mode": "NULLABLE"},
        },
        "description": {"type": "string", "maxlength": MAX_DESC_LENGTH},
        "policyTags": {
            "type": "dict",
            "schema": {
                "names": {
                    "type": "list",
                    "required": True,
                    "schema": {"type": "string"},
                }
            },
        },
        "fields": {
            "type": "list",
            "minlength": 1,
            "schema": {"type": "dict", "schema": "field_schema"},
            "dependencies": {"type": "RECORD"},
        },
    },
)

SOURCE_CONFIG_SCHEMA = {
    "schema_name": {"type": "string"},
    "schema_version": {"type": "string"},
    "schema_description": {"type": "string"},
    "labels": {"type": "dict"},
    "fields": {
        "type": "list",
        "required": True,
        "schema": {"type": "dict", "schema": "field_schema"},
    },
}

SERVICE_COLUMNS = [
    {
        "name": "__client_name",
        "type": "STRING",
        "mode": "REQUIRED",
    },
    {
        "name": "__source_name",
        "type": "STRING",
        "mode": "REQUIRED",
    },
    {
        "name": "__schema_version",
        "type": "STRING",
        "mode": "REQUIRED",
    },
    {
        "name": "__event_timestamp",
        "type": "TIMESTAMP",
        "mode": "REQUIRED",
    },
]


def validate_service_columns(document):
    """
    Validate mandatory service columns

    :param document:
    """
    col_status = {}
    for service_col in SERVICE_COLUMNS:
        col_status[service_col["name"]] = False
        # check each column from the document against a service column
        for col in document["fields"]:
            if all([col[key] == value for key, value in service_col.items()]):
                col_status[service_col["name"]] = True

    # raise an exception if any service column is missed
    missing_cols = [key for key, value in col_status.items() if not value]
    if missing_cols:
        message_columns = [
            col for col in SERVICE_COLUMNS if col["name"] in missing_cols
        ]
        raise Exception(
            f"Missing or invalid service columns: {missing_cols}\n"
            f"Use these values: {json.dumps(message_columns, indent=2)}"
        )


def validate_optional_columns(document):
    """
    Validate optional service columns

    :param document:
    """
    bad_cols = []
    for optional_col in OPTIONAL_COLUMNS:
        # check each column from the document against a service column
        for col in document["fields"]:
            if optional_col["name"] == col["name"] and not all(
                [col[key] == value for key, value in optional_col.items() if key != 'description']
            ):
                bad_cols.append(optional_col["name"])

    if bad_cols:
        message_columns = [col for col in OPTIONAL_COLUMNS if col["name"] in bad_cols]
        raise Exception(
            f"Invalid service columns: {bad_cols}\n"
            f"Use these values: {json.dumps(message_columns, indent=2)}"
        )


def validate_duplicates(document):
    """
    Validate duplicate column names

    :param document:
    """
    # get list of field's full path
    fields = [path for path, _ in flatten(get_fields(document["fields"], ""))]

    # count fields
    field_counter = {}
    for f in fields:
        if f in field_counter:
            field_counter[f] += 1
        else:
            field_counter[f] = 1

    # raise an exception if there are duplicates
    duplicates = [field for field, counter in field_counter.items() if counter > 1]
    if duplicates:
        raise Exception(f"Duplicate fields: {duplicates}")


def validate_syntax(document):
    """
    Validate config schema syntax

    :param document:
    """
    v = Validator(schema=SOURCE_CONFIG_SCHEMA)
    if not v.validate(document):
        raise Exception(f"Source config syntax validation error\n{v.errors}")


def validate_config(document):
    """
    Validate source config

    :param document:
    """
    # validate schema syntax
    validate_syntax(document)

    # validate mandatory service columns
    validate_service_columns(document)

    # validate optional service columns
    validate_optional_columns(document)

    # validate duplicate column names
    validate_duplicates(document)
