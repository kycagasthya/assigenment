import os
import re
import yaml
from utils import generate_bq
from utils import generate_proto


CLIENT_CONFIG_PATTERN = "conf/{client}/config.yml"
SOURCE_PATH_PATTERN = "conf/{client}/sources"
TABLE_PATH_PATTERN = "conf/{client}/tables"
PROTO_PATH_PATTERN = "conf/{client}/protobuf"


class SchemaGenerator():
    def __init__(self, working_dir) -> None:
        self.working_dir = working_dir

    def _create_version_map(self, config: dict) -> dict:
        versions = {}
        for src in config['sources']:
            version = config['sources'][src]['schema_version']
            match = re.search("v", version)
            key = config['sources'][src]['source_name']
            existing_value = versions.get(key, "0")
            new_value = version[match.end(0):]
            if float(new_value) > float(existing_value):
                versions[key] = new_value

        return versions

    def _generate_bq_schema(self, client: str, config: dict) -> None:
        versions = self._create_version_map(config=config)
        for source, version in versions.items():
            for src in config['sources']:
                if config['sources'][src]['source_name'] == source and config['sources'][src]['schema_version'] == "v" + str(version):
                    input_json = os.path.join(self.working_dir, SOURCE_PATH_PATTERN.format(
                        client=client), config['sources'][src]['configuration'])
                    table = os.path.join(self.working_dir, TABLE_PATH_PATTERN.format(
                        client=client), config['tables'][source]['table_id'])
                    print("Current version for `" + source +
                          "`: v" + version + " in " + input_json)
                    generate_bq.run(input_json, table)

    def _generate_pubsub_proto(self, client: str, config: dict) -> None:
        for src in config['sources']:
            input_json = os.path.join(self.working_dir, SOURCE_PATH_PATTERN.format(
                client=client), config['sources'][src]['configuration'])
            protobuf = os.path.join(self.working_dir, PROTO_PATH_PATTERN.format(
                client=client), config['sources'][src]['configuration'].replace('json', 'proto'))
            generate_proto.run(input_json, protobuf)

    def generate_schema(self, client: str) -> None:
        client_config = os.path.join(
            self.working_dir, CLIENT_CONFIG_PATTERN.format(client=client))
        with open(client_config, 'r') as file:
            yml = yaml.load(file, Loader=yaml.FullLoader)
        self._generate_bq_schema(client=client, config=yml)
        # self._generate_pubsub_proto(client=client, config=yml)
