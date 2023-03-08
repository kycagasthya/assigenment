# Records count comparison between Snowflake and BigQuery

This document describes the technical aspects of the SF/BQ records count script.
Current script provides the validation functionality
in form of comparison the count of the last 24 hour records in the Snowflake and BigQuery tables

## Updating config file
To add or remove new retailers or/and data sources we need to modify [config.yml](src/config.yml) file.
An example of the retailer config object: 
```
  albertsons:
    bq: albertsons
    snowflake: ABS
```
where `bq` contains client name in the BigQuery and `snowflake` - the name in the Snowflake DB
An example of the data source config object: 
```
   as_users:
    bq:
      table_name: as_users
      time_column_to_filter: __ingest_timestamp
    snowflake:
      table_name: AS_USERS
      time_column_to_filter: CREATED
```
where:
- `table_name` is the name for the table in `bq` and `snowflake`
- `time_column_to_filter` is the column name to provide filtering by time in `bq` and `snowflake`

## Deployment
Currently, code and infrastructure is not triggered automatically and should be executed manually. 
## Updating Cloud Function
After adding any changes to the [config.yml](src/config.yml) or to the [script](src/main.py) logic 
we need to update the Cloud Function.
In order to do that we can use [deploy.sh](deploy.sh) bash script:
```
GCP_PROJECT_ID=... # GCP poject id (e.g. prj-daas-n-dev-dl-sub-bq-9220)
SNOWFLAKE_ACCOUNT=... # Snowflake account name (e.g. dl40731.east-us-2.azure)
SNOWFLAKE_WAREHOUSE=... # Snowflake warehouse name (e.g. QA_WH)

sh deploy.sh $GCP_PROJECT_ID $SNOWFLAKE_ACCOUNT $SNOWFLAKE_WAREHOUSE
```
## Infrastructure deployment
To be implemented using Terraform


