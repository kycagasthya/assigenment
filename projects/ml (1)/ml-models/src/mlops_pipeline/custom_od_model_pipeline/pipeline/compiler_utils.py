# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# =============================================================================

"""This module will contain composer utility files"""

import os
from google.cloud import storage


def list_files(bucket_name: str, bucket_folder: str)->list:
    """
    Lists files in a GCP bucket.
    Args:
        bucket_name (str): bucket name where files stored
        bucket_folder (str): folder name where files stored
    Returns:
        files (list): List of files
    """

    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    elements = bucket.list_blobs(prefix=bucket_folder)
    files=['gs://'+ bucket_name + '/' + a.name for a in elements]
    return files

def upload_blob(bucket_name: str, source_file_name: str,
                destination_blob_name: str):
    """
    Uploads a file to the bucket.
    Args:
        bucket_name (str): bucket name where files stored
        source_file_name (str): path to source file
        destination_blob_name (str): complete path of destination folder
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

def delete_blob(bucket_name: str, blob_name: str):
    """
    Deletes a blob from the bucket.
    Args:
        bucket_name (str): bucket name where files stored
        blob_name (str): path to file
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()

def save_spec_file(bucket_path: str, commit_sha: str,
                   local_file: str, model: str):
    """
    Uploads specification file to bucket.
    Args:
        bucket_path (str): complete file path
        commit_sha (str): git commit id
        local_file (str): path of specfile generated at local
        model (str): type of model [cdc/cde/customod]
    """
    bucket_name = bucket_path.split('/')[2]
    bucket_folder = '/'.join(bucket_path.split('/')[3:])
    files = list_files(bucket_name, bucket_folder+f'/{model}/latest')
    for file in files:
        if file.endswith('.json'):
            blob_name = '/'.join(file.split('/')[3:])
            delete_blob(bucket_name, blob_name)
    destination_blob_name = os.path.join(
        bucket_folder,
        f'{model}/latest/{model}_training_pipeline_{commit_sha}.json')
    upload_blob(bucket_name, local_file, destination_blob_name)
    destination_blob_name = os.path.join(
        bucket_folder,
        f'{model}/build/{commit_sha}/{model}_training_pipeline.json')
    upload_blob(bucket_name, local_file, destination_blob_name)

def retrieve_spec_file(bucket_path: str, file_version: str = 'latest')->str:
    """
    Retrieves specification file to bucket.
    Args:
        bucket_path (str): complete file path
        file_version (str): version of spec file[latest/commit id]
    Returns:
        files (list): List of files
    """
    gcs_uri = None
    bucket_name = bucket_path.split('/')[2]
    bucket_folder = '/'.join(bucket_path.split('/')[3:])
    if file_version == 'latest':
        files = list_files(bucket_name, os.path.join(bucket_folder, 'latest'))
        for file in files:
            if file.endswith('.json'):
                gcs_uri = file
    else:
        files = list_files(bucket_name,
                        os.path.join(bucket_folder, f'build/{file_version}'))
        for file in files:
            if file.endswith('.json'):
                gcs_uri = file
    return gcs_uri
