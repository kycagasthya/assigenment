
mapping_prod = [

    {
        "client": "ahold",
        "database": "ALPHA",
        "min_ts": "2019-09-01T00:00:01.100000+00:00",
        "max_ts": "2020-03-11T00:00:01.100000+00:00"
    },
    {
        "client": "sedanos",
        "database": "SUNBIRD",
        "min_ts": "2019-09-01T00:00:01.100000+00:00",
        "max_ts": "2020-04-27T00:00:01.100000+00:00"
    },
    {
        "client": "tangerine-albertsons",
        "database": "TANGERINE",
        "min_ts": "2019-12-01T00:00:01.100000+00:00",
        "max_ts": "2020-04-27T00:00:01.100000+00:00"
    },
    {
        "client": "wakefern",
        "database": "WINTER",
        "min_ts": "2019-11-01T00:00:01.100000+00:00",
        "max_ts": "2020-03-12T00:00:01.100000+00:00"
    }
]

historical_sql = """copy into @json_unload_file_stage/{table}/{subdir}/{table}_json
             from (
                    select OBJECT_DELETE(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(KEYS_TO_SNAKE(ETL_DATA),
                                      '__client_name', '{client}', true),
                                      '__source_name', '{table}', true),
                                      '__schema_version', 'snowflake_historical', true),
                                      '__event_timestamp', TO_VARCHAR(created), true),
                                      '__publish_timestamp', null, true),
                                      '__ingestion_timestamp', null, true), 'index')
                    from {table}
                    where created >= to_timestamp('{min_ts}') and created < to_timestamp('{max_ts}')
                    and not (
                            IS_NULL_VALUE(etl_data:address)
                            or IS_NULL_VALUE(etl_data:last_update_date)
                            or IS_NULL_VALUE(etl_data:location_id)
                            or IS_NULL_VALUE(etl_data:product_id)
                            or IS_NULL_VALUE(etl_data:qty_allocated)
                            or IS_NULL_VALUE(etl_data:qty_available)
                            or IS_NULL_VALUE(etl_data:qty_reserved)
                            or IS_NULL_VALUE(etl_data:qty_total)
                            or IS_NULL_VALUE(etl_data:address) is null
                            or IS_NULL_VALUE(etl_data:last_update_date) is null
                            or IS_NULL_VALUE(etl_data:location_id) is null
                            or IS_NULL_VALUE(etl_data:product_id) is null
                            or IS_NULL_VALUE(etl_data:qty_allocated) is null
                            or IS_NULL_VALUE(etl_data:qty_available) is null
                            or IS_NULL_VALUE(etl_data:qty_reserved) is null
                            or IS_NULL_VALUE(etl_data:qty_total) is null
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
                            IS_NULL_VALUE(etl_data:address)
                            or IS_NULL_VALUE(etl_data:last_update_date)
                            or IS_NULL_VALUE(etl_data:location_id)
                            or IS_NULL_VALUE(etl_data:product_id)
                            or IS_NULL_VALUE(etl_data:qty_allocated)
                            or IS_NULL_VALUE(etl_data:qty_available)
                            or IS_NULL_VALUE(etl_data:qty_reserved)
                            or IS_NULL_VALUE(etl_data:qty_total)
                            or IS_NULL_VALUE(etl_data:address) is null
                            or IS_NULL_VALUE(etl_data:last_update_date) is null
                            or IS_NULL_VALUE(etl_data:location_id) is null
                            or IS_NULL_VALUE(etl_data:product_id) is null
                            or IS_NULL_VALUE(etl_data:qty_allocated) is null
                            or IS_NULL_VALUE(etl_data:qty_available) is null
                            or IS_NULL_VALUE(etl_data:qty_reserved) is null
                            or IS_NULL_VALUE(etl_data:qty_total) is null
                        )
                    )
                    HEADER = FALSE
                    OVERWRITE=TRUE"""

schema_version = "v1"

validation_sql = """
                SELECT COUNT(*) FROM (
                SELECT dl_service.delete_key(dl_service.remove_nulls(dl_service.format_ts(raw_data, ['last_update_date'])), ['index'])
                FROM datalake_{client}.raw_{table}
                EXCEPT DISTINCT
                SELECT dl_service.sort_json(dl_service.remove_nulls(to_json_string(t)))
                FROM (
                SELECT * EXCEPT(__client_name, __source_name, __schema_version, __event_timestamp, __publish_timestamp, __ingest_timestamp)
                FROM datalake_{client}.{table}
                WHERE __event_timestamp >= timestamp('{min_ts}') and __event_timestamp < timestamp('{max_ts}') 
                ) t
                ) a"""
