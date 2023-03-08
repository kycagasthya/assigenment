mapping_dev = [
    {
        "client": "ahold",
        "database": "ALPHA_DEV",
        "min_ts": "2022-04-15T00:01:20.333275+00:00",
        "max_ts": "2022-06-15T00:01:28.823389+00:00"
    },
    {
        "client": "big-y",
        "database": "BLUEBERRY_DEV",
        "min_ts": "2022-04-15T00:01:21.923099+00:00",
        "max_ts": "2022-06-15T00:01:15.867804+00:00"
    },
    {
        "client": "kroger",
        "database": "EIGHTYONE_DEV",
        "min_ts": "2022-04-15T00:01:19.979890+00:00",
        "max_ts": "2022-06-15T00:01:08.126489+00:00"
    },
    {
        "client": "loblaws",
        "database": "LOBSTER_DEV",
        "min_ts": "2022-04-15T11:37:12.261256+00:00",
        "max_ts": "2022-06-15T00:01:10.027141+00:00"
    },
    {
        "client": "maf",
        "database": "MAF_DEV",
        "min_ts": "2022-04-15T00:01:22.656820+00:00",
        "max_ts": "2022-06-15T00:01:45.990427+00:00"
    },
    {
        "client": "sedanos",
        "database": "SUNBIRD_DEV",
        "min_ts": "2022-04-15T00:01:30.506440+00:00",
        "max_ts": "2022-06-15T00:01:07.642810+00:00"
    },
    {
        "client": "tangerine-albertsons",
        "database": "TANGERINE_DEV",
        "min_ts": "2022-04-15T11:47:11.391290+00:00",
        "max_ts": "2022-04-19T00:02:02.408251+00:00"
    },
    {
        "client": "woolworths",
        "database": "WINGS_DEV",
        "min_ts": "2022-04-15T00:01:36.415572+00:00",
        "max_ts": "2022-06-15T00:01:12.240053+00:00"
    },
    {
        "client": "wakefern",
        "database": "WINTER_DEV",
        "min_ts": "2022-04-15T00:01:11.308620+00:00",
        "max_ts": "2022-06-15T00:01:17.251236+00:00"
    }
]

mapping_prod = [
    {
        "client": "albertsons",
        "database": "ABS",
        "min_ts": "2021-11-18T14:37:58.404000+00:00",
        "max_ts": "2022-07-11T06:00:07.732000+00:00"
    },
    {
        "client": "ahold",
        "database": "ALPHA",
        "min_ts": "2021-10-06T11:00:11.045000+00:00",
        "max_ts": "2022-07-11T05:00:09.538000+00:00"
    },
    {
        "client": "big-y",
        "database": "BLUEBERRY",
        "min_ts": "2021-10-01T10:00:12.093000+00:00",
        "max_ts": "2022-07-09T06:00:05.496000+00:00"
    },
    {
        "client": "kroger",
        "database": "EIGHTYONE",
        "min_ts": "2021-10-01T10:00:14.656000+00:00",
        "max_ts": "2022-07-11T02:00:05.197000+00:00"
    },
    {
        "client": "loblaws",
        "database": "LOBSTER",
        "min_ts": "2021-10-01T10:00:08.291000+00:00",
        "max_ts": "2022-07-10T11:00:11.685000+00:00"
    },
    {
        "client": "maf",
        "database": "MAF",
        "min_ts": "2021-10-01T11:00:09.733000+00:00",
        "max_ts": "2022-07-10T19:00:07.229000+00:00"
    },
    {
        "client": "sedanos",
        "database": "SUNBIRD",
        "min_ts": "2021-10-01T11:00:15.383000+00:00",
        "max_ts": "2022-07-09T16:00:04.820000+00:00"
    },
    {
        "client": "tangerine-albertsons",
        "database": "TANGERINE",
        "min_ts": "2021-10-01T11:00:20.737000+00:00",
        "max_ts": "2022-04-15T06:08:16.432000+00:00"
    },
    {
        "client": "woolworths",
        "database": "WINGS",
        "min_ts": "2021-10-01T11:00:10.659000+00:00",
        "max_ts": "2022-07-11T06:00:07.361000+00:00"
    },
    {
        "client": "wakefern",
        "database": "WINTER",
        "min_ts": "2021-10-01T11:00:18.251000+00:00",
        "max_ts": "2022-07-10T21:00:06.387000+00:00"
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
                            IS_NULL_VALUE(doc:"mfc-stop-buy")
                            or IS_NULL_VALUE(doc:"last-modified-ts")
                            or IS_NULL_VALUE(doc:"revision")
                            or IS_NULL_VALUE(doc:"name")
                            or IS_NULL_VALUE(doc:"tom-id")
                            or IS_NULL_VALUE(doc:"item-type")
                            or IS_NULL_VALUE(doc:"mfc-stop-fulfill")
                            or IS_NULL_VALUE(doc:"created-ts")
                            or IS_NULL_VALUE(doc:"department")
                            or IS_NULL_VALUE(doc:"case-item")
                            or IS_NULL_VALUE(doc:"retail-item")
                            or IS_NULL_VALUE(doc:"mfc-stop-buy") is null
                            or IS_NULL_VALUE(doc:"last-modified-ts") is null
                            or IS_NULL_VALUE(doc:"revision") is null
                            or IS_NULL_VALUE(doc:"name") is null
                            or IS_NULL_VALUE(doc:"tom-id") is null
                            or IS_NULL_VALUE(doc:"item-type") is null
                            or IS_NULL_VALUE(doc:"mfc-stop-fulfill") is null
                            or IS_NULL_VALUE(doc:"created-ts") is null
                            or IS_NULL_VALUE(doc:"department") is null
                            or IS_NULL_VALUE(doc:"case-item") is null
                            or IS_NULL_VALUE(doc:"retail-item") is null
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
                            IS_NULL_VALUE(doc:"mfc-stop-buy")
                            or IS_NULL_VALUE(doc:"last-modified-ts")
                            or IS_NULL_VALUE(doc:"revision")
                            or IS_NULL_VALUE(doc:"name")
                            or IS_NULL_VALUE(doc:"tom-id")
                            or IS_NULL_VALUE(doc:"item-type")
                            or IS_NULL_VALUE(doc:"mfc-stop-fulfill")
                            or IS_NULL_VALUE(doc:"created-ts")
                            or IS_NULL_VALUE(doc:"department")
                            or IS_NULL_VALUE(doc:"case-item")
                            or IS_NULL_VALUE(doc:"retail-item")
                            or IS_NULL_VALUE(doc:"mfc-stop-buy") is null
                            or IS_NULL_VALUE(doc:"last-modified-ts") is null
                            or IS_NULL_VALUE(doc:"revision") is null
                            or IS_NULL_VALUE(doc:"name") is null
                            or IS_NULL_VALUE(doc:"tom-id") is null
                            or IS_NULL_VALUE(doc:"item-type") is null
                            or IS_NULL_VALUE(doc:"mfc-stop-fulfill") is null
                            or IS_NULL_VALUE(doc:"created-ts") is null
                            or IS_NULL_VALUE(doc:"department") is null
                            or IS_NULL_VALUE(doc:"case-item") is null
                            or IS_NULL_VALUE(doc:"retail-item") is null
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
