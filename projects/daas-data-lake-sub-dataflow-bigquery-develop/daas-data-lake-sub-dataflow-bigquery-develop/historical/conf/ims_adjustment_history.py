mapping_dev = [
    {
        "client": "albertsons",
        "database": "ABS_DEV",
        "min_ts": "2021-11-01 00:00:00",
        "max_ts": "2021-12-01 00:00:00"
    },
    {
        "client": "ahold",
        "database": "ALPHA_DEV",
        "min_ts": "2021-11-01 00:00:00",
        "max_ts": "2021-12-01 00:00:00"
    },
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
        "min_ts": "2021-11-15T12:17:16.043486+00:00",
        "max_ts": "2022-06-16T17:47:05.929792+00:00"
    },
    {
        "client": "ahold",
        "database": "ALPHA",
        "min_ts": "2021-04-07T10:47:41.119544+00:00",
        "max_ts": "2022-06-16T17:47:08.436398+00:00"
    },
    {
        "client": "big-y",
        "database": "BLUEBERRY",
        "min_ts": "2021-04-07T15:12:17.545782+00:00",
        "max_ts": "2022-06-16T18:12:06.059405+00:00"
    },
    {
        "client": "kroger",
        "database": "EIGHTYONE",
        "min_ts": "2021-04-07T16:19:30.330213+00:00",
        "max_ts": "2022-06-16T18:12:06.983127+00:00"
    },
    {
        "client": "loblaws",
        "database": "LOBSTER",
        "min_ts": "2021-04-05T10:47:50.687661+00:00",
        "max_ts": "2022-06-16T17:47:08.094365+00:00"
    },
    {
        "client": "maf",
        "database": "MAF",
        "min_ts": "2021-04-06T15:42:20.779683+00:00",
        "max_ts": "2022-06-16T18:12:41.334439+00:00"
    },
    {
        "client": "sedanos",
        "database": "SUNBIRD",
        "min_ts": "2021-04-07T11:12:23.501106+00:00",
        "max_ts": "2022-05-06T12:12:12.738199+00:00"
    },
    {
        "client": "tangerine-albertsons",
        "database": "TANGERINE",
        "min_ts": "2021-04-05T10:47:52.877894+00:00",
        "max_ts": "2022-03-30T01:47:10.450080+00:00"
    },
    {
        "client": "woolworths",
        "database": "WINGS",
        "min_ts": "2021-04-06T16:18:01.872687+00:00",
        "max_ts": "2022-06-16T17:48:10.961416+00:00"
    },
    {
        "client": "wakefern",
        "database": "WINTER",
        "min_ts": "2021-04-07T21:19:58.277623+00:00",
        "max_ts": "2022-06-16T18:12:30.829004+00:00"
    }
]

historical_sql = """copy into @json_unload_file_stage/{table}/{subdir}/{table}_json
             from (
                    select OBJECT_DELETE(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(KEYS_TO_SNAKE(REMOVE_NULLS(ETL_DATA)),
                                      '__client_name', '{client}', true),
                                      '__source_name', '{table}', true),
                                      '__schema_version', 'snowflake_historical', true),
                                      '__event_timestamp', TO_VARCHAR(created), true),
                                      '__publish_timestamp', null, true),
                                      '__ingestion_timestamp', null, true), 'index')
                    from {table}
                    where created >= to_timestamp('{min_ts}') and created < to_timestamp('{max_ts}')
                    and not (
                            IS_NULL_VALUE(etl_data:id)
                            or IS_NULL_VALUE(etl_data:quantity)
                            or IS_NULL_VALUE(etl_data:balance_quantity_before)
                            or IS_NULL_VALUE(etl_data:product_id)
                            or IS_NULL_VALUE(etl_data:address)
                            or IS_NULL_VALUE(etl_data:location_id)
                            or IS_NULL_VALUE(etl_data:reason_code)
                            or IS_NULL_VALUE(etl_data:applied_at)
                            or IS_NULL_VALUE(etl_data:author)
                            or IS_NULL_VALUE(etl_data:command_id)
                            or IS_NULL_VALUE(etl_data:hidden)
                            or IS_NULL_VALUE(etl_data:id) is null
                            or IS_NULL_VALUE(etl_data:quantity) is null
                            or IS_NULL_VALUE(etl_data:balance_quantity_before) is null
                            or IS_NULL_VALUE(etl_data:product_id) is null
                            or IS_NULL_VALUE(etl_data:address) is null
                            or IS_NULL_VALUE(etl_data:location_id) is null
                            or IS_NULL_VALUE(etl_data:reason_code) is null
                            or IS_NULL_VALUE(etl_data:applied_at) is null
                            or IS_NULL_VALUE(etl_data:author) is null
                            or IS_NULL_VALUE(etl_data:command_id) is null
                            or IS_NULL_VALUE(etl_data:hidden) is null
                    )
            )
                HEADER = FALSE
                OVERWRITE=TRUE"""

raw_sql = """copy into @csv_unload_file_stage/{table}/{subdir}/{table}_csv
                 from (
                        select OBJECT_DELETE(ETL_DATA, 'index')
                        from {table}
                        where created >= to_timestamp('{min_ts}') and created < to_timestamp('{max_ts}')
                        and not (
                            IS_NULL_VALUE(etl_data:id)
                            or IS_NULL_VALUE(etl_data:quantity)
                            or IS_NULL_VALUE(etl_data:balance_quantity_before)
                            or IS_NULL_VALUE(etl_data:product_id)
                            or IS_NULL_VALUE(etl_data:address)
                            or IS_NULL_VALUE(etl_data:location_id)
                            or IS_NULL_VALUE(etl_data:reason_code)
                            or IS_NULL_VALUE(etl_data:applied_at)
                            or IS_NULL_VALUE(etl_data:author)
                            or IS_NULL_VALUE(etl_data:command_id)
                            or IS_NULL_VALUE(etl_data:hidden)
                            or IS_NULL_VALUE(etl_data:id) is null
                            or IS_NULL_VALUE(etl_data:quantity) is null
                            or IS_NULL_VALUE(etl_data:balance_quantity_before) is null
                            or IS_NULL_VALUE(etl_data:product_id) is null
                            or IS_NULL_VALUE(etl_data:address) is null
                            or IS_NULL_VALUE(etl_data:location_id) is null
                            or IS_NULL_VALUE(etl_data:reason_code) is null
                            or IS_NULL_VALUE(etl_data:applied_at) is null
                            or IS_NULL_VALUE(etl_data:author) is null
                            or IS_NULL_VALUE(etl_data:command_id) is null
                            or IS_NULL_VALUE(etl_data:hidden) is null
                        )        
                )
                    HEADER = FALSE
                    OVERWRITE=TRUE"""

schema_version = "v1"

validation_sql = """
                SELECT COUNT(*) FROM (
                SELECT dl_service.delete_key(dl_service.remove_nulls(dl_service.format_ts(raw_data, ['applied_at', 'expiration_date'])), ['index'])
                FROM datalake_{client}.raw_{table}
                EXCEPT DISTINCT
                SELECT dl_service.sort_json(dl_service.remove_nulls(to_json_string(t)))
                FROM (
                SELECT * EXCEPT(__client_name, __source_name, __schema_version, __event_timestamp, __publish_timestamp, __ingest_timestamp)
                FROM datalake_{client}.{table}
                WHERE __event_timestamp >= timestamp('{min_ts}') and __event_timestamp < timestamp('{max_ts}') 
                ) t
                ) a"""
