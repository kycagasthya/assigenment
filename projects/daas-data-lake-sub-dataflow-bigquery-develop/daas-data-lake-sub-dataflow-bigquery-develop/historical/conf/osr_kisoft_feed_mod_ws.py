mapping_dev = [{'client': 'ahold', 'database': 'ALPHA_DEV', 'min_ts': '2020-08-26T07:25:58.759000+00:00',
                'max_ts': '2021-05-24T12:33:34.459000+00:00'},
               {'client': 'loblaws', 'database': 'LOBSTER_DEV', 'min_ts': '2020-08-12T23:02:21.888000+00:00',
                'max_ts': '2021-03-05T13:55:13.419000+00:00'},
               {'client': 'maf', 'database': 'MAF_DEV', 'min_ts': '2021-02-01T13:35:14.787000+00:00',
                'max_ts': '2021-03-05T13:51:48.209000+00:00'},
               {'client': 'sedanos', 'database': 'SUNBIRD_DEV', 'min_ts': '2020-08-14T11:13:53.222000+00:00',
                'max_ts': '2021-02-21T12:46:28.233000+00:00'},
               {'client': 'woolworths', 'database': 'WINGS_DEV', 'min_ts': '2020-10-01T07:50:26.784000+00:00',
                'max_ts': '2021-03-05T13:56:34.666000+00:00'},
               {'client': 'wakefern', 'database': 'WINTER_DEV', 'min_ts': '2020-05-28T10:54:29.972000+00:00',
                'max_ts': '2021-05-24T13:24:18.756000+00:00'},
               {'client': 'tangerine-albertsons', 'database': 'TANGERINE_DEV',
                'min_ts': '2020-05-29T17:27:41.120000+00:00', 'max_ts': '2021-03-22T20:14:55.726000+00:00'}]

mapping_prod = [{'client': 'ahold', 'database': 'ALPHA', 'min_ts': '2020-08-26T07:25:58.759000+00:00',
                 'max_ts': '2021-05-24T12:33:34.459000+00:00'},
                {'client': 'loblaws', 'database': 'LOBSTER', 'min_ts': '2020-08-12T23:02:21.888000+00:00',
                 'max_ts': '2021-03-05T13:55:13.419000+00:00'},
                {'client': 'maf', 'database': 'MAF', 'min_ts': '2021-02-01T13:35:14.787000+00:00',
                 'max_ts': '2021-03-05T13:51:48.209000+00:00'},
                {'client': 'sedanos', 'database': 'SUNBIRD', 'min_ts': '2020-08-14T11:13:53.222000+00:00',
                 'max_ts': '2021-02-21T12:46:28.233000+00:00'},
                {'client': 'woolworths', 'database': 'WINGS', 'min_ts': '2020-10-01T07:50:26.784000+00:00',
                 'max_ts': '2021-03-05T13:56:34.666000+00:00'},
                {'client': 'wakefern', 'database': 'WINTER', 'min_ts': '2020-05-28T10:54:29.972000+00:00',
                 'max_ts': '2021-05-24T13:24:18.756000+00:00'},
                {'client': 'tangerine-albertsons', 'database': 'TANGERINE',
                 'min_ts': '2020-05-29T17:27:41.120000+00:00', 'max_ts': '2021-03-22T20:14:55.726000+00:00'}]

historical_sql = """copy into @json_unload_file_stage/{table}/{subdir}/{table}_json
             from (
                    select OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(KEYS_TO_SNAKE(REMOVE_NULLS(OBJECT_DELETE(DOC, 'pubsub_publish_time'))) , 'csv', TO_VARCHAR(DOC:csv), true),
                                  'recordid', TO_VARCHAR(DOC:csv[0][0]), true),
                                  'id', TO_NUMBER(DOC:csv[0][1]), true),
                                  'action', TO_VARCHAR(DOC:csv[0][2]), true),  
                                  'sub_action', TO_VARCHAR(DOC:csv[0][3]), true),
                                  'systemid', TO_VARCHAR(DOC:csv[0][4]), true),
                                  'record_id', TO_VARCHAR(DOC:csv[1][0]), true),
                                  'event_id', TO_VARCHAR(DOC:csv[1][1]), true),
                                  'wpono', TO_VARCHAR(DOC:csv[1][2]), true), 
                                  'cntno', TO_VARCHAR(DOC:csv[1][3]), true), 
                                  'master_fp_name', TO_VARCHAR(DOC:csv[1][4]), true),
                                  'ws_no', TO_NUMBER(DOC:csv[1][5]), true),
                                  'status', TO_VARCHAR(DOC:csv[1][6]), true),
                                  'error_id', TO_VARCHAR(DOC:csv[1][7]), true),
                                  'ws_type', TO_VARCHAR(DOC:csv[1][8]), true),
                                  'actqty', TO_NUMBER(DOC:csv[1][9]), true),
                                  'remark', TO_VARCHAR(DOC:csv[1][10]), true),
                                  'itemno', TO_VARCHAR(DOC:csv[1][11]), true),
                                  'pin_code', TO_VARCHAR(DOC:csv[1][12]), true),
                                  'locno_act', TO_VARCHAR(DOC:csv[1][13]), true),
                                  '__client_name', '{client}', true), 
                                  '__source_name', '{table}', true), 
                                  '__schema_version', 'snowflake_historical', true), 
                                  '__event_timestamp', TO_VARCHAR(created), true),
                                  '__publish_timestamp', current_timestamp(), true),
                                  '__ingest_timestamp', current_timestamp(), true)
                    from OSR_KISOFT_FEED 
                    where (DOC:type = 'mod-ws') 
                        and created >= to_timestamp('{min_ts}') and created < to_timestamp('{max_ts}')
                )
                HEADER = FALSE
                OVERWRITE=TRUE"""

raw_sql = """copy into @csv_unload_file_stage/{table}/{subdir}/{table}_csv
                 from (
                        select doc
                        from OSR_KISOFT_FEED 
                        where (DOC:type = 'mod-ws')
                            and created >= to_timestamp('{min_ts}') and created < to_timestamp('{max_ts}')
                    )
                    HEADER = FALSE
                    OVERWRITE=TRUE"""

schema_version = "v2"

validation_sql = """
                WITH raw as (SELECT
    JSON_EXTRACT(raw_data, '$.csv') as csv,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(0)])[OFFSET(0)] as recordid,
  CAST(JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(0)])[OFFSET(1)] as INT64) as id,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(0)])[OFFSET(2)] as action,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(0)])[OFFSET(3)] as sub_action,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(0)])[OFFSET(4)] as systemid,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(0)] as record_id,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(1)] as event_id,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(2)] as wpono,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(3)] as cntno,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(4)] as master_fp_name,
  CAST(JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(5)] as INT64) as ws_no,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(6)] as status,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(7)] as error_id,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(8)] as ws_type,
  CAST(JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(9)] as INT64) as actqty,
  NULLIF(JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(10)], '')  as remark,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(11)] as itemno,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(12)] as pin_code,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(13)] as locno_act,
  JSON_EXTRACT_SCALAR(raw_data, '$.type') as type,
  JSON_EXTRACT_SCALAR(raw_data, '$.cmd') as cmd,
    STRUCT(JSON_EXTRACT_SCALAR(raw_data, '$.file.data') as data, JSON_EXTRACT_SCALAR(raw_data, '$.file.location-id') as location_id, JSON_EXTRACT_SCALAR(raw_data, '$.file.name') as name) as file
FROM
  `prj-daas-n-dev-dl-sub-bq-9220.datalake_sedanos.raw_osr_kisoft_feed_mod_ws`)

SELECT COUNT(*) FROM (SELECT dl_service.sort_json(dl_service.remove_nulls(to_json_string(raw)))
FROM raw
EXCEPT DISTINCT
SELECT dl_service.sort_json(dl_service.remove_nulls(to_json_string(t)))
                FROM (
                  SELECT NULLIF(remark, '') as remark,
                * EXCEPT(__client_name, __source_name, __schema_version, __event_timestamp, __publish_timestamp, __ingest_timestamp, remark)
                FROM `prj-daas-n-dev-dl-sub-bq-9220.datalake_sedanos.osr_kisoft_feed_mod_ws`) t)"""
