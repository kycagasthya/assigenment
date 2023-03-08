
mapping_prod = [
    {
        "client": "albertsons",
        "database": "ABS",
        "min_ts": "2021-11-11T13:12:30.005000+00:00",
        "max_ts": "2022-02-17T05:41:13.349000+00:00"
    },
    {
        "client": "ahold",
        "database": "ALPHA",
        "min_ts": "2020-06-05T17:06:30.436000+00:00",
        "max_ts": "2022-02-17T05:19:09.313000+00:00"
    },
    {
        "client": "big-y",
        "database": "BLUEBERRY",
        "min_ts": "2021-03-29T19:08:12.959000+00:00",
        "max_ts": "2022-02-16T21:51:14.832000+00:00"
    },
    {
        "client": "kroger",
        "database": "EIGHTYONE",
        "min_ts": "2020-10-21T14:01:47.450000+00:00",
        "max_ts": "2022-02-17T02:21:14.987000+00:00"
    },
    {
        "client": "loblaws",
        "database": "LOBSTER",
        "min_ts": "2020-04-24T14:32:20.532000+00:00",
        "max_ts": "2022-02-16T10:48:12.709000+00:00"
    },
    {
        "client": "maf",
        "database": "MAF",
        "min_ts": "2021-01-26T22:31:50.764000+00:00",
        "max_ts": "2022-02-16T17:51:10.501000+00:00"
    },
    {
        "client": "sedanos",
        "database": "SUNBIRD",
        "min_ts": "2020-10-08T16:00:37.640000+00:00",
        "max_ts": "2022-02-16T16:15:16.182000+00:00"
    },
    {
        "client": "tangerine-albertsons",
        "database": "TANGERINE",
        "min_ts": "2020-08-06T18:34:53.199000+00:00",
        "max_ts": "2022-02-17T04:30:10.672000+00:00"
    },
    {
        "client": "woolworths",
        "database": "WINGS",
        "min_ts": "2020-09-24T18:30:10.861000+00:00",
        "max_ts": "2022-02-17T08:01:10.463000+00:00"
    },
    {
        "client": "wakefern",
        "database": "WINTER",
        "min_ts": "2020-06-07T16:05:40.461000+00:00",
        "max_ts": "2022-02-15T21:13:09.798000+00:00"
    }
]

historical_sql = """copy into @json_unload_file_stage/{table}/{subdir}/{table}_json
             from (
                    select OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(KEYS_TO_SNAKE(REMOVE_NULLS(doc)), 'extra', TO_VARCHAR(doc:extra), true),
                                      '__client_name', '{client}', true), 
                                      '__source_name', '{table}', true), 
                                      '__schema_version', 'snowflake_historical', true), 
                                      '__event_timestamp', TO_VARCHAR(created), true),
                                      '__publish_timestamp', null, true),
                                      '__ingestion_timestamp', null, true) 
                    from {table}
                    where created >= to_timestamp('{min_ts}') and created < to_timestamp('{max_ts}')
                    and not (
                            IS_NULL_VALUE(doc:"last-modified-ts")
                            or IS_NULL_VALUE(doc:"tom-id")
                            or IS_NULL_VALUE(doc:"last-modified-ts") is null
                            or IS_NULL_VALUE(doc:"tom-id") is null
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
                            IS_NULL_VALUE(doc:"last-modified-ts")
                            or IS_NULL_VALUE(doc:"tom-id")
                            or IS_NULL_VALUE(doc:"last-modified-ts") is null
                            or IS_NULL_VALUE(doc:"tom-id') is null
                    )
                    )
                    HEADER = FALSE
                    OVERWRITE=TRUE"""

schema_version = "v2"

validation_sql = """
                SELECT COUNT(*) FROM (
                SELECT dl_service.delete_key(dl_service.remove_nulls(dl_service.format_ts(dl_service.keys_to_snake(raw_data), ['created_ts', 'last_modified_ts'])),['extra'])
                FROM datalake_{client}.raw_{table}
                EXCEPT DISTINCT
                SELECT dl_service.sort_json(dl_service.remove_nulls(to_json_string(t)))
                FROM (
                SELECT * EXCEPT(__client_name, __source_name, __schema_version, __event_timestamp, __publish_timestamp, __ingest_timestamp, extra)
                FROM datalake_{client}.{table}
                WHERE __event_timestamp >= timestamp('{min_ts}') and __event_timestamp < timestamp('{max_ts}') 
                ) t
                ) a"""
