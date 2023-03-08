#!/usr/bin/env python
import logging
import os
import sys
import snowflake.connector

from google.cloud import bigquery

from constants import projects, buckets

SF_USER = os.getenv('SF_USER')
SF_PASSWORD = os.getenv('SF_PASSWORD')
SF_ACCOUNT = os.getenv('SF_ACCOUNT')
SF_WAREHOUSE = os.getenv('SF_WAREHOUSE')
SF_ENV = os.getenv('SF_ENV')

sys.path.append("")
logging.basicConfig(format='%(asctime)s,%(msecs)2d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level="INFO", stream=sys.stdout)

config = sys.argv[1]  # config path, line ims_balances/config.py
table = sys.argv[2]  # table name, like ims_balances
env = sys.argv[3]  # env name, like dev or prod

module = config.split(".")[0].replace("/", ".")
imp = __import__(module, fromlist=[module])

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
    logging.exception("Incorrect environment. Use dev or prod.")

# Gets the version
conn = snowflake.connector.connect(
    user=SF_USER,
    password=SF_PASSWORD,
    account=SF_ACCOUNT,
    warehouse=SF_WAREHOUSE
)

for map in mapping:

    client = map["client"]
    database = map["database"]
    min_ts = map["min_ts"]
    max_ts = map["max_ts"]
    subdir = min_ts.replace(" ", "T") + "_" + max_ts.replace(" ", "T")
    json_unload_file_stage = map.get("json_unload_file_stage", "json_unload_file_stage")
    csv_unload_file_stage = map.get("csv_unload_file_stage", "csv_unload_file_stage")

    historical_sql = imp.historical_sql.format(client=client, min_ts=min_ts, max_ts=max_ts, table=table,
                                               subdir=subdir, json_unload_file_stage=json_unload_file_stage)
    raw_sql = imp.raw_sql.format(min_ts=min_ts, max_ts=max_ts, table=table, subdir=subdir,
                                 csv_unload_file_stage=csv_unload_file_stage)

    cs = conn.cursor()
    cs.execute("USE ROLE ETL_ROLE")
    cs.execute("USE DATABASE {0}".format(database))
    cs.execute("USE SCHEMA DATA_LAKE")
    cs.execute("alter session set timestamp_output_format = 'YYYY-MM-DDTHH24:MI:SS.FF6TZH:TZM'")
    cs.execute("alter session set timestamp_input_format = 'YYYY-MM-DDTHH24:MI:SS.FF6TZH:TZM'")
    cs.execute("alter session set timezone = 'UTC'")

    try:
        logging.info("STEP 1: Running FORMATTED data export for client={0}, "
                     "database={1}, table={2}, min_ts={3}, max_ts={4}".format(client, database, table, min_ts, max_ts))
        cs.execute(historical_sql)
        result = cs.fetchone()
        logging.info("Rows unloaded: {0}, input bytes: {1}, output bytes: {2}".format(result[0], result[1], result[2]))
        if result[0] == 0:
            logging.info("Nothing exported for client={0}, "
                         "database={1}, table={2}, min_ts={3}, max_ts={4}".format(client, database, table, min_ts,
                                                                                  max_ts))
            logging.info("Skipping STEP 2, STEP 3, STEP 4 and going to next client")
            logging.info(
                "-----------------------------------------------------------------------------------------------------------")
            logging.info(
                "-----------------------------------------------------------------------------------------------------------")
            continue

        logging.info("STEP 2: Running RAW data export for client={0}, "
                     "database={1}, table={2}, min_ts={3}, max_ts={4}".format(client, database, table, min_ts, max_ts))
        cs.execute(raw_sql)
        result = cs.fetchone()
        logging.info("Rows unloaded: {0}, input bytes: {1}, output bytes: {2}".format(result[0], result[1], result[2]))
    finally:
        cs.close()

    logging.info("STEP 3: Loading FORMATTED data for client={0}, "
                 "database={1}, table={2}, min_ts={3}, max_ts={4}".format(client, database, table, min_ts, max_ts))

    # Construct a BigQuery client object.
    bq_client = bigquery.Client(project=project)

    table_id = "{project}.datalake_{client}.{table}".format(project=project, client=client.replace("-", "_"),
                                                            table=table)
    table_schema = bq_client.get_table(table_id).schema  # API Request

    job_config = bigquery.LoadJobConfig(
        schema=table_schema,
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    )

    uri = "gs://{bucket}/{database}/{table}/{subdir}/{table}_json_*.json.gz".format(bucket=bucket,
                                                                                    database=database,
                                                                                    table=table,
                                                                                    subdir=subdir)
    load_job = bq_client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )  # Make an API request.

    load_job.result()  # Waits for the job to complete.

    logging.info("Loaded rows: {0}, loaded bytes: {1}".format(load_job.output_rows, load_job.output_bytes))

    logging.info("STEP 4: Loading RAW data for validation for client={0}, "
                 "database={1}, table={2}, min_ts={3}, max_ts={4}".format(client, database, table, min_ts, max_ts))

    # Construct a BigQuery client object.
    bq_client = bigquery.Client(project=project)

    table_id = "{project}.datalake_{client}.raw_sf_{table}".format(project=project, client=client.replace("-", "_"),
                                                                table=table)

    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("raw_data", "STRING")
        ],
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        source_format=bigquery.SourceFormat.CSV
    )

    uri = "gs://{bucket}/{database}/csv/{table}/{subdir}/{table}_csv_*".format(bucket=bucket, database=database,
                                                                               table=table, subdir=subdir)
    load_job = bq_client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )  # Make an API request.

    load_job.result()  # Waits for the job to complete.

    destination_table = bq_client.get_table(table_id)
    logging.info("Loaded {} rows.".format(destination_table.num_rows))

    logging.info("Processing completed for client={0}, "
                 "database={1}, table={2}, min_ts={3}, max_ts={4}".format(client, database, table, min_ts, max_ts))
    logging.info(
        "-----------------------------------------------------------------------------------------------------------")
    logging.info(
        "-----------------------------------------------------------------------------------------------------------")

conn.close()
