#!/usr/bin/env python
import argparse
import json
import os
import sys
from utils.deployment import create_infra, create_datalake, cleanup
from utils.iteration import iterate_clients, validate_sources


SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
TMP_DIR = os.path.join(SCRIPT_PATH, "../.sandbox")


def _up(args):
    project = args.project
    tag = args.tag
    if args.clients == "all":
        clients = iterate_clients()
    else:
        clients = args.clients.split(",")
    sources = args.sources.split(",")
    if len(sources) > 1:
        validate_sources(clients=clients, sources=sources)
    elif len(sources) == 1:
        if "all" in sources:
            pass
        else:
            validate_sources(clients=clients, sources=sources)

    create_infra(project=project, tag=tag,
                 clients=clients, sources=sources)
    results = create_datalake(project=project, tag=tag,
                              clients=clients, sources=sources)
    for result in results:
        print(result)


def _down(args):
    project = args.project
    with open(f"{TMP_DIR}/.sandbox.json", 'r') as file:
        sandbox_config = json.load(file)
    tag = sandbox_config['tag']
    clients = sandbox_config['clients']
    cleanup(project=project, tag=tag, clients=clients)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()
create = subparsers.add_parser('create')
create.set_defaults(func=_up)
delete = subparsers.add_parser('delete')
delete.set_defaults(func=_down)
create.add_argument(
    "-p", "--project",
    type=str,
    required=True,
    help="The Google Cloud project ID."
)
create.add_argument(
    "-c", "--clients",
    type=str,
    default="all",
    help="Comma-separated list of clients to spin up. Deploys all clients by default."
)
create.add_argument(
    "-s", "--sources",
    type=str,
    default="all",
    help="Comma-separated list of sources to spin up. Deploys all sources per client by default."
)
create.add_argument(
    "-t", "--tag",
    type=str,
    required=True,
    help="Tag related to datalake being created. E.g. `datalake-444`"
)

delete.add_argument(
    "-p", "--project",
    type=str,
    required=True,
    help="The Google Cloud project ID."
)


if __name__ == "__main__":
    args = parser.parse_args()
    args.func(args)
