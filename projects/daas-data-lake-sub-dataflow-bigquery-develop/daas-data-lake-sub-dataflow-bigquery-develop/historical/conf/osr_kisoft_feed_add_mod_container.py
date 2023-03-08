mapping_dev = [{'client': 'ahold', 'database': 'ALPHA_DEV', 'min_ts': '2020-08-26T07:25:58.776000+00:00',
                'max_ts': '2021-05-24T13:22:09.575000+00:00'},
               {'client': 'kroger', 'database': 'EIGHTYONE_DEV', 'min_ts': '2020-11-12T12:40:48.002000+00:00',
                'max_ts': '2020-11-30T17:34:35.287000+00:00'},
               {'client': 'loblaws', 'database': 'LOBSTER_DEV', 'min_ts': '2020-08-12T20:53:26.935000+00:00',
                'max_ts': '2021-03-05T13:55:13.415000+00:00'},
               {'client': 'maf', 'database': 'MAF_DEV', 'min_ts': '2021-02-01T13:35:02.572000+00:00',
                'max_ts': '2021-03-05T13:55:27.401000+00:00'},
               {'client': 'sedanos', 'database': 'SUNBIRD_DEV', 'min_ts': '2020-08-14T11:13:49.197000+00:00',
                'max_ts': '2021-02-21T13:02:09.514000+00:00'},
               {'client': 'woolworths', 'database': 'WINGS_DEV', 'min_ts': '2020-10-01T07:50:26.679000+00:00',
                'max_ts': '2021-03-05T13:56:16.066000+00:00'},
               {'client': 'wakefern', 'database': 'WINTER_DEV', 'min_ts': '2020-05-28T10:54:30.048000+00:00',
                'max_ts': '2021-05-24T13:24:17.832000+00:00'},
               {'client': 'tangerine-albertsons', 'database': 'TANGERINE_DEV',
                'min_ts': '2020-05-29T17:27:40.421000+00:00', 'max_ts': '2021-03-22T20:14:55.731000+00:00'}]

mapping_prod = [{'client': 'ahold', 'database': 'ALPHA', 'min_ts': '2020-08-26T07:25:58.776000+00:00',
                 'max_ts': '2021-05-24T13:22:09.575000+00:00'},
                {'client': 'kroger', 'database': 'EIGHTYONE', 'min_ts': '2020-11-12T12:40:48.002000+00:00',
                 'max_ts': '2020-11-30T17:34:35.287000+00:00'},
                {'client': 'loblaws', 'database': 'LOBSTER', 'min_ts': '2020-08-12T20:53:26.935000+00:00',
                 'max_ts': '2021-03-05T13:55:13.415000+00:00'},
                {'client': 'maf', 'database': 'MAF', 'min_ts': '2021-02-01T13:35:02.572000+00:00',
                 'max_ts': '2021-03-05T13:55:27.401000+00:00'},
                {'client': 'sedanos', 'database': 'SUNBIRD', 'min_ts': '2020-08-14T11:13:49.197000+00:00',
                 'max_ts': '2021-02-21T13:02:09.514000+00:00'},
                {'client': 'woolworths', 'database': 'WINGS', 'min_ts': '2020-10-01T07:50:26.679000+00:00',
                 'max_ts': '2021-03-05T13:56:16.066000+00:00'},
                {'client': 'wakefern', 'database': 'WINTER', 'min_ts': '2020-05-28T10:54:30.048000+00:00',
                 'max_ts': '2021-05-24T13:24:17.832000+00:00'},
                {'client': 'tangerine-albertsons', 'database': 'TANGERINE',
                 'min_ts': '2020-05-29T17:27:40.421000+00:00', 'max_ts': '2021-03-22T20:14:55.731000+00:00'}]

historical_sql = """copy into @json_unload_file_stage/{table}/{subdir}/{table}_json
                from (
select 
OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(KEYS_TO_SNAKE(REMOVE_NULLS(OBJECT_DELETE(DOC, 'pubsub_publish_time'))),
              'csv', TO_VARCHAR(DOC:csv), true),
              'action', TO_VARCHAR(DOC:csv[0][2]), true),  
              'sub_action', TO_VARCHAR(DOC:csv[0][3]), true),
              'systemid', TO_VARCHAR(DOC:csv[0][4]), true),
              'record_id', TO_VARCHAR(DOC:csv[1][0]), true),
              'event_id', TO_VARCHAR(DOC:csv[1][1]), true),
              'wpono', TO_VARCHAR(DOC:csv[1][2]), true), 
              'cntno', TO_VARCHAR(DOC:csv[1][3]), true), 
              'licenceplate', TO_VARCHAR(DOC:csv[1][9]), true),
              'marriagetime', TO_VARCHAR(DOC:csv[1][7]), true),
              'status', TO_VARCHAR(DOC:csv[1][5]), true),
                'error_id', TO_VARCHAR(DOC:csv[1][6]), true),
              '__client_name', '{client}', true), 
              '__source_name', '{table}', true), 
              '__schema_version', 'snowflake_historical', true), 
              '__event_timestamp', TO_VARCHAR(created), true),
              '__publish_timestamp', current_timestamp(), true),
              '__ingest_timestamp', current_timestamp(), true)
                    from OSR_KISOFT_FEED 
                  where created >= to_timestamp('{min_ts}') and created < to_timestamp('{max_ts}')
                  and DOC:csv[1][0] = 'CO' and DOC:csv[0][2] IN ('ADD', 'MOD') and DOC:csv[0][3] = 'CONTAINER'
                )
                HEADER = FALSE
                OVERWRITE=TRUE"""

raw_sql = """copy into @csv_unload_file_stage/{table}/{subdir}/{table}_csv
                 from (
                        select doc
                        from osr_kisoft_feed 
                        where DOC:csv[1][0] = 'CO' and DOC:csv[0][2] IN ('ADD', 'MOD') and DOC:csv[0][3] = 'CONTAINER'
                            and created >= to_timestamp('{min_ts}') and created < to_timestamp('{max_ts}')
                    )
                    HEADER = FALSE
                    OVERWRITE=TRUE"""

schema_version = "v2"

validation_sql = """
                WITH raw as (SELECT
  JSON_EXTRACT(raw_data, '$.csv') as csv,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(0)])[OFFSET(2)] as action,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(0)])[OFFSET(3)] as sub_action,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(0)])[OFFSET(4)] as systemid,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(0)] as record_id,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(1)] as event_id,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(2)] as wpono,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(3)] as cntno,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(9)] as licenceplate,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(7)] as marriagetime,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(5)] as status,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(6)] as error_id,
  STRUCT(JSON_EXTRACT_SCALAR(raw_data, '$.file.data') as data, JSON_EXTRACT_SCALAR(raw_data, '$.file.location-id') as location_id, JSON_EXTRACT_SCALAR(raw_data, '$.file.name') as name) as file,
  JSON_EXTRACT_SCALAR(raw_data, '$.type') as type,
  JSON_EXTRACT_SCALAR(raw_data, '$.cmd') as cmd,
FROM
  `prj-daas-n-dev-dl-sub-bq-9220.datalake_kroger.raw_osr_kisoft_feed_add_mod_container`)

SELECT COUNT(*) FROM (SELECT dl_service.sort_json(dl_service.remove_nulls(to_json_string(raw)))
FROM raw
EXCEPT DISTINCT
SELECT dl_service.sort_json(dl_service.remove_nulls(to_json_string(t)))
                FROM (SELECT * EXCEPT(__client_name, __source_name, __schema_version, __event_timestamp, __publish_timestamp, __ingest_timestamp)
                FROM `prj-daas-n-dev-dl-sub-bq-9220.datalake_kroger.osr_kisoft_feed_add_mod_container`) t)"""
