import argparse
import os
from utils.schema_generator import SchemaGenerator


SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(SCRIPT_PATH, "..")
CLIENT_CONFIG_PATTERN = "conf/{client}/config.yml"
SOURCE_PATH_PATTERN = "conf/{client}/sources"
TABLE_PATH_PATTERN = "conf/{client}/tables"
PROTO_PATH_PATTERN = "conf/{client}/protobuf"


def _run(client: str) -> None:
    gen = SchemaGenerator(working_dir=PROJECT_ROOT)
    gen.generate_schema(client=client)


parser = argparse.ArgumentParser()
parser.set_defaults(func=_run)
parser.add_argument(
    "-c", "--client",
    type=str,
    help="The client ID to process."
)


if __name__ == "__main__":
    args = parser.parse_args()
    args.func(args.client)
