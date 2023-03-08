import json
import os
import yaml
import argparse

import return_latest_bq


SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(SCRIPT_PATH, "..")
CLIENT_CONFIG_PATTERN = "conf/{client}/config.yml"
SOURCE_DETAILS_PATH_PATTERN = "conf/{client}/sources/{schema_file}"
TABLES_SCHEMAS_DIR_PATTERN = "conf/{client}/tables/{table_id}/"

TF_PATH = os.path.join(PROJECT_ROOT, "terragenesis/stacks/datalake/")

CLIENT_OUTPUT_CONFIG_FILE_NAME = 'client_config.json'
TF_VARS_FILE_NAME = 'terraform.auto.tfvars.json'


def create_version_map(client_config: dict) -> dict:
    versions_mapping = {}
    for source_id, source_data in client_config['sources'].items():
        source_name = source_data['source_name']

        existing_value = versions_mapping.get(source_name, '0')
        new_value = source_data['schema_version'].split('v')[-1]
        if float(new_value) > float(existing_value):
            versions_mapping[source_name] = new_value
    return versions_mapping


def prefly(client, tag=None):
    project_root = os.path.join(PROJECT_ROOT, ".sandbox") if tag else PROJECT_ROOT
    work_dir = os.path.join(
        project_root, f"stacks/{client}/") if tag else TF_PATH
    client_config_file_path = os.path.join(
        project_root, CLIENT_CONFIG_PATTERN.format(client=client))
    with open(client_config_file_path, 'r') as file:
        client_config = yaml.load(file, Loader=yaml.FullLoader)

    client_id = client_config['client_id']
    sources = client_config['sources']
    dataset_id = client_config['dataset_id']
    views_config = client_config.get('views', {})
    versions_mapping = create_version_map(client_config)

    tf_config_sources = {}
    tf_config_tables = {}
    client_output_sources_config = {}
    for source_id, source_data in sources.items():

        source_name = source_data['source_name']
        schema_version = source_data['schema_version']
        table_config = client_config['tables'][source_name]

        # if source_data['type'] == "streaming":
        if source_data.get('type', "streaming") == "streaming": # Temporary code until all sources contain 'type' field.
            client_output_sources_config[source_name] = table_config['table_id']
            tf_config_sources[source_id] = {
                'source_name': source_name,
                'schema_version': schema_version
                # 'topic_schema_file': source_data['configuration'].replace('json', 'proto')
            }

        version = versions_mapping.get(source_name)
        if version and schema_version == f'v{version}':
            source_details_path = SOURCE_DETAILS_PATH_PATTERN.format(client=client,
                                                                     schema_file=source_data['configuration'])
            table_id = table_config['table_id']
            source_details_relative_path = os.path.join(
                project_root, source_details_path)
            with open(source_details_relative_path, 'r') as file:
                source_details = json.load(file)

            tables_schemas_dir = os.path.join(project_root,
                                              TABLES_SCHEMAS_DIR_PATTERN.format(client=client,
                                                                                table_id=table_id))
            table_latest_schema = os.path.basename(
                return_latest_bq.run(tables_schemas_dir))
            tf_config_tables[source_name] = {
                'table_id': table_config['table_id'],
                'protected': table_config['protected'],
                'description': source_details['schema_description'],
                'client_labels': source_details['labels'],
                'table_schema_file': table_latest_schema
            }

    tf_client_config = {
        'client_id': client_id,
        'dataset_id': dataset_id,
        'sources': tf_config_sources,
        'tables': tf_config_tables,
        'views': views_config
    }
    with open(os.path.join(work_dir, TF_VARS_FILE_NAME), 'w') as file_handler:
        json.dump(tf_client_config, file_handler, indent=2)

    client_output_config = {
        client_id: {
            'dataset': dataset_id,
            'sources': client_output_sources_config
        }
    }
    with open(os.path.join(work_dir, CLIENT_OUTPUT_CONFIG_FILE_NAME), 'w') as file_handler:
        json.dump(client_output_config, file_handler)
    print(f"Prefly done for {client}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('client', type=str)
    parser.add_argument(
        "-t", "--tag",
        type=str,
        default=None,
        help="Tag related to datalake being created. E.g. `datalake-444`"
    )
    args = parser.parse_args()
    prefly(args.client, args.tag)
