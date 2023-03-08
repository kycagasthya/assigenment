#!/usr/bin/env python
import logging
import sys

from google.cloud import bigquery
from constants import projects, buckets

sys.path.append("")
logging.basicConfig(format='%(asctime)s,%(msecs)2d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level="INFO", stream=sys.stdout)

config = sys.argv[1]    # config path, line ims_balances/config.py
table = sys.argv[2]     # table name, like ims_balances
env = sys.argv[3]       # env name, like dev or prod

module = config.split(".")[0].replace("/", ".")
imp = __import__(module, fromlist=[module])

project = None
if env == "dev":
    mapping = imp.mapping_dev
    project = projects["dev"]
    bucket = buckets["dev"]
elif env == "stg":
    mapping = imp.mapping_dev
    project = projects["stg"]
    bucket = buckets["stg"]
elif env == "prod":
    mapping = imp.mapping_prod
    project = projects["prod"]
    bucket = buckets["prod"]
else:
    mapping = None
    logging.exception("Incorrect env. Use dev or prod.")

for map in mapping:

    client = map["client"]
    database = map["database"]
    min_ts = map["min_ts"]
    max_ts = map["max_ts"]
    subdir = min_ts.replace(" ", "T") + "_" + max_ts.replace(" ", "T")
    row_count = 0

    logging.info("Data validation for client={0}, "
          "database={1}, table={2}, min_ts={3}, max_ts={4}".format(client, database, table, min_ts, max_ts))

    # Construct a BigQuery client object.
    bq_client = bigquery.Client()

    count_validation = """
            SELECT cnt FROM (
            SELECT count(*) as cnt, '0' as idx
            FROM `{project}.datalake_{client}.raw_sf_{table}`
            UNION ALL 
            SELECT count(*) as cnt, '1' as idx
            FROM `{project}.datalake_{client}.{table}`
            WHERE __event_timestamp >= timestamp('{min_ts}') and __event_timestamp <= timestamp('{max_ts}') 
            ) as t
            ORDER BY idx 
        """.format(client=client.replace("-", "_"), min_ts=min_ts, max_ts=max_ts, project=project, table=table)

    query_job = bq_client.query(count_validation)  # Make an API request.

    logging.info("Row count validation:")
    i = 0
    for row in query_job:
        # Row values can be accessed by field name or index.
        if i == 0:
            logging.info("Row count in RAW table = {}".format(row[0]))
        elif i == 1:
            logging.info("Row count in DATA table = {}".format(row[0]))
        else:
            exit(1)
        i = i + 1

    row_by_row_validation_sql = imp.validation_sql.format(client=client.replace("-", "_"),
                                                          min_ts=min_ts,
                                                          max_ts=max_ts,
                                                          project=project,
                                                          table=table)

    query_job = bq_client.query(row_by_row_validation_sql)  # Make an API request.

    logging.info("Row by row validation data:")
    for row in query_job:
        # Row values can be accessed by field name or index.
        row_count = row[0]
        logging.info("Result rows = {}".format(row_count))

    if row_count > 0:
        logging.error("FAILED validation for client={0}, "
          "database={1}, table={2}, min_ts={3}, max_ts={4}".format(client, database, table, min_ts, max_ts))
    else:
        logging.info("SUCCESS validation for client={0}, "
          "database={1}, table={2}, min_ts={3}, max_ts={4}".format(client, database, table, min_ts, max_ts))
    logging.info("--------------------------------------------------------------------------------------------------------")
    logging.info("--------------------------------------------------------------------------------------------------------")