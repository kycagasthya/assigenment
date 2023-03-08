import json
import os
import shutil
import sys
import concurrent.futures
import logging

from prefly import prefly
from utils.dataflow_template import DataflowTemplate
from utils.iteration import copy_sources
from utils.schema_generator import SchemaGenerator
from utils.terraform_stack import TerraformStack


SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(SCRIPT_PATH, "../..")
TMP_DIR = os.path.join(PROJECT_ROOT, ".sandbox")
FORMAT = "%(asctime)s: %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)

# Values defined here are not real.
ENV = "sandbox"
SLACK = {
    'notification_channel': '#coe-data-lake-alerting-gcp--nonprod',
    'auth_token': 'idontknowthetoken'
}
OPSGENIE_TOKEN = "13644b83-29a4-4432-90ce-71d7c6b11d38"
GITHUB_TOKEN = "ghp_PeeTKU2RMoQyWE8oNru2F58Mak5eFA2niqW0"
PUB_PROJECT_ID = "prj-daas-n-stg-dl-pub-gen-25d0"


def create_infra(project: str, tag: str, clients: list[str], sources: list[str]):
    logging.info("Creating the sandbox...")
    try:
        shutil.copytree(os.path.join(
            PROJECT_ROOT, "terragenesis/modules"), os.path.join(TMP_DIR, "modules"))
        shutil.copytree(os.path.join(
            PROJECT_ROOT, "terragenesis/src"), os.path.join(TMP_DIR, "src"))
        shutil.copytree(os.path.join(PROJECT_ROOT, "dataflow"),
                        os.path.join(TMP_DIR, "dataflow"))
        shutil.copytree(os.path.join(PROJECT_ROOT, "conf"),
                        os.path.join(TMP_DIR, "conf"))
    except OSError as e:
        logging.error(e)
    # Create infrastructure stack
    sandbox_config = {
        "project": project,
        "tag": tag,
        "clients": clients,
        "sources": sources
    }
    try:
        with open(os.path.join(TMP_DIR, ".sandbox.json"), 'r') as file:
            current_config = json.load(file)
            logging.info("Sandbox configuration found")
            current_config['clients'] = list(dict.fromkeys(
                current_config['clients'] + sandbox_config['clients']))
            current_config['sources'] = list(dict.fromkeys(
                current_config['sources'] + sandbox_config['sources']))
            with open(os.path.join(TMP_DIR, ".sandbox.json"), 'w') as file:
                json.dump(current_config, file)
            logging.info("Successfully updated sandbox configuration")
    except FileNotFoundError:
        with open(os.path.join(TMP_DIR, ".sandbox.json"), 'w') as file:
            json.dump(sandbox_config, file)
    print(
        "Google project:", project, "\n"
        "Clients:", clients, "\n"
        "Sources (per client):", sources, "\n"
        "Tag:", tag
    )

    tf_dir = os.path.join(PROJECT_ROOT, "terragenesis/stacks/infra")
    try:
        shutil.copytree(tf_dir, os.path.join(TMP_DIR, "stacks/infra"))
        os.remove(os.path.join(TMP_DIR, "stacks/infra/functions.tf"))
        os.remove(os.path.join(TMP_DIR, "stacks/infra/secrets.tf"))
    except (FileExistsError, FileNotFoundError) as e:
        logging.error(e)

    infra = TerraformStack(
        working_dir=os.path.join(TMP_DIR, "stacks/infra"),
        project=project,
        variables={
            "project": project,
            "tag": tag,
            "env": ENV,
            "publisher_project_id": PUB_PROJECT_ID,
            "slack": SLACK,
            "opsgenie_token": OPSGENIE_TOKEN,
            "github_private_access_token": GITHUB_TOKEN
        }
    )
    try:
        infra.init(prefix="infrastructure/state")
        infra.apply()
        logging.info("The infrastructure has been created")
    except Exception as e:
        logging.error(f"Failed to create the infrastructure\n{e}")
        sys.exit(1)


def create_datalake(project: str, tag: str, clients: list[str], sources: list[str]):
    try:
        copy_sources()
    except FileExistsError as e:
        logging.warning(e)
    # Build Dataflow template
    tpl = DataflowTemplate(
        working_dir=TMP_DIR,
        project=project
    )
    try:
        template_path = tpl.create()
        logging.info("Dataflow template has been created successfully")
    except Exception as e:
        logging.error(f"Failed to create Dataflow template\n{e}")
        sys.exit(1)
    # template_path = "gs://sandbox-20220126-a9lh9m-artifacts/templates/test-py-image-latest.json"
    futures_list = []
    results = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        for client in clients:
            futures = executor.submit(_deploy_client, project=project,
                                      tag=tag, client=client, sources=sources, template_path=template_path)
            futures_list.append(futures)
        for future in futures_list:
            try:
                result = future.result(timeout=60)
                results.append(result)
            except Exception as e:
                results.append(e)
    return results


def _deploy_client(project: str, tag: str, client: str, sources: list, template_path: str):
    gen = SchemaGenerator(working_dir=TMP_DIR)
    gen.generate_schema(client=client)
    logging.info(f"Creating the datalake for {client}...")
    tf_dir = os.path.join(PROJECT_ROOT, "terragenesis/stacks/datalake")
    try:
        shutil.copytree(tf_dir, os.path.join(TMP_DIR, "stacks", client))
        os.remove(os.path.join(TMP_DIR, "stacks", client, "monitoring.tf"))
        os.remove(os.path.join(TMP_DIR, "stacks", client, "views.tf"))
    except (FileExistsError, FileNotFoundError) as e:
        logging.error(e)
    try:
        prefly(client, tag)
        if not 'all' in sources:
            _sort_sources(client, sources)
    except Exception as e:
        print(e)
    datalake = TerraformStack(
        working_dir=os.path.join(TMP_DIR, "stacks", client),
        project=project,
        variables={
            "project": project,
            "tag": tag,
            "env": ENV,
            "template_path": template_path
        }
    )
    try:
        datalake.init(prefix=f"snfk-to-gcp/state/{client}")
        tfargs = {
            "replace": [
                "google_dataflow_flex_template_job.df_job"
            ]
        }
        datalake.apply(tfargs)
        logging.info(f"Successfully created the datalake for {client}")
    except Exception as e:
        logging.error(f"Failed to create the datalake for {client}\n{e}")
        sys.exit(1)


def _sort_sources(client: str, sources: list) -> None:
    with open(os.path.join(TMP_DIR, "stacks", client, "terraform.auto.tfvars.json"), 'r') as file:
        config = json.load(file)

    for source_id, source_data in list(config['sources'].items()):
        if not source_data['source_name'] in sources:
            del config['sources'][source_id]
            if source_data['source_name'] in config['tables']:
                del config['tables'][source_data['source_name']]
    with open(os.path.join(TMP_DIR, "stacks", client, "terraform.auto.tfvars.json"), 'w') as file:
        json.dump(config, file, indent=2)

    with open(os.path.join(TMP_DIR, "stacks", client, "client_config.json"), 'r') as file:
        config = json.load(file)
    for source, table in list(config[client]['sources'].items()):
        if not source in sources:
            del config[client]['sources'][source]
    with open(os.path.join(TMP_DIR, "stacks", client, "client_config.json"), 'w') as file:
        json.dump(config, file, indent=2)


def cleanup(project: str, tag: str, clients: list):
    logging.info(f"Cleaning up the sandbox...")
    template_path = f"gs://{project}/templates/test-py-image-latest.json"
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        for client in clients:
            executor.submit(_wipe_client, project=project, tag=tag,
                            client=client, template_path=template_path)
    # Delete infrastructure stack
    infra = TerraformStack(
        working_dir=os.path.join(TMP_DIR, "stacks/infra"),
        project=project,
        variables={
            "project": project,
            "tag": tag,
            "env": ENV,
            "publisher_project_id": PUB_PROJECT_ID,
            "slack": SLACK,
            "opsgenie_token": OPSGENIE_TOKEN,
            "github_private_access_token": GITHUB_TOKEN
        }
    )
    try:
        infra.destroy()
        shutil.rmtree(TMP_DIR)
        logging.info(f"The sandbox has been cleaned up succesfully")
    except Exception as e:
        logging.error(f"Failed to clean up the sandbox\n{e}")
        sys.exit(1)


def _wipe_client(project: str, tag: str, client: str, template_path: str):
    datalake = TerraformStack(
        working_dir=os.path.join(TMP_DIR, "stacks", client),
        project=project,
        variables={
            "project": project,
            "tag": tag,
            "env": ENV,
            "template_path": template_path
        }
    )
    try:
        datalake.destroy()
        logging.info(f"Successfully destroyed the datalake for {client}")
    except Exception as e:
        logging.error(
            f"Failed to destroy datalake resources for {client}\n{e}")
        sys.exit(1)
