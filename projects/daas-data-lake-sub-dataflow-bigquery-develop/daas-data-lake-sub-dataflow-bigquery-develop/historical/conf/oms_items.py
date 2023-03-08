mapping_dev = [
    {
        "client": "albertsons",
        "database": "ABS_DEV",
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
        "min_ts": "2021-11-15T12:37:10.385626+00:00",
        "max_ts": "2022-06-08T14:07:06.235293+00:00"
    },
    {
        "client": "big-y",
        "database": "BLUEBERRY",
        "min_ts": "2021-04-01T20:27:20.743822+00:00",
        "max_ts": "2022-06-08T13:57:07.497533+00:00"
    },
    {
        "client": "kroger",
        "database": "EIGHTYONE",
        "min_ts": "2021-05-18T21:27:25.564792+00:00",
        "max_ts": "2022-06-08T13:57:05.587864+00:00"
    },
    {
        "client": "loblaws",
        "database": "LOBSTER",
        "min_ts": "2020-04-24T14:32:16.065000+00:00",
        "max_ts": "2022-06-08T13:54:06.564306+00:00"
    },
    {
        "client": "maf",
        "database": "MAF",
        "min_ts": "2021-02-11T18:27:19.330539+00:00",
        "max_ts": "2022-06-08T13:57:11.904279+00:00"
    },
    {
        "client": "sedanos",
        "database": "SUNBIRD",
        "min_ts": "2020-10-01T20:27:43.688675+00:00",
        "max_ts": "2022-01-21T19:21:12.649575+00:00"
    },
    {
        "client": "tangerine-albertsons",
        "database": "TANGERINE",
        "min_ts": "2020-05-22T11:11:50.782237+00:00",
        "max_ts": "2022-03-30T00:37:17.515930+00:00"
    },
    {
        "client": "woolworths",
        "database": "WINGS",
        "min_ts": "2020-09-25T17:59:42.439268+00:00",
        "max_ts": "2022-06-08T13:46:32.851127+00:00"
    },
    {
        "client": "wakefern",
        "database": "WINTER",
        "min_ts": "2020-03-18T12:57:09.827000+00:00",
        "max_ts": "2022-06-08T14:01:09.362457+00:00"
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
                            or IS_NULL_VALUE(etl_data:takeoff_item_id)
                            or IS_NULL_VALUE(etl_data:requested_quantity)
                            or IS_NULL_VALUE(etl_data:line_id)
                            or IS_NULL_VALUE(etl_data:id) is null
                            or IS_NULL_VALUE(etl_data:takeoff_item_id) is null
                            or IS_NULL_VALUE(etl_data:requested_quantity) is null
                            or IS_NULL_VALUE(etl_data:line_id) is null
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
                            or IS_NULL_VALUE(etl_data:takeoff_item_id)
                            or IS_NULL_VALUE(etl_data:requested_quantity)
                            or IS_NULL_VALUE(etl_data:line_id)
                            or IS_NULL_VALUE(etl_data:id) is null
                            or IS_NULL_VALUE(etl_data:takeoff_item_id) is null
                            or IS_NULL_VALUE(etl_data:requested_quantity) is null
                            or IS_NULL_VALUE(etl_data:line_id) is null
                            )
                    )
                    HEADER = FALSE
                    OVERWRITE=TRUE"""

schema_version = "v1"

validation_sql = """
                SELECT COUNT(*) FROM (
                SELECT dl_service.delete_key(dl_service.remove_nulls(dl_service.format_ts(raw_data, ['creation_datetime', 'last_modified'])), ['index'])
                FROM datalake_{client}.raw_{table}
                EXCEPT DISTINCT
                SELECT dl_service.sort_json(dl_service.remove_nulls(to_json_string(t)))
                FROM (
                SELECT * EXCEPT(__client_name, __source_name, __schema_version, __event_timestamp, __publish_timestamp, __ingest_timestamp)
                FROM datalake_{client}.{table}
                WHERE __event_timestamp >= timestamp('{min_ts}') and __event_timestamp < timestamp('{max_ts}') 
                ) t
                ) a"""
