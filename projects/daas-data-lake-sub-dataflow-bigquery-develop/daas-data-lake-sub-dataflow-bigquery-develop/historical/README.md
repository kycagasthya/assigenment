# Historical data migration

This document describs how to migrate historical data per source for all clients. 

## Preparation

1. Prepare Snowflake environment by running statements within [00_snowflake_preparation.sql](preparation/00_snowflake_preparation.sql)

*Note: this step is MANDATORY to make sure that all stages linked to correct GCP project!!!!*

2. Prepare BigQuery environment by running statement within [01_bigquery_preparation.sql](preparation/01_bigquery_preparation.sql)

*Note: this step already done for both dev and prod Datalake environments*


## Usage

Steps to be followed: 

1. Log in to GCP environment under your `@takeoff.com` email in command line, like this:

```
gcloud auth login
```

2. Set default GCP project name pointing to Datalake Subscriber project:

```
gcloud config set project [PROJECT_NAME]
```

3. Set environment variables:
```
export SF_USER=[snowflake user]
export SF_PASSWORD=[snowflake password]
export SF_ACCOUNT=[snowflake account]
export SF_WAREHOUSE=[snowflake warehouse]
```

4. For specific table you need to migrate, adjust `min_ts` and `max_ts` per client.

These parameters will be handy when you try to understand what exact time period should be migrated for specific table. 

5. Run `data_migration.py` script for specific table and environment, like this:
``` 
python data_migration.py [config] [table] [env

# example for ims_balances
# python data_migration.py conf/ims_balances.py ims_balances dev
```

6. Wait some time to make sure all data is loaded to Datalake.

7. Run `data_validation.py` script for specific table and environment, like this:
``` 
python data_validation.py [config] [table] [env]

# example for ims_balances
# python data_validation.py conf/ims_balances.py ims_balances dev
```

8. When validation done, do cleanup for BigQuery (truncate or drop `raw` tables), like this:
``` 
python cleanup.py [table] [operation] [env]

# truncating all raw_ims_balances tables for all clients
# python cleanup.py raw_ims_balances truncate dev

# truncating all raw tables for all clients
# python cleanup.py all_raw truncate dev

# dropping all raw tables for all clients
# python cleanup.py all_raw drop prod
```

## Adding new table to history migration

Add configuration file with correct mapping, historical_sql, raw_sql, and validation_sql to `conf` directory. 
