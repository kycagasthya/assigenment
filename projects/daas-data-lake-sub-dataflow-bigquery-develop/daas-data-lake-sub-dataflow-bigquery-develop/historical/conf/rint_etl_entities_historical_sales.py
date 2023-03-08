mapping_dev = [
    {
        "client": "woolworths",
        "database": "WINGS_DEV",
        "min_ts": "2021-10-20T07:52:19.819000+00:00",
        "max_ts": "2021-10-21T04:25:49.247000+00:00"
    }
]

mapping_prod = [
    {
        "client": "woolworths",
        "database": "WINGS",
        "min_ts": "2021-10-20T07:52:19.819000+00:00",
        "max_ts": "2022-11-11T05:52:55.120000+00:00"
    }
]

historical_sql = """copy into @json_unload_file_stage/{table}/{subdir}/{table}_json
             from (
                    select OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(
                        KEYS_TO_SNAKE_TO_LOWER(REMOVE_NULLS(DOC)), 'attributes', TO_VARCHAR(doc:attributes), true), 
                                  '__client_name', '{client}', true), 
                                  '__source_name', '{table}', true), 
                                  '__schema_version', 'snowflake_historical', true), 
                                  '__event_timestamp', TO_VARCHAR(created), true),
                                  '__publish_timestamp', current_timestamp(), true),
                                  '__ingest_timestamp', current_timestamp(), true)
                    from RINT_ETL_ENTITIES
                    where created >= to_timestamp('{min_ts}') and created <= to_timestamp('{max_ts}') 
                    and DOC:attributes:ENTITY_NAME = 'historical_sales'
             )
                HEADER = FALSE
                OVERWRITE=TRUE"""

raw_sql = """copy into @csv_unload_file_stage/{table}/{subdir}/{table}_csv
                  from (
                        select DOC
                        from RINT_ETL_ENTITIES
                        where created >= to_timestamp('{min_ts}') and created <= to_timestamp('{max_ts}')
                        and DOC:attributes:ENTITY_NAME = 'historical_sales'
                  )
                    HEADER = FALSE
                    OVERWRITE=TRUE"""

schema_version = "v1"

validation_sql = """
                SELECT COUNT(*) FROM (
                SELECT dl_service.keys_to_snake_to_lower(dl_service.remove_nulls(dl_service.format_ts(raw_data, ['created_ts','delivered_ts','pubsub_publish_time'])))
                FROM datalake_{client}.raw_{table}
                EXCEPT DISTINCT
                SELECT dl_service.sort_json(dl_service.remove_nulls(to_json_string(t)))
                FROM (
                SELECT * EXCEPT(__client_name, __source_name, __schema_version, __event_timestamp, __publish_timestamp, __ingest_timestamp)
                FROM datalake_{client}.{table}
                WHERE __event_timestamp >= timestamp('{min_ts}') and __event_timestamp < timestamp('{max_ts}') 
                ) t
                ) a"""
