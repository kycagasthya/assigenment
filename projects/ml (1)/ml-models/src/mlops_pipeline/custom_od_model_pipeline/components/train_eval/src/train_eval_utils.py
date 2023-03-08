# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.
# ==============================================================================

"""This module will contail util functions for train_eval"""

from google.cloud import storage
from custlogger import ml_logger
import traceback
client = storage.Client()

def file_exist(path: str):
    """
    find best checkpoint from trained ckpt files
    Parameters:
    ----------
    path : str
        pipeline config path
    Returns
    -------
    boolean
        file exist or not

    """
    try:
        bucket_name = path.split("/")[2]
        file_name = "/".join(path.split("/")[3:])
        bucket = client.bucket(bucket_name)
        stats = storage.Blob(bucket=bucket, name=file_name).exists(client)
        return stats
    except Exception:
        ml_logger(type_log="ERROR", component="Custom OD-train_eval",
                  message="Exception in file_exist",
                  status_code="500", traceback=traceback.format_exc())
        raise

def delete_blob(bucket_name, blob_name):
    """
    Deletes a blob from the bucket.
    bucket_name = "your-bucket-name"
    blob_name = "your-object-name"
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()
