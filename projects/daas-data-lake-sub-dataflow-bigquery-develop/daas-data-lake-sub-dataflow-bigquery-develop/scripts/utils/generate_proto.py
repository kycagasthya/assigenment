import argparse
from io import StringIO
import os
from typing import List

from utils.generation import find_key, load_json, normalize
from utils.generation import FIELDS_COL, MODE_COL, NAME_COL, PUBSUB_MODE_COL, TYPE_COL
from utils.generation import NULLABLE_MODE, OPTIONAL_MODE, REPEATED_MODE, REQUIRED_MODE
from utils.validation import validate_config


# proto schema
INDENT = "  "
PROTO_HEADER = """syntax = "proto2";

message protocol_buffer {
"""
PROTO_FOOTER = "}"


def convert_mode(bq_mode: str, pubsub_mode: str) -> str:
    """
    Convert BQ mode to protobuf mode

    :param bq_mode:
    :param pubsub_mode:
    :return: protobuf mode
    """
    if pubsub_mode:
        if pubsub_mode.lower() == REQUIRED_MODE and bq_mode.lower() == NULLABLE_MODE:
            return REQUIRED_MODE
        else:
            raise Exception(f"Illegal values for {PUBSUB_MODE_COL}/{MODE_COL}: '{pubsub_mode}'/'{bq_mode}'")
    elif bq_mode.lower() == NULLABLE_MODE:
        return OPTIONAL_MODE
    elif bq_mode.lower() == REQUIRED_MODE:
        return REQUIRED_MODE
    elif bq_mode.lower() == REPEATED_MODE:
        return REPEATED_MODE
    else:
        raise Exception(f"Unknown BQ mode value: {bq_mode}")


def convert_type(bq_type: str) -> str:
    """
    Convert BQ data type to protobuf data type

    :param bq_type:
    :return: protobuf data type
    """
    if bq_type.lower() in ("int64", "integer"):
        return "int64"
    elif bq_type.lower() in ("float64", "float", "numeric", "bignumeric"):
        return "double"
    elif bq_type.lower() in ("bool", "boolean"):
        return "bool"
    elif bq_type.lower() == "bytes":
        return "bytes"
    elif bq_type.lower() == "record":
        return "record"
    else:
        return "string"


def parse(buffer: StringIO, fields: List, level: int, path: str):
    """
    Parse JSON fields and generate protobuf schema written to buffer

    :param buffer: out buffer
    :param fields: list of JSON fields
    :param level: nesting level
    :param path: nesting level path
    """
    for i, field in enumerate(fields, 1):
        # convert mode and type
        proto_mode = convert_mode(field[MODE_COL], field.get(PUBSUB_MODE_COL))
        proto_type = convert_type(field[TYPE_COL])
        proto_name = field[NAME_COL]

        if proto_type == "record":
            # build record proto field
            if FIELDS_COL not in field:
                raise Exception(f"'{FIELDS_COL}' key not found for 'record' column")

            # record type name includes level path ot make it unique
            record_type = path + "_" + proto_name + "_record"

            # declare record field
            buffer.write(
                INDENT * level + f"{proto_mode} {record_type} {proto_name} = {i};\n"
            )

            # declare record type
            buffer.write(INDENT * level + f"message {record_type} {{\n")
            parse(buffer, field[FIELDS_COL], level + 1, path + "_" + proto_name)
            buffer.write(INDENT * level + "}\n")
        else:
            # declare scalar field
            buffer.write(
                INDENT * level + f"{proto_mode} {proto_type} {proto_name} = {i};\n"
            )


def generate(config: dict) -> StringIO:
    """
    Generate protobuf schema from JSON config

    :param config: input config JSON dict
    :return: protobuf schema
    """
    # get and normalize schema
    schema = config[find_key(FIELDS_COL, config)]
    schema = normalize(schema)

    # create out buffer
    out_buf = StringIO()

    # parse BQ schema and generate protobuf schema, write it to out buffer
    out_buf.write(PROTO_HEADER)
    parse(out_buf, schema, 1, "")
    out_buf.write(PROTO_FOOTER)

    return out_buf


def run(in_json: str, out_protobuf: str = None):
    """
    Generate protobuf schema file from JSON schema file

    :param in_json: input config JSON file name, "fields" schema format must be BigQuery JSON schema like
    :param out_protobuf: output protobuf file name
    """
    json_config = load_json(in_json)

    # validate input config
    validate_config(json_config)

    # generate protobuf StringIO
    proto = generate(json_config)

    # write StringIO to out file
    os.makedirs(os.path.dirname(out_protobuf), exist_ok=True)
    with open(out_protobuf, "w") as out_file:
        out_file.write(proto.getvalue())
        proto.close()


if __name__ == "__main__":
    # parse input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--in_json", required=True, help="Input JSON config file")
    parser.add_argument(
        "--out_protobuf",
        required=True,
        help="Output protocol buffer schema file",
    )
    args, other = parser.parse_known_args()

    run(args.in_json, args.out_protobuf)
