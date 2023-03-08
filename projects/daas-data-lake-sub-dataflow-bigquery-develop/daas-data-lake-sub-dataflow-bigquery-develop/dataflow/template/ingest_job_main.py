import argparse
import json
from typing import Dict, List, Tuple

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

from takeoff.dl.ingest.config import common, dataflow
from takeoff.dl.ingest.utils.log import CountError, LogMessage
from takeoff.dl.ingest.utils.process import (
    AddServiceCols, FormatErrorRow, FormatFailedBQRow,
    ValidateMessageContent, ValidateMessageSchema, GetTableSchema,
    fix_null_lists, pubsub_msg_to_msg_id_and_dict,
)

# Backup settings
WINDOW_SIZE = 60  # in seconds
NUM_SHARDS = 10
BATCH_SIZE = 10000


def table_fn(element: Dict) -> str:
    """
    Define dynamic table name using element's data

    :param element: PCollection element
    :return: fully-qualified BQ table name
    """
    dataset = CLIENT_BQ_CONFIG[element[common.CLIENT_FIELD].lower()]["dataset"]
    table = CLIENT_BQ_CONFIG[element[common.CLIENT_FIELD].lower()]["sources"][
        element[common.SOURCE_FIELD].lower()
    ]
    return f"{GCP_PROJECT}:{dataset}.{table}"


def generate_table_names_from_config(project_id: str, client_bq_config: dict) -> List[Tuple]:
    """
    Generates list of tuples with client-source strings and table ids
    from client config

    :param project_id: Google Cloud project id
    :param client_bq_config: input client configuration object,
        e.g. {"atb": {"dataset": "dl_atb", "sources": {"customer": "customer", "product": "product"}}}
    :return: list of tuples with client-source strings and table ids
    """
    table_names_for_clients = []
    for client_name, client_config in client_bq_config.items():
        dataset = client_config["dataset"]
        for source_name, table_name in client_config['sources'].items():
            client_source_key = f"{client_name.lower()}.{source_name.lower()}"
            table_full_name = f"{project_id}.{dataset}.{table_name}"
            table_names_for_clients.append((client_source_key, table_full_name))
    return table_names_for_clients


def run(project: str, pubsub_subscriptions: List[str], beam_args: List[str] = None):
    """
    Run Beam pipeline for each input subscription and write messages to BigQuery table

    :param project: GCP project ID
    :param pubsub_subscriptions: list of PubSub subscription short names
    :param beam_args: list of beam options as command line arguments
    """

    # Create Beam Pipeline options using input arguments and options from config.
    beam_options = PipelineOptions(beam_args, project=project, **dataflow.OPTIONS)

    # Create the Pipeline with specified options.
    with beam.Pipeline(options=beam_options) as pipeline:
        # get BigQuery tables schemas
        source_client_configs = generate_table_names_from_config(project_id=project,
                                                                 client_bq_config=CLIENT_BQ_CONFIG)
        bq_schemas = (
                pipeline
                | f"table names list from client config" >> beam.Create(source_client_configs)
                | f"get table schema" >> beam.ParDo(GetTableSchema(project_id=project))
        )

        # Read each PubSub topic separately.
        for subscription in pubsub_subscriptions:
            subscription_path = f"projects/{project}/subscriptions/{subscription}"

            # read messages from PubSub
            pubsub_data = (
                pipeline
                | f"read from {subscription}" >> beam.io.ReadFromPubSub(subscription=subscription_path,
                                                                        with_attributes=True)
            )

            # validate PubSub messages
            unvalidated_message_data = (
                pubsub_data
                | f"to json {subscription}" >> beam.Map(pubsub_msg_to_msg_id_and_dict)  # message is decoded implicitly here
                | f"log message {subscription}" >> beam.ParDo(LogMessage(subscription))  # log each message
                | f"add service cols {subscription}" >> beam.ParDo(AddServiceCols())  # add service columns to the message
                | f"validate table schema {subscription}" >> beam.ParDo(ValidateMessageSchema(subscription))  # validate message
                .with_outputs(
                    common.INVALID_RECORD, common.INVALID_RECORD_SCHEMA, main=common.VALID_RECORD  # tag outputs
                )
            )
            # fix dictionaries and validate if client is allowed to send this message
            message_data = (
                unvalidated_message_data[common.VALID_RECORD]
                | f"fix null lists {subscription}" >> beam.Map(fix_null_lists, bq_schemas=beam.pvalue.AsDict(bq_schemas))
                | f"validate {subscription}" >> beam.ParDo(ValidateMessageContent(subscription, CLIENT_BQ_CONFIG))  # validate message
                .with_outputs(
                    common.INVALID_CLIENT, common.INVALID_SOURCE, main=common.VALID_RECORD  # tag outputs
                )
            )

            # write valid messages to the target BQ table
            bq_data = (
                message_data[common.VALID_RECORD]
                | f"write to BQ {subscription}" >> beam.io.WriteToBigQuery(
                    table=table_fn,  # dynamic destination function
                    create_disposition=beam.io.BigQueryDisposition.CREATE_NEVER,  # BQ table must exist
                    write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,  # add rows
                    insert_retry_strategy=beam.io.gcp.bigquery_tools.RetryStrategy.RETRY_ON_TRANSIENT_ERROR,
                )
            )

            # reformat failed rows
            bq_failed_data = (
                bq_data[beam.io.gcp.bigquery.BigQueryWriteFn.FAILED_ROWS]
                | f"format failed bq row {subscription}" >> beam.ParDo(FormatFailedBQRow())
            )

            # merge invalid and failed rows and write them to BQ error table
            (
                (message_data[common.INVALID_CLIENT], message_data[common.INVALID_SOURCE], bq_failed_data,
                 unvalidated_message_data[common.INVALID_RECORD], unvalidated_message_data[common.INVALID_RECORD_SCHEMA])
                | f"merge errors {subscription}" >> beam.Flatten()  # merge error rows
                | f"count errors {subscription}" >> beam.ParDo(CountError(subscription))  # count errors using metric
                | f"format error row {subscription}" >> beam.ParDo(FormatErrorRow(subscription))  # format data
                | f"write error to BQ {subscription}" >> beam.io.WriteToBigQuery(
                    table=f"{GCP_PROJECT}:{common.SERVICE_DATASET}.{common.INGEST_ERRORS_TABLE}",
                    create_disposition=beam.io.BigQueryDisposition.CREATE_NEVER,  # BQ table must exist
                    write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,  # add rows
                )
            )


if __name__ == "__main__":
    # parse input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project",
        required=True,
        help="GCP project ID"
    )
    parser.add_argument(
        "--clients_config",
        required=True,
        help="Serialized clients BigQuery config dictionary",
    )
    parser.add_argument(
        "--subscriptions",
        required=True,
        help="PubSub subscriptions comma separated list",
    )

    args, beam_args = parser.parse_known_args()

    # GCP project ID
    GCP_PROJECT = args.project

    # deserialize clients BQ config dict
    CLIENT_BQ_CONFIG = json.loads(args.clients_config)

    # parse PubSub subscriptions
    subscriptions = [
        sub.strip() for sub in args.subscriptions.split(",") if sub.strip()
    ]

    run(GCP_PROJECT, subscriptions, beam_args)
