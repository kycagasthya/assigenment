#!/usr/bin/env python
# Usage: cleanup.py [table_name] [operation] [env]
# example: cleanup.py raw_ims_balances truncate dev
import logging
import sys

from google.cloud import bigquery
from constants import projects, buckets, clients

logging.basicConfig(format='%(asctime)s,%(msecs)2d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level="INFO", stream=sys.stdout)

table_to_cleanup = sys.argv[1]     # table name
operation = sys.argv[2]  # truncate or drop
env = sys.argv[3]       # env name, like dev or prod

if env == "dev":
    project = projects["dev"]
    bucket = buckets["dev"]
elif env == "stg":
    project = projects["stg"]
    bucket = buckets["stg"]
elif env == "prod":
    project = projects["prod"]
    bucket = buckets["prod"]
else:
    mapping = None
    logging.exception("Incorrect environment. Use dev or prod.")

if operation == "truncate":
    cleanup_sql = "truncate table `{table_id}`"
elif operation == "drop":
    cleanup_sql = "drop table if exists `{table_id}`"
else:
    cleanup_sql = None
    logging.exception("Invalid cleanup operation")

# Construct a BigQuery client object.
bq_client = bigquery.Client(project=project)

for client in clients:
    if table_to_cleanup == "all_raw":
        dataset_id = "datalake_{client}".format(client=client.replace("-", "_"))
        tables = bq_client.list_tables(dataset_id)

        for table in tables:
            if table.table_id.startswith("raw_"):
                table_id = "{}.{}.{}".format(table.project, table.dataset_id, table.table_id)

                logging.info("Cleanup operation for table {table_id} is {operation}".format(table_id=table_id, operation=operation.upper()))
                query_job = bq_client.query(cleanup_sql.format(table_id=table_id))
                logging.info("Cleanup done for table {table_id}".format(table_id=table_id))
            else:
                continue
    else:
        table_id = "{project}.datalake_{client}.{table}".format(project=project, client=client.replace("-", "_"),
                                                                        table=table_to_cleanup)

        logging.info("Cleanup operation for table {table_id} is {operation}".format(table_id=table_id,
                                                                                    operation=operation.upper()))
        query_job = bq_client.query(cleanup_sql.format(table_id=table_id))
        logging.info("Cleanup done for table {table_id}".format(table_id=table_id))

logging.info("Script completed.")