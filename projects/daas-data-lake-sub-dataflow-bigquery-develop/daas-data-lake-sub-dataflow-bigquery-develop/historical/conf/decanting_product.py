mapping_dev = [
    {
        "client": "albertsons",
        "database": "ABS_DEV",
        "min_ts": "2022-04-25T00:00:00.000000+00:00",
        "max_ts": "2022-05-25T07:57:06.109822+00:00"
    },
    {
        "client": "ahold",
        "database": "ALPHA_DEV",
        "min_ts": "2022-04-17T00:00:00.000000+00:00",
        "max_ts": "2022-05-17T07:57:07.919824+00:00"
    },
    {
        "client": "big-y",
        "database": "BLUEBERRY_DEV",
        "min_ts": "2022-06-04T00:00:00.000000+00:00",
        "max_ts": "2022-07-04T14:27:06.655856+00:00"
    },
    {
        "client": "kroger",
        "database": "EIGHTYONE_DEV",
        "min_ts": "2022-04-17T00:00:00.000000+00:00",
        "max_ts": "2022-05-17T04:57:06.274217+00:00"
    },
    {
        "client": "loblaws",
        "database": "LOBSTER_DEV",
        "min_ts": "2022-04-17T00:00:00.000000+00:00",
        "max_ts": "2022-05-17T09:57:04.735370+00:00"
    },
    {
        "client": "maf",
        "database": "MAF_DEV",
        "min_ts": "2022-04-17T00:00:00.000000+00:00",
        "max_ts": "2022-05-17T09:57:11.171686+00:00"
    },
    {
        "client": "sedanos",
        "database": "SUNBIRD_DEV",
        "min_ts": "2021-12-15T00:00:00.000000+00:00",
        "max_ts": "2022-01-20T16:27:13.773342+00:00"
    },
    {
        "client": "tangerine-albertsons",
        "database": "TANGERINE_DEV",
        "min_ts": "2022-02-19T00:00:00.000000+00:00",
        "max_ts": "2022-03-29T20:57:11.969609+00:00"
    },
    {
        "client": "woolworths",
        "database": "WINGS_DEV",
        "min_ts": "2022-01-23T00:00:00.000000+00:00",
        "max_ts": "2022-02-23T15:27:27.697560+00:00"
    },
    {
        "client": "wakefern",
        "database": "WINTER_DEV",
        "min_ts": "2022-04-17T00:00:00.000000+00:00",
        "max_ts": "2022-05-17T08:27:10.128429+00:00"
    }
]

mapping_prod = [
    {
        "client": "albertsons",
        "database": "ABS",
        "min_ts": "2021-11-17T15:42:07.947043+00:00",
        "max_ts": "2022-08-01T17:42:06.647286+00:00"
    },
    {
        "client": "ahold",
        "database": "ALPHA",
        "min_ts": "2020-11-09T13:45:14.561533+00:00",
        "max_ts": "2022-08-01T17:42:08.245181+00:00"
    },
    {
        "client": "big-y",
        "database": "BLUEBERRY",
        "min_ts": "2021-03-29T19:27:18.361486+00:00",
        "max_ts": "2022-08-01T17:42:06.108544+00:00"
    },
    {
        "client": "kroger",
        "database": "EIGHTYONE",
        "min_ts": "2020-11-18T14:42:16.257397+00:00",
        "max_ts": "2022-08-01T04:42:05.724103+00:00"
    },
    {
        "client": "loblaws",
        "database": "LOBSTER",
        "min_ts": "2020-11-30T18:27:17.196429+00:00",
        "max_ts": "2022-08-01T00:27:03.825202+00:00"
    },
    {
        "client": "maf",
        "database": "MAF",
        "min_ts": "2021-02-02T03:27:11.510580+00:00",
        "max_ts": "2022-08-01T17:42:13.017866+00:00"
    },
    {
        "client": "sedanos",
        "database": "SUNBIRD",
        "min_ts": "2020-11-09T13:45:17.630329+00:00",
        "max_ts": "2022-01-20T16:27:13.773342+00:00"
    },
    {
        "client": "tangerine-albertsons",
        "database": "TANGERINE",
        "min_ts": "2020-11-09T13:45:19.491660+00:00",
        "max_ts": "2022-03-29T20:57:11.969609+00:00"
    },
    {
        "client": "woolworths",
        "database": "WINGS",
        "min_ts": "2020-11-18T21:42:14.309032+00:00",
        "max_ts": "2022-08-01T17:42:18.906139+00:00"
    },
    {
        "client": "wakefern",
        "database": "WINTER",
        "min_ts": "2020-11-09T13:45:08.637568+00:00",
        "max_ts": "2022-08-01T17:42:09.320455+00:00"
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
                        or IS_NULL_VALUE(etl_data:task_id)
                        or IS_NULL_VALUE(etl_data:product)
                        or IS_NULL_VALUE(etl_data:description)
                        or IS_NULL_VALUE(etl_data:date_received)
                        or IS_NULL_VALUE(etl_data:qty)
                        or IS_NULL_VALUE(etl_data:qty_decanted)
                        or IS_NULL_VALUE(etl_data:units)
                        or IS_NULL_VALUE(etl_data:id) is NULL
                        or IS_NULL_VALUE(etl_data:task_id) is NULL
                        or IS_NULL_VALUE(etl_data:product) is NULL
                        or IS_NULL_VALUE(etl_data:description) is NULL
                        or IS_NULL_VALUE(etl_data:date_received) is NULL
                        or IS_NULL_VALUE(etl_data:qty) is NULL
                        or IS_NULL_VALUE(etl_data:qty_decanted) is NULL
                        or IS_NULL_VALUE(etl_data:units) is NULL
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
                            or IS_NULL_VALUE(etl_data:task_id)
                            or IS_NULL_VALUE(etl_data:product)
                            or IS_NULL_VALUE(etl_data:description)
                            or IS_NULL_VALUE(etl_data:date_received)
                            or IS_NULL_VALUE(etl_data:qty)
                            or IS_NULL_VALUE(etl_data:qty_decanted)
                            or IS_NULL_VALUE(etl_data:units)
                            or IS_NULL_VALUE(etl_data:id) is NULL
                            or IS_NULL_VALUE(etl_data:task_id) is NULL
                            or IS_NULL_VALUE(etl_data:product) is NULL
                            or IS_NULL_VALUE(etl_data:description) is NULL
                            or IS_NULL_VALUE(etl_data:date_received) is NULL
                            or IS_NULL_VALUE(etl_data:qty) is NULL
                            or IS_NULL_VALUE(etl_data:qty_decanted) is NULL
                            or IS_NULL_VALUE(etl_data:units) is NULL
                        )
                    )
                    HEADER = FALSE
                    OVERWRITE=TRUE"""

schema_version = "v1"

validation_sql = """
                SELECT COUNT(*) FROM (
                SELECT dl_service.delete_key(dl_service.remove_nulls(dl_service.format_ts(raw_data, ['date_received', 'last_modified'])), ['index'])
                FROM datalake_{client}.raw_{table}
                EXCEPT DISTINCT
                SELECT dl_service.sort_json(dl_service.remove_nulls(to_json_string(t)))
                FROM (
                SELECT * EXCEPT(__client_name, __source_name, __schema_version, __event_timestamp, __publish_timestamp, __ingest_timestamp)
                FROM datalake_{client}.{table}
                WHERE __event_timestamp >= timestamp('{min_ts}') and __event_timestamp < timestamp('{max_ts}') 
                ) t
                ) a"""
