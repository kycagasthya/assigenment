mapping_dev = [
    {
        "client": "big-y",
        "database": "BLUEBERRY_DEV",
        "min_ts": "2021-11-01 00:00:00",
        "max_ts": "2021-12-01 00:00:00"
    },
    {
        "client": "kroger",
        "database": "EIGHTYONE_DEV",
        "min_ts": "2021-11-01 00:00:00",
        "max_ts": "2021-12-01 00:00:00"
    },
    {
        "client": "loblaws",
        "database": "LOBSTER_DEV",
        "min_ts": "2021-11-01 00:00:00",
        "max_ts": "2021-12-01 00:00:00"
    },
    {
        "client": "maf",
        "database": "MAF_DEV",
        "min_ts": "2021-11-01 00:00:00",
        "max_ts": "2021-12-01 00:00:00"
    },
    {
        "client": "sedanos",
        "database": "SUNBIRD_DEV",
        "min_ts": "2021-11-01 00:00:00",
        "max_ts": "2021-12-01 00:00:00"
    },
    {
        "client": "tangerine-albertsons",
        "database": "TANGERINE_DEV",
        "min_ts": "2021-11-01 00:00:00",
        "max_ts": "2021-12-01 00:00:00"
    },
    {
        "client": "woolworths",
        "database": "WINGS_DEV",
        "min_ts": "2021-11-01 00:00:00",
        "max_ts": "2021-12-01 00:00:00"
    },
    {
        "client": "wakefern",
        "database": "WINTER_DEV",
        "min_ts": "2021-11-01 00:00:00",
        "max_ts": "2021-12-01 00:00:00"
    }
]

mapping_prod = [
    {
        "client": "albertsons",
        "database": "ABS",
        "min_ts": "2021-11-16T00:01:13.900644+00:00",
        "max_ts": "2022-06-15T00:01:25.934139+00:00"
    },
    {
        "client": "ahold",
        "database": "ALPHA",
        "min_ts": "2021-04-08T00:01:20.333275+00:00",
        "max_ts": "2022-06-15T00:01:28.823389+00:00"
    },
    {
        "client": "big-y",
        "database": "BLUEBERRY",
        "min_ts": "2021-04-08T00:01:21.923099+00:00",
        "max_ts": "2022-06-15T00:01:15.867804+00:00"
    },
    {
        "client": "kroger",
        "database": "EIGHTYONE",
        "min_ts": "2021-04-08T00:01:19.979890+00:00",
        "max_ts": "2022-06-15T00:01:08.126489+00:00"
    },
    {
        "client": "loblaws",
        "database": "LOBSTER",
        "min_ts": "2021-04-05T11:37:12.261256+00:00",
        "max_ts": "2022-06-15T00:01:10.027141+00:00"
    },
    {
        "client": "maf",
        "database": "MAF",
        "min_ts": "2021-04-07T00:01:22.656820+00:00",
        "max_ts": "2022-06-15T00:01:45.990427+00:00"
    },
    {
        "client": "sedanos",
        "database": "SUNBIRD",
        "min_ts": "2021-04-08T00:01:30.506440+00:00",
        "max_ts": "2022-06-15T00:01:07.642810+00:00"
    },
    {
        "client": "tangerine-albertsons",
        "database": "TANGERINE",
        "min_ts": "2021-04-05T11:47:11.391290+00:00",
        "max_ts": "2022-04-19T00:02:02.408251+00:00"
    },
    {
        "client": "woolworths",
        "database": "WINGS",
        "min_ts": "2021-04-07T00:01:36.415572+00:00",
        "max_ts": "2022-06-15T00:01:12.240053+00:00"
    },
    {
        "client": "wakefern",
        "database": "WINTER",
        "min_ts": "2021-04-08T00:01:11.308620+00:00",
        "max_ts": "2022-06-15T00:01:17.251236+00:00"
    }
]

historical_sql = """copy into @json_unload_file_stage/{table}/{subdir}/ims_balances_json
             from (
                    select OBJECT_DELETE(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(KEYS_TO_SNAKE(ETL_DATA),
                                      '__client_name', '{client}', true),
                                      '__source_name', '{table}', true),
                                      '__schema_version', 'snowflake_historical', true),
                                      '__event_timestamp', TO_VARCHAR(created), true),
                                      '__publish_timestamp', null, true),
                                      '__ingestion_timestamp', null, true), 'index')
                    from {table}
                    where created >= to_timestamp('{min_ts}') and created < to_timestamp('{max_ts}')
                    and not (
                            IS_NULL_VALUE(etl_data:address)
                            or IS_NULL_VALUE(etl_data:last_updated)
                            or IS_NULL_VALUE(etl_data:location_id)
                            or IS_NULL_VALUE(etl_data:product_id)
                            or IS_NULL_VALUE(etl_data:quantity)
                            or IS_NULL_VALUE(etl_data:address) is null
                            or IS_NULL_VALUE(etl_data:last_updated) is null
                            or IS_NULL_VALUE(etl_data:location_id) is null
                            or IS_NULL_VALUE(etl_data:product_id) is null
                            or IS_NULL_VALUE(etl_data:quantity) is null
                            )
                )
                HEADER = FALSE
                OVERWRITE=TRUE"""

raw_sql = """copy into @csv_unload_file_stage/{table}/{subdir}/ims_balances_csv
                 from (
                        select OBJECT_DELETE(ETL_DATA, 'index')
                        from {table}
                        where created >= to_timestamp('{min_ts}') and created < to_timestamp('{max_ts}')
                        and not (
                            IS_NULL_VALUE(etl_data:address)
                            or IS_NULL_VALUE(etl_data:last_updated)
                            or IS_NULL_VALUE(etl_data:location_id)
                            or IS_NULL_VALUE(etl_data:product_id)
                            or IS_NULL_VALUE(etl_data:quantity)
                            or IS_NULL_VALUE(etl_data:address) is null
                            or IS_NULL_VALUE(etl_data:last_updated) is null
                            or IS_NULL_VALUE(etl_data:location_id) is null
                            or IS_NULL_VALUE(etl_data:product_id) is null
                            or IS_NULL_VALUE(etl_data:quantity) is null
                            )
                    )
                    HEADER = FALSE
                    OVERWRITE=TRUE"""

schema_version = "v1"

validation_sql = """
                SELECT COUNT(*) FROM (
                SELECT dl_service.delete_key(dl_service.remove_nulls(dl_service.format_ts(raw_data, ['last_updated'])), ['index'])
                FROM datalake_{client}.raw_{table}
                EXCEPT DISTINCT
                SELECT dl_service.sort_json(dl_service.remove_nulls(to_json_string(t)))
                FROM (
                SELECT * EXCEPT(__client_name, __source_name, __schema_version, __event_timestamp, __publish_timestamp, __ingest_timestamp)
                FROM datalake_{client}.{table}
                WHERE __event_timestamp >= timestamp('{min_ts}') and __event_timestamp < timestamp('{max_ts}') 
                ) t
                ) a"""
