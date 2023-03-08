mapping_dev = [{'client': 'ahold', 'database': 'ALPHA_DEV', 'min_ts': '2020-08-27T10:55:38.606000+00:00',
                'max_ts': '2021-05-24T13:24:15.184000+00:00'},
               {'client': 'kroger', 'database': 'EIGHTYONE_DEV', 'min_ts': '2020-11-12T20:28:33.862000+00:00',
                'max_ts': '2021-03-15T14:20:12.043000+00:00'},
               {'client': 'loblaws', 'database': 'LOBSTER_DEV', 'min_ts': '2020-08-12T20:15:00.948000+00:00',
                'max_ts': '2021-03-05T13:55:13.902000+00:00'},
               {'client': 'maf', 'database': 'MAF_DEV', 'min_ts': '2021-02-01T13:35:02.572000+00:00',
                'max_ts': '2021-03-05T13:55:39.619000+00:00'},
               {'client': 'sedanos', 'database': 'SUNBIRD_DEV', 'min_ts': '2020-08-14T11:13:37.501000+00:00',
                'max_ts': '2021-02-22T05:10:13.139000+00:00'},
               {'client': 'woolworths', 'database': 'WINGS_DEV', 'min_ts': '2020-10-01T07:50:26.649000+00:00',
                'max_ts': '2021-03-05T13:56:34.666000+00:00'},
               {'client': 'wakefern', 'database': 'WINTER_DEV', 'min_ts': '2020-05-28T10:54:29.972000+00:00',
                'max_ts': '2021-05-24T13:24:18.756000+00:00'},
               {'client': 'tangerine-albertsons', 'database': 'TANGERINE_DEV',
                'min_ts': '2020-05-29T17:27:40.421000+00:00', 'max_ts': '2021-03-22T20:14:55.731000+00:00'}]

mapping_prod = [{'client': 'ahold', 'database': 'ALPHA', 'min_ts': '2020-08-26T07:25:58.759000+00:00',
                 'max_ts': '2021-05-24T13:24:15.184000+00:00'},
                {'client': 'kroger', 'database': 'EIGHTYONE', 'min_ts': '2020-11-12T12:40:17.283000+00:00',
                 'max_ts': '2021-03-15T14:20:12.043000+00:00'},
                {'client': 'loblaws', 'database': 'LOBSTER', 'min_ts': '2020-08-12T20:15:00.948000+00:00',
                 'max_ts': '2021-03-05T13:55:13.902000+00:00'},
                {'client': 'maf', 'database': 'MAF', 'min_ts': '2021-02-01T13:35:02.572000+00:00',
                 'max_ts': '2021-03-05T13:55:39.619000+00:00'},
                {'client': 'sedanos', 'database': 'SUNBIRD', 'min_ts': '2020-08-14T11:13:37.501000+00:00',
                 'max_ts': '2021-02-22T05:10:13.139000+00:00'},
                {'client': 'woolworths', 'database': 'WINGS', 'min_ts': '2020-10-01T07:50:26.649000+00:00',
                 'max_ts': '2021-03-05T13:56:34.666000+00:00'},
                {'client': 'wakefern', 'database': 'WINTER', 'min_ts': '2020-05-28T10:54:29.972000+00:00',
                 'max_ts': '2021-05-24T13:24:18.756000+00:00'},
                {'client': 'tangerine-albertsons', 'database': 'TANGERINE',
                 'min_ts': '2020-05-29T17:27:40.421000+00:00', 'max_ts': '2021-03-22T20:14:55.731000+00:00'}]

historical_sql = """copy into @json_unload_file_stage/{table}/{subdir}/{table}_json
                from (
                  select 
                  object_construct(
                           '__client_name', '{client}'
                         , '__source_name', '{table}'
                         , '__schema_version', 'snowflake_historical'
                         , '__event_timestamp', TO_VARCHAR(created)
                         , '__publish_timestamp', current_timestamp()
                         , '__ingest_timestamp', current_timestamp()
                         , 'created', created
                         , 'recordid', doc:csv[1][0]
                         , 'event_id', doc:csv[0][1]
                         , 'master_fp_name', doc:csv[1][2]
                         , 'itemno', doc:csv[1][3]
                         , 'expiry_date', doc:csv[1][4]
                         , 'reason', doc:csv[1][6]
                         , 'pin_code', doc:csv[1][8]
                         , 'locno_act', doc:csv[1][9]
                         , 'message_created', TO_VARCHAR(
                            CONVERT_TIMEZONE('UTC', TRY_TO_TIMESTAMP(DOC:csv[1][12]::TEXT,'YYYYMMDDHHMISS')::TIMESTAMP_NTZ),
                            'YYYYMMDDHHMISS')
                         , 'mfc_id', doc:file['location-id']
                         , 'records', array_construct(
                                        object_construct(
                                            'adjustment_type', doc:csv[1][7]
                                          , 'qty', doc:csv[1][5]
                                          , 'licenceplate', doc:csv[1][10]
                                          , 'slot_id', doc:csv[1][11])
                                       ,object_construct(
                                            'adjustment_type', doc:csv[2][7]
                                          , 'qty', doc:csv[2][5]
                                          , 'licenceplate', doc:csv[2][10]
                                          , 'slot_id', doc:csv[2][11])
                                      )
                         , 'csv', TO_VARCHAR(doc:csv)
                  )
                  from osr_kisoft_feed
                  where created >= to_timestamp('{min_ts}') and created <= to_timestamp('{max_ts}')
                  and doc:csv[0][2]='MOVE' and doc:csv[0][3]='STOCK'
                )
                HEADER = FALSE
                OVERWRITE=TRUE"""

raw_sql = """copy into @csv_unload_file_stage/{table}/{subdir}/{table}_csv
                 from (
                        select doc
                        from osr_kisoft_feed 
                        where doc:csv[0][2]='MOVE' and doc:csv[0][3]='STOCK'
                            and created >= to_timestamp('{min_ts}') and created <= to_timestamp('{max_ts}')   
                    )
                    HEADER = FALSE
                    OVERWRITE=TRUE"""

schema_version = "v1"

validation_sql = """
                WITH raw as (SELECT
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(0)] as recordid,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(1)] as event_id,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(2)] as master_fp_name,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(3)] as itemno,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(4)] as expiry_date,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(6)] as reason,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(8)] as pin_code,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(9)] as locno_act,
  JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(12)] as message_created,
  JSON_EXTRACT_SCALAR(raw_data, '$.file.location-id') as mfc_id,
  [STRUCT(
    JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(7)] as adjustment_type,
    CAST(JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(5)] as INT64) as qty,
    JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(10)] as licenceplate,
    CAST(JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(1)])[OFFSET(11)] as INT64) as slot_id
  ), STRUCT(
    JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(2)])[OFFSET(7)] as adjustment_type,
    CAST(JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(2)])[OFFSET(5)] as INT64) as qty,
    JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(2)])[OFFSET(10)] as licenceplate,
    CAST(JSON_EXTRACT_STRING_ARRAY(JSON_EXTRACT_ARRAY(JSON_EXTRACT(raw_data, '$.csv'))[OFFSET(2)])[OFFSET(11)] as INT64) as slot_id
  )] as records,
  JSON_EXTRACT(raw_data, '$.csv') as csv,
FROM
  `prj-daas-n-dev-dl-sub-bq-9220.datalake_kroger.raw_osr_kisoft_feed_merge_and_defrag`)

SELECT COUNT(*) FROM (SELECT dl_service.sort_json(dl_service.remove_nulls(to_json_string(raw)))
FROM raw
EXCEPT DISTINCT
SELECT dl_service.sort_json(dl_service.remove_nulls(to_json_string(t)))
                FROM (SELECT * EXCEPT(__client_name, __source_name, __schema_version, __event_timestamp, __publish_timestamp, __ingest_timestamp, created)
                FROM `prj-daas-n-dev-dl-sub-bq-9220.datalake_kroger.osr_kisoft_feed_merge_and_defrag`) t)"""
