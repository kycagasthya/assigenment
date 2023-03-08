# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# =============================================================================

"""This module will perform training for cde processor"""

import argparse
import json
import traceback
import requests
import time
from kfp.v2.dsl import Output,Artifact
from kfp.v2.components.executor import Executor
import google.auth
import google.auth.transport.requests
from custom_logger import ml_logger as logger


def get_auth_token(location: str)->(str, str):
    """
    Function to get token for authetication and host for post/get request
    Args:
        location (str):location of the processor
    Returns:
        Returns token and host for post/get request
    """
    authentication_request = google.auth.transport.requests.Request()
    credentials, _ = google.auth.default()
    credentials.refresh(authentication_request)
    token = credentials.token

    endpoint = f"{location}-documentai.googleapis.com"
    host = f"https://{endpoint}"

    return token, host


def uptraining(project_number: str, processor_id: str, version_id: str,
               location: str, model_version_name: str):
    """
    Function to do uptraining
    Args:
        project_number (str): project_number
        processor_id (str): processor_id
        version_id (str): version_id to uptrain from
        location (str):location of the processor
        model_version_name (str): Display name of the processor
    Returns:
        Returns response for the post request
    """
    token, host = get_auth_token(location)

    base_version = f"projects/{project_number}/locations/{location}/\
processors/{processor_id}/processorVersions/{version_id}"
    post_data = {
        "processorVersion" : {
            "displayName" : model_version_name
        },
        "baseProcessorVersion" : base_version
    }

    url = f"{host}/uiv1beta3/projects/{project_number}/locations/{location}/\
processors/{processor_id}/processorVersions:train"

    response = requests.post(url,data=json.dumps(post_data),
                             headers={"Authorization": f"Bearer {token}"})

    return response


def training_from_scratch(project_number: str, processor_id: str,
                          location: str, model_version_name: str):
    """
    Function to do training from scratch
    Args:
        project_number (str): project_number
        processor_id (str): processor_id
        location (str):location of the processor
        model_version_name (str): Display name of the processor
    Returns:
        Returns response for the post request
    """
    token, host = get_auth_token(location)

    post_data = {
        "processorVersion" : {
            "displayName" : model_version_name
        }
    }

    url = f"{host}/uiv1beta3/projects/{project_number}/locations/{location}/\
processors/{processor_id}/processorVersions:train"

    response = requests.post(url,data=json.dumps(post_data),
                             headers={"Authorization": f"Bearer {token}"})

    return response


def get_latest_version(project_number: str, processor_id: str,
                       location: str)->str:
    """
    Function to get the latest version of the processor
    Args:
        project_number (str): project_number
        processor_id (str): processor_id
        location (str):location of the processor
    Returns:
        Returns version_id of latest version
    """
    try:
        token, host = get_auth_token(location)

        url = f"{host}/uiv1beta3/projects/{project_number}/\
locations/{location}/processors/{processor_id}/processorVersions/"

        response = requests.get(url,
                                headers={"Authorization": f"Bearer {token}"})

        if response.status_code == 200:
            try:
                latest_version = sorted(response.json()["processorVersions"],
                                        key= lambda x:x["createTime"])[-1]
                version_id = latest_version["name"].split("/")[-1]
                logger("INFO", "Training", f"Latest version id : {version_id}")

            except KeyError as error:
                trace=traceback.format_exc()
                logger("ERROR", "Training", error, "", response.json(), trace)
                raise

            except Exception as error:
                trace=traceback.format_exc()
                logger("ERROR", "Training", error, "500",
                       response.json(), trace)
                raise

        elif response.status_code == 403:
            raise RuntimeError("The ProjectID is incorrect or doesnot exist")
        elif response.status_code == 404:
            raise RuntimeError("The ProcessorID is incorrect or doesnot exist")
        else:
            raise RuntimeError("Unknown error")

    except RuntimeError as error:
        trace=traceback.format_exc()
        if response.text:
            logger("ERROR", "Training", error, str(response.status_code),
                   response.json(), trace)
        else:
            logger("ERROR", "Training", error, str(response.status_code),
                   traceback=trace)
        raise

    except Exception as error:
        trace=traceback.format_exc()
        logger("ERROR", "Training", error, "500", traceback=trace)
        raise

    return version_id


def get_default_version(project_number: str, processor_id: str,
                        location: str)->str:
    """
    Function to get the default version of the processor
    Args:
        project_number (str): project_number
        processor_id (str): processor_id
        location (str):location of the processor
    Returns:
        Returns version_id of default version
    """
    try:
        token, host = get_auth_token(location)

        url = f"{host}/uiv1beta3/projects/{project_number}/\
locations/{location}/processors/{processor_id}/"

        response = requests.get(url,
                                headers={"Authorization": f"Bearer {token}"})

        if response.status_code == 200:
            try:
                version_id = response.json()[
                             "defaultProcessorVersion"].split("/")[-1]
                logger("INFO", "Training", f"Default version id: {version_id}")

            except KeyError as error:
                trace=traceback.format_exc()
                logger("ERROR", "Training", error, "", response.json(), trace)
                raise

            except Exception as error:
                trace=traceback.format_exc()
                logger("ERROR", "Training", error, "500",
                       response.json(), trace)
                raise

        elif response.status_code == 403:
            raise RuntimeError("The ProjectID is incorrect or doesnot exist")
        elif response.status_code == 404:
            raise RuntimeError("The ProcessorID is incorrect or doesnot exist")
        else:
            raise RuntimeError("Unknown error")

    except RuntimeError as error:
        trace=traceback.format_exc()
        if response.text:
            logger("ERROR", "Training", error, str(response.status_code),
                   response.json(), trace)
        else:
            logger("ERROR", "Training", error, str(response.status_code),
                   traceback=trace)
        raise

    except Exception as error:
        trace=traceback.format_exc()
        logger("ERROR", "Training", error, "500", traceback=trace)
        raise

    return version_id


def training(project_number: str, processor_id: str, version: str,
             location: str, model_version_name: str):
    """
    Function to do training of the processor
    Args:
        project_number (str): project_number
        processor_id (str): processor_id
        version (str): version type("latest", "default", "none", version_id)
        location (str):location of the processor
        model_version_name (str): Display name of the processor
    Returns:
        Returns response for the post request
    """
    if version == "default":
        version_id = get_default_version(project_number,
                                         processor_id, location)
        response = uptraining(project_number, processor_id, version_id,
                              location, model_version_name)

    elif version == "latest":
        version_id = get_latest_version(project_number, processor_id, location)
        response = uptraining(project_number, processor_id, version_id,
                              location, model_version_name)

    elif version == "none":
        response = training_from_scratch(project_number, processor_id,
                                         location, model_version_name)

    else:
        response = uptraining(project_number, processor_id, version,
                              location, model_version_name)

    return response


def create_version_name(project_number: str, processor_id: str,
                        location: str)->str:
    """
    Function to get version name of the processor
    Args:
        project_number (str): project_number
        processor_id (str): processor_id
        location (str):location
    Returns(string):
        Returns a new version name
        new_version_name (str) :new_version_name
    """

    try:
        token, host = get_auth_token(location)
        url = f"{host}/uiv1beta3/projects/{project_number}/\
locations/{location}/processors/{processor_id}/processorVersions"
        response = requests.get(url,
                                headers={"Authorization": f"Bearer {token}"})
        logger("INFO", "Training", response.json())
        if response.status_code == 200:
            resp_dict = response.json()
            disp_name_prefix = "v"
            new_version_name = disp_name_prefix+str(1)
        elif response.status_code == 403:
            raise RuntimeError("The ProjectID is incorrect or doesnot exist")
        elif response.status_code == 404:
            raise RuntimeError("The ProcessorID is incorrect or doesnot exist")
        else:
            raise RuntimeError("Unknown error")

    except RuntimeError as error:
        trace=traceback.format_exc()
        if response.text:
            logger("ERROR", "Training", error, str(response.status_code),
                   response.json(), trace)
        else:
            logger("ERROR", "Training", error, str(response.status_code),
                   traceback=trace)
        raise

    except Exception as error:
        trace=traceback.format_exc()
        logger("ERROR", "Training", error, "500", traceback=trace)
        raise

    try:
        if len(resp_dict["processorVersions"]) > 0:
            all_display_names = []
            all_display_integers = []

            for i in range(len(resp_dict["processorVersions"])):
                if not "Google default" in resp_dict["processorVersions"][i][
                    "displayName"]:
                    cur_disp_name = resp_dict["processorVersions"][i][
                                    "displayName"]
                    all_display_names.append(cur_disp_name)
                    if len(cur_disp_name) >= len(disp_name_prefix)+1 and \
                    str(cur_disp_name.lower()).startswith(disp_name_prefix) \
                    and cur_disp_name[len(disp_name_prefix):].isdigit():
                        all_display_integers.append(
                                int(cur_disp_name[len(disp_name_prefix):]))
            if len(all_display_integers) > 0:
                new_version_name = disp_name_prefix + str(
                                   max(all_display_integers)+1)
            logger("INFO", "Training", f"new version name:{new_version_name}")
    except Exception as error:
        trace=traceback.format_exc()
        logger("INFO", "Training", error, "500", traceback = trace)
        raise
    return new_version_name


def lro(lro_name: str, location: str, check_status_after: str):
    """
    Function to check lro status of training job
    Args:
        lro_name (str): lro_name
        location (str):location of the processor
        check_status_after (str):time interval in millimeters after
                                 which status is checked
    Returns(string):
        Returns status of the training job
    """
    token, host = get_auth_token(location)
    url = f"{host}/uiv1beta3/{lro_name}"
    lro_response = requests.get(url,
                   headers={"Authorization": f"Bearer {token}"})

    try:
        lro_response_json=lro_response.json()
        status=lro_response_json["metadata"][
                    "commonMetadata"]["state"]
    except Exception as error:
        trace=traceback.format_exc()
        if lro_response.text:
            logger("ERROR", "Training", error,
            str(lro_response.status_code), lro_response.json(), trace)
        else:
            logger("ERROR", "Training", error,
                   str(lro_response.status_code), traceback=trace)
        raise

    while status not in ["SUCCEEDED"]:
        token, _ = get_auth_token(location)
        response = requests.get(url,
                        headers={"Authorization": f"Bearer {token}"})
        try:
            response_json=response.json()
            status = response_json["metadata"][
                                   "commonMetadata"]["state"]
        except Exception as error:
            trace=traceback.format_exc()
            if response.text:
                logger("ERROR", "Training", error,
                    str(response.status_code), response.json(), trace)
            else:
                logger("ERROR", "Training", error,
                       str(response.status_code), traceback=trace)
            raise

        if status == "RUNNING":
            logger("INFO", "Training",
                   "Current state of the training-job is : RUNNING")
        elif status == "CANCELLED":
            raise RuntimeError("The Training-job has been CANCELLED")
        elif status == "FAILED":
            raise RuntimeError("The Training-job has FAILED")
        time.sleep(int(check_status_after))

    return status


def cde_train(project_number : str,
              processor_id : str,
              version : str,
              location : str,
              check_status_after : str,
              version_name: Output[Artifact]
              ):
    """
    Training Component for CDE
    Args:
        project_number (str): project_number
        processor_id (str): processor_id
        version (str): version type("latest", "default", "none", version_id)
        location (str): location
        check_status_after (str): time interval in millimeters after
                                 which status is checked
    Returns(string):
        version_name (Output[Artifact]): version_name
    """
    logger("INFO", "Training", "Entering in training component for CDE")

    model_version_name = create_version_name(project_number,
                                             processor_id, location)
    response = training(project_number, processor_id, version,
                        location, model_version_name)

    try:
        if response.status_code == 200:
            logger("INFO", "Training", "Response:" +str(response.json()),
                   response.status_code)
            version_id_temp = response.json()["metadata"][
                             "commonMetadata"]["resource"].split("/")[-1]

            logger("INFO", "Training",
                   f"Version name Artifact :{version_id_temp}")
            lro_name = response.json()["name"]

            status = lro(lro_name, location, check_status_after)
            logger("INFO", "Training", f"Training Job: {status}")
            version_name.metadata = {"version_name":model_version_name,
                                     "processor_version_id":version_id_temp}

        elif response.status_code == 403:
            raise RuntimeError("The ProjectID is incorrect or doesnot exist")
        elif response.status_code == 404:
            raise RuntimeError("The ProcessorID is incorrect or doesnot exist")
        elif response.status_code == 429:
            raise RuntimeError(
                "Resources has been Exhausted. Please check Quota limit.")
        else:
            raise RuntimeError("Unknown error")

    except RuntimeError as error:
        trace=traceback.format_exc()
        if response.text:
            logger("ERROR", "Training", error, str(response.status_code),
                   response.json(), trace)
        else:
            logger("ERROR", "Training", error, str(response.status_code),
                   traceback=trace)
        raise

    except Exception as error:
        trace=traceback.format_exc()
        logger("ERROR", "Training", error, "500", traceback=trace)
        raise


def executor_main():
    """
    The main executor function
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--executor_input", type=str)
    parser.add_argument("--function_to_execute", type=str)
    args, _ = parser.parse_known_args()
    executor_input = json.loads(args.executor_input)
    function_to_execute = globals()[args.function_to_execute]
    executor = Executor(executor_input=executor_input,
                      function_to_execute=function_to_execute)
    executor.execute()


if __name__ == "__main__":
    executor_main()
