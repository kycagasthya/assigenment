mapping_dev = [
    {
        "client": "tangerine-albertsons",
        "database": "TANGERINE_DEV",
        "min_ts": "2020-10-05T14:22:36.944820+00:00",
        "max_ts": "2022-03-30T00:03:16.637871+00:00"
    }
]

mapping_prod = [
    {
        "client": "tangerine-albertsons",
        "database": "TANGERINE",
        "min_ts": "2020-10-05T14:22:36.944820+00:00",
        "max_ts": "2022-03-30T00:03:16.637871+00:00"
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
                    from {table} || 's'
                    where created >= to_timestamp('{min_ts}') and created <= to_timestamp('{max_ts}')
                )
                HEADER = FALSE
                OVERWRITE=TRUE"""

raw_sql = """copy into @csv_unload_file_stage/{table}/{subdir}/{table}_csv
                  from (
                        select OBJECT_DELETE(ETL_DATA, 'index')
                        from {table} 
                        where created >= to_timestamp('{min_ts}') and created <= to_timestamp('{max_ts}')
                    )
                    HEADER = FALSE
                    OVERWRITE=TRUE"""

schema_version = "v1"

validation_sql = """
                SELECT COUNT(*) FROM (
                SELECT dl_service.delete_key(dl_service.remove_nulls(dl_service.format_ts(raw_data)), ['index'])
                FROM datalake_{client}.raw_{table}
                EXCEPT DISTINCT
                SELECT dl_service.sort_json(dl_service.remove_nulls(to_json_string(t)))
                FROM (
                SELECT * EXCEPT(__client_name, __source_name, __schema_version, __event_timestamp, __publish_timestamp, __ingest_timestamp)
                FROM datalake_{client}.{table}
                WHERE __event_timestamp >= timestamp('{min_ts}') and __event_timestamp < timestamp('{max_ts}') 
                ) t
                ) a"""
