
mapping_prod = [
    {
        "client": "ahold",
        "database": "ALPHA",
        "min_ts": "2020-04-23T14:56:32.562000+00:00",
        "max_ts": "2020-04-23T14:59:09.019000+00:00"
    },
    {
        "client": "tangerine-albertsons",
        "database": "TANGERINE",
        "min_ts": "2020-04-27T12:54:14.951000+00:00",
        "max_ts": "2020-07-22T07:10:00.468000+00:00"
    },
    {
        "client": "wakefern",
        "database": "WINTER",
        "min_ts": "2020-05-01T19:01:12.174000+00:00",
        "max_ts": "2020-05-27T07:00:34.790000+00:00"
    }
]

historical_sql = """copy into @json_unload_file_stage/{table}/{subdir}/{table}_json
             from (
                    select OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(KEYS_TO_SNAKE(REMOVE_NULLS(doc)), 'extra', TO_VARCHAR(doc:extra), true), 'source', TO_VARCHAR(doc:source), true),                  
                                      '__client_name', '{client}', true), 
                                      '__source_name', '{table}', true), 
                                      '__schema_version', 'snowflake_historical', true), 
                                      '__event_timestamp', TO_VARCHAR(created), true),
                                      '__publish_timestamp', null, true),
                                      '__ingestion_timestamp', null, true) 
                    from {table}
                    where created >= to_timestamp('{min_ts}') and created < to_timestamp('{max_ts}')
                    and not (
                            IS_NULL_VALUE(doc:id)
                            or IS_NULL_VALUE(doc:id) is null
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
                            IS_NULL_VALUE(doc:id)
                            or IS_NULL_VALUE(doc:id) is null
                    )
                    )
                    HEADER = FALSE
                    OVERWRITE=TRUE"""

schema_version = "v3"

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
