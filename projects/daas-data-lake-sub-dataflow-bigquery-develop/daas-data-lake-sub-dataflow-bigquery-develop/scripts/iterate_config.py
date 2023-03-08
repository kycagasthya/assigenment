import json
import os
import sys
import yaml
from validate_to_delete import client_enabled, set_action_output

if __name__ == "__main__":
    folders = []
    path = sys.argv[1]

    for item in os.listdir(path):
        if os.path.isdir(path + "/" + item):
            client_config = path + "/" + item + "/config.yml"
            with open(client_config, 'r') as file:
                yml = yaml.load(file, Loader=yaml.FullLoader)
            if client_enabled(yml):
                folders.append(item)

    set_action_output('folders', json.dumps(folders))
  