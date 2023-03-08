import json
from multiprocessing.sharedctypes import Value
import os
import sys
import yaml
from validate_to_delete import client_enabled

contacts = {
    'teams': {},
    'channels': {}
}
tf_path = "%s/../terraform/monitoring" % os.path.dirname(os.path.abspath(__file__))

def get_client_contacts(config: dict):
    for src in config['sources']:
        source = config['sources'][src]['source_name']
        channel = config['sources'][src]['owner'].split("@")[0]
        email = config['sources'][src]['owner']
        contacts['teams'][source] = {}
        contacts['teams'][source]['source_name'] = source
        contacts['teams'][source]['channel_name'] = channel
        contacts['channels'][channel] = {}
        contacts['channels'][channel]['channel_name'] = channel
        contacts['channels'][channel]['email'] = email

if __name__ == "__main__":
    path = sys.argv[1]

    for item in os.listdir(path):
        if os.path.isdir(path + "/" + item):
            client_config = path + "/" + item + "/config.yml"
            with open(client_config, 'r') as file:
                yml = yaml.load(file, Loader=yaml.FullLoader)
            if client_enabled(yml):
                get_client_contacts(yml)

    with open(tf_path + '/terraform.auto.tfvars.json', 'w',encoding='utf-8') as file_handler:
            file_handler.writelines(json.dumps(contacts, indent=2))
