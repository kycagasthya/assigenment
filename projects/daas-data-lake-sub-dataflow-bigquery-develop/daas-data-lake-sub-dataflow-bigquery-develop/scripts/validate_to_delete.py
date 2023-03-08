import json
import os
import sys
import yaml

def client_enabled(config: dict):
    return True if config.get('enabled', False) == True else False

def table_protected(source: dict):
    return True if yml['tables'][source]['protected'] == True else False

def set_action_output(name: str, value: str):
    sys.stdout.write(f'::set-output name={name}::{value}\n')


if __name__ == "__main__":
    client_id = sys.argv[1]
    client_config = "../conf/" + client_id + "/config.yml"

    with open(client_config, 'r') as file:
        yml = yaml.load(file, Loader=yaml.FullLoader)

    if os.path.isdir("../conf/" + client_id):
        if client_enabled(yml):
            raise ValueError("The client is currently active.")
        for src in yml['tables']:
            if table_protected(src):
                raise ValueError("The table `" + yml['tables'][src]['table_id'] + "` is protected from deletion.")
    else:
        raise FileNotFoundError("Client not found.")

    set_action_output('to_delete', json.dumps(client_id))