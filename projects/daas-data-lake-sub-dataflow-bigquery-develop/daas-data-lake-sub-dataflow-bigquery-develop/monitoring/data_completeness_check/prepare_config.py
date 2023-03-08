import os
import yaml

from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent
MAIN_CONFIG_DIR = os.path.join(ROOT_DIR, 'conf')
MAIN_CONFIG_FILE_NAME = 'config.yml'

COMPLETENESS_SERVICE_CONF = os.path.join(ROOT_DIR, 'monitoring/data_completeness_check/src/config.yml')


def load_yaml(yaml_path: str):
    """
    Loads YAML file content as dict

    :param str yaml_path: YAML file local path
    :return dict: loaded YAML content
    """
    with open(yaml_path, "r") as stream:
        return yaml.safe_load(stream)


def save_yaml(yaml_path: str, data: dict):
    """
    Saves dictionary as YAML file

    :param str yaml_path: YAML file local path
    :param dict data: dictionary to store into YAML
    :return dict : loaded YAML content
    """
    with open(yaml_path, "w") as stream:
        yaml.safe_dump(data, stream)


if __name__ == '__main__':
    conf_sub_dirs = [f.path for f in os.scandir(MAIN_CONFIG_DIR) if f.is_dir()]

    config = {}
    for conf_subdir in conf_sub_dirs:
        conf_file_path = os.path.join(conf_subdir, MAIN_CONFIG_FILE_NAME)
        client_conf = load_yaml(conf_file_path)
        if client_conf['enabled']:
            client_sources = []
            for source_name, source_table_config in client_conf['tables'].items():
                client_sources.append(source_table_config['table_id'])
            config[client_conf['client_id']] = client_sources
    save_yaml(COMPLETENESS_SERVICE_CONF, config)
