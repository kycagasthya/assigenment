"""Script for manual creation of Publisher state files based on maximum timestamp in Subscription BQ"""
import os
import sys
import argparse
import logging

from google.cloud import bigquery
from google.cloud import storage

from historical.conf.slipstick_alerts import mapping_prod as slipstick_alerts_mapping_prod

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

input_data = {'slipstick_alerts': ('created', slipstick_alerts_mapping_prod)}


def find_max_timestamps_in_subscriber_bq(work_dir, subscriber_project_id):
    """
    Searches for maximum timestamps in Subscriber BQ tables
    and saves results into output file

    :param work_dir: working dir in a local filesystem
    :param subscriber_project_id: GCP project id for Subscriber project
    :return: Output file path
    """
    bq_client = bigquery.Client()
    output_file = work_dir + 'timestamps.csv'
    for table_name, date_column_and_mappings in input_data.items():
        date_column, prod_mappings = date_column_and_mappings
        for client in prod_mappings:
            client_name = client['client']
            client_name_fixed = client_name.replace('-', '_')
            dataset = f'datalake_{client_name_fixed}'
            logging.info(f"Work with {dataset}.{table_name}")

            query = f"""
                SELECT max({date_column})
                FROM `{subscriber_project_id}.{dataset}.{table_name}`;
            """
            query_job = bq_client.query(query)

            for row in query_job:
                timestamp = row[0].strftime("%Y-%m-%dT%H:%M:%S%z")
                formatted_timestamp = "{0}:{1}".format(timestamp[:-2], timestamp[-2:])
                with open(output_file, "a") as f:
                    f.write(f"{table_name},{client_name},{formatted_timestamp}\n")
    return output_file


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the GCS bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    logging.info(f'File {source_file_name} uploaded to {destination_blob_name}.')


def create_state_files(work_dir, bucket, output_file):
    """
    Creates state files with maximum timestamps in Publisher storage state bucket

    :param work_dir: working dir in a local filesystem
    :param bucket: Publisher storage state bucket
    :param output_file: String file with maximum timestamps
    :return:
    """
    with open(output_file, "r") as f:
        lines = f.readlines()
    for line in lines:
        line_parts = line.split(',')
        file_name = "end_date.txt"
        file_full_name = work_dir + file_name
        with open(file_full_name, 'w') as f:
            to_write = line_parts[2].replace('\n', '')
            f.write(to_write)

        blob_name = f"{line_parts[0]}/{line_parts[1]}/{file_name}"

        upload_blob(bucket, file_full_name, blob_name)
        os.remove(file_full_name)


if __name__ == "__main__":
    work_dir = 'temp/'

    parser = argparse.ArgumentParser()
    parser.add_argument("sub_project_id", help="Subscriber GCP project id")
    parser.add_argument("dest_bucket", help="Destination Publisher GCS bucket")
    args, other = parser.parse_known_args()

    sub_project_id = args.sub_project_id
    dest_bucket = args.dest_bucket

    if not os.path.exists(work_dir):
        os.makedirs(work_dir)

    intermediate_file = find_max_timestamps_in_subscriber_bq(work_dir, sub_project_id)
    create_state_files(work_dir, dest_bucket, intermediate_file)
