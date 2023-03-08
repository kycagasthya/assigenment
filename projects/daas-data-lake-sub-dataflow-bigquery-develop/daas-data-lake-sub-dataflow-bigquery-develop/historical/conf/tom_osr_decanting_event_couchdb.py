mapping_dev = [
    {
        "client": "ahold",
        "database": "ALPHA_DEV",
        "min_ts": "2020-03-27T13:39:17.630000+00:00",
        "max_ts": "2020-11-04T08:01:57.278000+00:00"
    },
    {
        "client": "kroger",
        "database": "EIGHTYONE_DEV",
        "min_ts": "2020-10-21T14:06:46.063000+00:00",
        "max_ts": "2020-11-11T22:46:32.572000+00:00"
    },
    {
        "client": "loblaws",
        "database": "LOBSTER_DEV",
        "min_ts": "2020-04-24T14:34:44.746000+00:00",
        "max_ts": "2020-11-18T16:23:46.503000+00:00"
    },
    {
        "client": "sedanos",
        "database": "SUNBIRD_DEV",
        "min_ts": "2020-04-27T19:45:56.856000+00:00",
        "max_ts": "2020-10-18T15:16:06.171000+00:00"
    },
    {
        "client": "tangerine-albertsons",
        "database": "TANGERINE_DEV",
        "min_ts": "2020-04-27T14:31:55.202000+00:00",
        "max_ts": "2020-10-27T02:16:01.743000+00:00"
    },
    {
        "client": "woolworths",
        "database": "WINGS_DEV",
        "min_ts": "2020-09-24T19:46:23.230000+00:00",
        "max_ts": "2020-11-18T05:59:50.089000+00:00"
    },
    {
        "client": "wakefern",
        "database": "WINTER_DEV",
        "min_ts": "2020-03-26T18:29:27.528151+00:00",
        "max_ts": "2020-11-04T19:03:46.911000+00:00"
    }
]

mapping_prod = [
    {
        "client": "ahold",
        "database": "ALPHA",
        "min_ts": "2020-03-27T13:39:17.630000+00:00",
        "max_ts": "2020-11-04T08:01:57.278000+00:00"
    },
    {
        "client": "kroger",
        "database": "EIGHTYONE",
        "min_ts": "2020-10-21T14:06:46.063000+00:00",
        "max_ts": "2020-11-11T22:46:32.572000+00:00"
    },
    {
        "client": "loblaws",
        "database": "LOBSTER",
        "min_ts": "2020-04-24T14:34:44.746000+00:00",
        "max_ts": "2020-11-18T16:23:46.503000+00:00"
    },
    {
        "client": "sedanos",
        "database": "SUNBIRD",
        "min_ts": "2020-04-27T19:45:56.856000+00:00",
        "max_ts": "2020-10-18T15:16:06.171000+00:00"
    },
    {
        "client": "tangerine-albertsons",
        "database": "TANGERINE",
        "min_ts": "2020-04-27T14:31:55.202000+00:00",
        "max_ts": "2020-10-27T02:16:01.743000+00:00"
    },
    {
        "client": "woolworths",
        "database": "WINGS",
        "min_ts": "2020-09-24T19:46:23.230000+00:00",
        "max_ts": "2020-11-18T05:59:50.089000+00:00"
    },
    {
        "client": "wakefern",
        "database": "WINTER",
        "min_ts": "2020-03-26T18:29:27.528151+00:00",
        "max_ts": "2020-11-04T19:03:46.911000+00:00"
    }
]

historical_sql = """copy into @json_unload_file_stage/{table}/{subdir}/{table}_json
             from (
                    select OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(
                        KEYS_TO_SNAKE(REMOVE_NULLS(doc)), 
                                  '__client_name', '{client}', true), 
                                  '__source_name', '{table}', true), 
                                  '__schema_version', 'snowflake_historical', true), 
                                  '__event_timestamp', TO_VARCHAR(created), true),
                                  '__publish_timestamp', null, true),
                                  '__ingestion_timestamp', null, true)
                    from {table}
                    where created >= to_timestamp('{min_ts}') and created < to_timestamp('{max_ts}')
                    and not (
                        IS_NULL_VALUE(doc:_id)
                        or IS_NULL_VALUE(doc:mfc)
                        or IS_NULL_VALUE(doc:licenceplate)
                        or IS_NULL_VALUE(doc:_id) is NULL
                        or IS_NULL_VALUE(doc:mfc) is NULL
                        or IS_NULL_VALUE(doc:licenceplate) is NULL
                    )
             )
                HEADER = FALSE
                OVERWRITE=TRUE"""

raw_sql = """copy into @csv_unload_file_stage/{table}/{subdir}/{table}_csv
                  from (
                        select doc
                        from {table}
                        where created >= to_timestamp('{min_ts}') and created < to_timestamp('{max_ts}')
                        and not (
                            IS_NULL_VALUE(doc:_id)
                            or IS_NULL_VALUE(doc:mfc)
                            or IS_NULL_VALUE(doc:licenceplate)
                            or IS_NULL_VALUE(doc:_id) is NULL
                            or IS_NULL_VALUE(doc:mfc) is NULL
                            or IS_NULL_VALUE(doc:licenceplate) is NULL
                        )
                  )
                    HEADER = FALSE
                    OVERWRITE=TRUE"""

schema_version = "v1"

validation_sql = """
                SELECT COUNT(*) FROM (
                SELECT dl_service.keys_to_snake(dl_service.remove_nulls(raw_data))
                FROM datalake_{client}.raw_{table}
                EXCEPT DISTINCT
                SELECT dl_service.sort_json(dl_service.remove_nulls(to_json_string(t)))
                FROM (
                SELECT * EXCEPT(__client_name, __source_name, __schema_version, __event_timestamp, __publish_timestamp, __ingest_timestamp)
                FROM datalake_{client}.{table}
                WHERE __event_timestamp >= timestamp('{min_ts}') and __event_timestamp < timestamp('{max_ts}') 
                ) t
                ) a"""