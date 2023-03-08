mapping_dev = [
    {'client': 'ahold', 'database': 'ALPHA_DEV', 'min_ts': '2021-12-01T14:05:11.362547+00:00',
     'max_ts': '2022-08-10T11:50:05.589022+00:00'},
    {'client': 'big-y', 'database': 'BLUEBERRY_DEV', 'min_ts': '2022-04-15T15:20:12.123422+00:00',
     'max_ts': '2022-08-10T15:50:04.762194+00:00'},
    {'client': 'loblaws', 'database': 'LOBSTER_DEV', 'min_ts': '2021-12-01T14:05:10.012149+00:00',
     'max_ts': '2022-08-11T09:05:04.984008+00:00'},
    {'client': 'wakefern', 'database': 'WINTER_DEV', 'min_ts': '2021-12-01T14:05:12.225641+00:00',
     'max_ts': '2022-08-10T10:35:04.678562+00:00'},
    {'client': 'tangerine-albertsons', 'database': 'TANGERINE_DEV',
     'min_ts': '2021-12-01T14:05:12.082299+00:00', 'max_ts': '2022-03-30T04:35:15.983099+00:00'}
]

mapping_prod = [
    {'client': 'ahold', 'database': 'ALPHA', 'min_ts': '2021-12-01T14:05:11.362547+00:00',
     'max_ts': '2022-08-31T09:35:04.766050+00:00'},
    {'client': 'big-y', 'database': 'BLUEBERRY', 'min_ts': '2022-04-15T15:20:12.123422+00:00',
     'max_ts': '2022-08-31T09:35:04.666371+00:00'},
    {'client': 'loblaws', 'database': 'LOBSTER', 'min_ts': '2021-12-01T14:05:10.012149+00:00',
     'max_ts': '2022-08-31T09:35:04.678301+00:00'},
    {'client': 'wakefern', 'database': 'WINTER', 'min_ts': '2021-12-01T14:05:12.225641+00:00',
     'max_ts': '2022-08-31T09:35:04.628078+00:00'},
    {'client': 'tangerine-albertsons', 'database': 'TANGERINE',
     'min_ts': '2021-12-01T14:05:12.082299+00:00', 'max_ts': '2022-03-30T04:35:15.983099+00:00'}
]

historical_sql = """copy into @json_unload_file_stage/{table}/{subdir}/{table}_json
             from (
                    select OBJECT_DELETE(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(KEYS_TO_SNAKE(REMOVE_NULLS(OBJECT_DELETE(OBJECT_DELETE(ETL_DATA, 'aisle_free_positions'), 'aisle_number'))), 
                                  '__client_name', '{client}', true), 
                                  '__event_timestamp', TO_VARCHAR(created), true), 
                                  '__schema_version', 'snowflake_historical', true), 
                                  '__source_name', '{table}', true),
                                  '__publish_timestamp', current_timestamp(), true),
                                  '__ingest_timestamp', current_timestamp(), true), 'index')
                    from {table}
                    where created >= to_timestamp('{min_ts}') and created <= to_timestamp('{max_ts}')
                )
                HEADER = FALSE
                OVERWRITE=TRUE"""

raw_sql = """copy into @csv_unload_file_stage/{table}/{subdir}/{table}_csv
                  from (
                        select OBJECT_DELETE(OBJECT_DELETE(ETL_DATA, 'aisle_free_positions'), 'aisle_number')
                        from {table}
                        where created >= to_timestamp('{min_ts}') and created <= to_timestamp('{max_ts}')
                    )
                    HEADER = FALSE
                    OVERWRITE=TRUE"""

schema_version = "v1"

validation_sql = """
                SELECT COUNT(*) FROM (
                SELECT dl_service.delete_key(dl_service.remove_nulls(dl_service.format_ts(raw_data, ['created'])), ['index'])
                FROM `{project}.datalake_{client}.raw_{table}`
                EXCEPT DISTINCT
                SELECT dl_service.sort_json(dl_service.remove_nulls(to_json_string(t)))
                FROM (
                SELECT * EXCEPT(__client_name, __source_name, __schema_version, __event_timestamp, __publish_timestamp, __ingest_timestamp)
                FROM `{project}.datalake_{client}.{table}`
                WHERE __event_timestamp >= timestamp('{min_ts}') and __event_timestamp <= timestamp('{max_ts}') 
                ) t
                ) a"""
