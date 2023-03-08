import os
import shutil
import yaml


SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(SCRIPT_PATH, "../..")
TMP_DIR = os.path.join(SCRIPT_PATH, "../../.sandbox")
CLIENT_CONFIG_PATTERN = "conf/{client}/config.yml"
SOURCE_PATH_PATTERN = "conf/{client}/sources"
DATAFLOW_PATH_PATTERN = "dataflow/template/takeoff/dl/ingest/sources/{client}"


def client_enabled(config: dict):
    return True if config.get('enabled', False) == True else False


def iterate_clients() -> list:
    clients = []
    for item in os.listdir(os.path.join(PROJECT_ROOT, "conf")):
        if os.path.isdir(os.path.join(PROJECT_ROOT, "conf", item)):
            with open(os.path.join(PROJECT_ROOT, CLIENT_CONFIG_PATTERN.format(client=item)), 'r') as file:
                yml = yaml.load(file, Loader=yaml.FullLoader)
            if client_enabled(yml):
                clients.append(item)

    return clients


def validate_sources(clients: list, sources: list) -> None:
    source_map = _get_available_sources(clients=clients)
    for client in clients:
        for source in sources:
            if not source in source_map[client]:
                raise RuntimeError(
                    f"Source '{source}' not found in conf/{client}/config.yml")
            else:
                continue


def _get_available_sources(clients: list) -> dict:
    source_list = {}
    for client in clients:
        source_list[client] = []
        with open(os.path.join(PROJECT_ROOT, CLIENT_CONFIG_PATTERN.format(client=client)), 'r') as file:
            yml = yaml.load(file, Loader=yaml.FullLoader)
        for source_id, source_data in yml['sources'].items():
            source_list[client].append(source_data['source_name'])

    return source_list


def copy_sources() -> None:
    if os.path.exists(os.path.join(TMP_DIR, "dataflow/template/takeoff/dl/ingest/sources")):
        shutil.rmtree(os.path.join(
            TMP_DIR, "dataflow/template/takeoff/dl/ingest/sources"))
    clients = iterate_clients()
    for client in clients:
        shutil.copytree(os.path.join(TMP_DIR, SOURCE_PATH_PATTERN.format(client=client)), os.path.join(
            TMP_DIR, DATAFLOW_PATH_PATTERN.format(client=client), "sources"))
        with open(os.path.join(TMP_DIR, DATAFLOW_PATH_PATTERN.format(client=client), "__init.py__"), 'w') as file:
            pass
    with open(os.path.join(TMP_DIR, "dataflow/template/takeoff/dl/ingest/sources/__init.py__"), 'w') as file:
        pass
