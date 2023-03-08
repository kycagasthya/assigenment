mapping_dev = [
    {
        "client": "albertsons",
        "database": "ABS_DEV",
        "min_ts": "2022-02-08T11:25:13.875000+00:00",
        "max_ts": "2022-08-02T13:00:05.404000+00:00"
    },
    {
        "client": "ahold",
        "database": "ALPHA_DEV",
        "min_ts": "2022-02-08T11:24:52.430000+00:00",
        "max_ts": "2022-07-22T12:00:05.125000+00:00"
    },
    {
        "client": "big-y",
        "database": "BLUEBERRY_DEV",
        "min_ts": "2022-02-08T11:23:57.300000+00:00",
        "max_ts": "2022-07-22T12:00:04.258000+00:00"
    },
    {
        "client": "kroger",
        "database": "EIGHTYONE_DEV",
        "min_ts": "2022-02-08T11:23:09.491000+00:00",
        "max_ts": "2022-08-04T13:00:04.877000+00:00"
    },
    {
        "client": "loblaws",
        "database": "LOBSTER_DEV",
        "min_ts": "2022-02-08T11:24:29.199000+00:00",
        "max_ts": "2022-08-02T11:00:04.535000+00:00"
    },
    {
        "client": "maf",
        "database": "MAF_DEV",
        "min_ts": "2022-02-08T11:25:14.095000+00:00",
        "max_ts": "2022-07-22T12:00:07.886000+00:00"
    },
    {
        "client": "woolworths",
        "database": "WINGS_DEV",
        "min_ts": "2022-02-08T11:23:05.886000+00:00",
        "max_ts": "2022-07-27T09:00:07.634000+00:00"
    },
    {
        "client": "wakefern",
        "database": "WINTER_DEV",
        "min_ts": "2022-02-08T11:24:32.738000+00:00",
        "max_ts": "2022-07-21T11:00:05.074000+00:00"
    },
    {
        'client': 'tangerine-albertsons',
        'database': 'TANGERINE_DEV',
        'min_ts': '2022-02-08T11:23:40.417000+00:00',
        'max_ts': '2022-04-18T21:00:10.861000+00:00'
    }
]

mapping_prod = [
    {
        "client": "albertsons",
        "database": "ABS",
        "min_ts": "2022-02-08T11:25:13.875000+00:00",
        "max_ts": "2022-08-05T11:00:04.940000+00:00"
    },
    {
        "client": "ahold",
        "database": "ALPHA",
        "min_ts": "2022-02-08T11:24:52.430000+00:00",
        "max_ts": "2022-08-05T11:00:06.088000+00:00"
    },
    {
        "client": "big-y",
        "database": "BLUEBERRY",
        "min_ts": "2022-02-08T11:23:57.300000+00:00",
        "max_ts": "2022-08-05T11:00:05.167000+00:00"
    },
    {
        "client": "kroger",
        "database": "EIGHTYONE",
        "min_ts": "2022-02-08T11:23:09.491000+00:00",
        "max_ts": "2022-08-05T11:00:04.859000+00:00"
    },
    {
        "client": "loblaws",
        "database": "LOBSTER",
        "min_ts": "2022-02-08T11:24:29.199000+00:00",
        "max_ts": "2022-08-05T11:00:04.780000+00:00"
    },
    {
        "client": "maf",
        "database": "MAF",
        "min_ts": "2022-02-08T11:25:14.095000+00:00",
        "max_ts": "2022-08-05T11:00:08.034000+00:00"
    },
    {
        "client": "woolworths",
        "database": "WINGS",
        "min_ts": "2022-02-08T11:23:05.886000+00:00",
        "max_ts": "2022-08-05T11:00:07.906000+00:00"
    },
    {
        "client": "wakefern",
        "database": "WINTER",
        "min_ts": "2022-02-08T11:24:32.738000+00:00",
        "max_ts": "2022-08-05T11:00:05.035000+00:00"
    },
    {
        'client': 'tangerine-albertsons',
        'database': 'TANGERINE',
        'min_ts': '2022-02-08T11:23:40.417000+00:00',
        'max_ts': '2022-04-18T21:00:10.861000+00:00'
    }
]

historical_sql = """copy into @json_unload_file_stage/{table}/{subdir}/{table}_json
             from (
                    select OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(KEYS_TO_SNAKE(REMOVE_NULLS(doc)),
                                      '__client_name', '{client}', true), 
                                      '__source_name', '{table}', true), 
                                      '__schema_version', 'snowflake_historical', true), 
                                      '__event_timestamp', TO_VARCHAR(created), true),
                                      '__publish_timestamp', current_timestamp(), true),
                                      '__ingest_timestamp', current_timestamp(), true)
                    from {table}
                    where created >= to_timestamp('{min_ts}') and created <= to_timestamp('{max_ts}')
                    and not (
                            IS_NULL_VALUE(doc:"created")
                            or IS_NULL_VALUE(doc:"is-disabled")
                            or IS_NULL_VALUE(doc:"is-email-verified")
                            or IS_NULL_VALUE(doc:"user-id")
                            or IS_NULL_VALUE(doc:"roles")
                    )
                )
                HEADER = FALSE
                OVERWRITE=TRUE"""

raw_sql = """copy into @csv_unload_file_stage/{table}/{subdir}/{table}_csv
                 from (
                        select doc
                        from {table}
                        where created >= to_timestamp('{min_ts}') and created <= to_timestamp('{max_ts}')
                        and not (
                            IS_NULL_VALUE(doc:"created")
                            or IS_NULL_VALUE(doc:"is-disabled")
                            or IS_NULL_VALUE(doc:"is-email-verified")
                            or IS_NULL_VALUE(doc:"user-id")
                            or IS_NULL_VALUE(doc:"roles")
                        )
                    )
                    HEADER = FALSE
                    OVERWRITE=TRUE"""

schema_version = "v1"

validation_sql = """
                SELECT COUNT(*) FROM (
                SELECT dl_service.remove_nulls(dl_service.format_ts(dl_service.keys_to_snake(raw_data),
                      ['created',
                      'last_refresh',
                      'last_sign_in'])),
                FROM `{project}.datalake_{client}.raw_sf_{table}`
                EXCEPT DISTINCT
                SELECT dl_service.sort_json(dl_service.remove_nulls(to_json_string(t)))
                FROM (
                SELECT * EXCEPT(__client_name, 
                __source_name, 
                __schema_version, 
                __event_timestamp, 
                __publish_timestamp, 
                __ingest_timestamp)
                FROM datalake_{client}.{table}
                WHERE __event_timestamp >= timestamp('{min_ts}') and __event_timestamp <= timestamp('{max_ts}') 
                ) t
                ) a"""
