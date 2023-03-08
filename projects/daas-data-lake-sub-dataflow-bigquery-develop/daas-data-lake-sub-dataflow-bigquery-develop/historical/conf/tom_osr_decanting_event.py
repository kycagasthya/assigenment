mapping_dev = [
    {
        "client": "albertsons",
        "database": "ABS_DEV",
        "min_ts": "2021-11-19T01:26:11.723810+00:00",
        "max_ts": "2022-08-02T13:26:05.194540+00:00"
    },
    {
        "client": "ahold",
        "database": "ALPHA_DEV",
        "min_ts": "2020-11-06T21:45:13.905814+00:00",
        "max_ts": "2022-07-22T11:56:04.864976+00:00"
    },
    {
        "client": "big-y",
        "database": "BLUEBERRY_DEV",
        "min_ts": "2021-04-01T20:11:21.006946+00:00",
        "max_ts": "2022-07-22T11:56:04.432038+00:00"
    },
    {
        "client": "kroger",
        "database": "EIGHTYONE_DEV",
        "min_ts": "2020-11-16T19:56:14.482092+00:00",
        "max_ts": "2022-07-21T06:41:05.897094+00:00"
    },
    {
        "client": "loblaws",
        "database": "LOBSTER_DEV",
        "min_ts": "2020-11-19T18:41:12.586325+00:00",
        "max_ts": "2022-08-02T10:56:03.938168+00:00"
    },
    {
        "client": "maf",
        "database": "MAF_DEV",
        "min_ts": "2021-02-10T22:26:22.214472+00:00",
        "max_ts": "2022-07-22T12:26:06.771940+00:00"
    },
    {
        "client": "sedanos",
        "database": "SUNBIRD_DEV",
        "min_ts": "2020-11-04T14:08:25.434319+00:00",
        "max_ts": "2022-01-20T16:26:08.735538+00:00"
    },
    {
        "client": "tangerine-albertsons",
        "database": "TANGERINE_DEV",
        "min_ts": "2020-11-06T16:30:16.522656+00:00",
        "max_ts": "2022-03-29T20:56:10.693866+00:00"
    },
    {
        "client": "woolworths",
        "database": "WINGS_DEV",
        "min_ts": "2020-11-18T21:41:12.761232+00:00",
        "max_ts": "2022-07-27T08:56:07.677100+00:00"
    },
    {
        "client": "wakefern",
        "database": "WINTER_DEV",
        "min_ts": "2020-11-09T19:15:09.823304+00:00",
        "max_ts": "2022-07-21T10:56:05.063644+00:00"
    }
]

mapping_prod = [
    {
        "client": "albertsons",
        "database": "ABS",
        "min_ts": "2021-11-19T01:26:11.723810+00:00",
        "max_ts": "2022-08-04T17:56:05.717204+00:00"
    },
    {
        "client": "ahold",
        "database": "ALPHA",
        "min_ts": "2020-11-06T21:45:13.905814+00:00",
        "max_ts": "2022-08-04T17:56:05.612262+00:00"
    },
    {
        "client": "big-y",
        "database": "BLUEBERRY",
        "min_ts": "2021-04-01T20:11:21.006946+00:00",
        "max_ts": "2022-08-04T14:56:04.750116+00:00"
    },
    {
        "client": "kroger",
        "database": "EIGHTYONE",
        "min_ts": "2020-11-16T19:56:14.482092+00:00",
        "max_ts": "2022-08-04T06:11:05.105863+00:00"
    },
    {
        "client": "loblaws",
        "database": "LOBSTER",
        "min_ts": "2020-11-19T18:41:12.586325+00:00",
        "max_ts": "2022-08-04T17:26:05.593275+00:00"
    },
    {
        "client": "maf",
        "database": "MAF",
        "min_ts": "2021-02-10T22:26:22.214472+00:00",
        "max_ts": "2022-08-04T17:56:07.023887+00:00"
    },
    {
        "client": "sedanos",
        "database": "SUNBIRD",
        "min_ts": "2020-11-04T14:08:25.434319+00:00",
        "max_ts": "2022-01-20T16:26:08.735538+00:00"
    },
    {
        "client": "tangerine-albertsons",
        "database": "TANGERINE",
        "min_ts": "2020-11-06T16:30:16.522656+00:00",
        "max_ts": "2022-03-29T20:56:10.693866+00:00"
    },
    {
        "client": "woolworths",
        "database": "WINGS",
        "min_ts": "2020-11-18T21:41:12.761232+00:00",
        "max_ts": "2022-08-04T17:56:06.701538+00:00"
    },
    {
        "client": "wakefern",
        "database": "WINTER",
        "min_ts": "2020-11-09T19:15:09.823304+00:00",
        "max_ts": "2022-08-04T17:56:05.594814+00:00"
    }
]

historical_sql = """copy into @json_unload_file_stage/{table}/{subdir}/{table}_json
             from (
                    select OBJECT_DELETE(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(
                        KEYS_TO_SNAKE(REMOVE_NULLS(ETL_DATA)), 
                                  '__client_name', '{client}', true), 
                                  '__source_name', '{table}', true), 
                                  '__schema_version', 'snowflake_historical', true), 
                                  '__event_timestamp', TO_VARCHAR(created), true),
                                  '__publish_timestamp', null, true),
                                  '__ingestion_timestamp', null, true),
                                  '_rev','',true),
                                  'wpno','',true),'index')
                    from {table}
                    where created >= to_timestamp('{min_ts}') and created < to_timestamp('{max_ts}')
                    and not (
                        IS_NULL_VALUE(etl_data:_id)
                        or IS_NULL_VALUE(etl_data:created)
                        or IS_NULL_VALUE(etl_data:mfc)
                        or IS_NULL_VALUE(etl_data:licenceplate)
                        or IS_NULL_VALUE(etl_data:_id) is NULL
                        or IS_NULL_VALUE(etl_data:created) is NULL
                        or IS_NULL_VALUE(etl_data:mfc) is NULL
                        or IS_NULL_VALUE(etl_data:licenceplate) is NULL
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
                            IS_NULL_VALUE(etl_data:_id)
                            or IS_NULL_VALUE(etl_data:created)
                            or IS_NULL_VALUE(etl_data:mfc)
                            or IS_NULL_VALUE(etl_data:licenceplate)
                            or IS_NULL_VALUE(etl_data:_id) is NULL
                            or IS_NULL_VALUE(etl_data:created) is NULL
                            or IS_NULL_VALUE(etl_data:mfc) is NULL
                            or IS_NULL_VALUE(etl_data:licenceplate) is NULL
                        )
                  )
                    HEADER = FALSE
                    OVERWRITE=TRUE"""

schema_version = "v1"

validation_sql = """
                SELECT COUNT(*) FROM (
                SELECT dl_service.delete_key(dl_service.keys_to_snake(dl_service.remove_nulls(dl_service.format_ts(raw_data, ['last_modified_ts','created']))), ['index'])
                FROM datalake_{client}.raw_{table}
                EXCEPT DISTINCT
                SELECT dl_service.sort_json(dl_service.remove_nulls(to_json_string(t)))
                FROM (
                SELECT * EXCEPT(__client_name, __source_name, __schema_version, __event_timestamp, __publish_timestamp, __ingest_timestamp, _rev,wpno)
                FROM datalake_{client}.{table}
                WHERE __event_timestamp >= timestamp('{min_ts}') and __event_timestamp < timestamp('{max_ts}') 
                ) t
                ) a"""
