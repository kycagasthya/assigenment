
mapping_dev = [
    {'client': 'albertsons', 'database': 'ABS_DEV', 'min_ts': '2021-11-11T19:15:55.055000+00:00',
    'max_ts': '2022-09-21T11:09:43.248000+00:00'},
    {'client': 'ahold', 'database': 'ALPHA_DEV', 'min_ts': '2021-05-24T13:41:07.709000+00:00',
     'max_ts': '2022-08-10T11:53:47.494000+00:00'},
    {'client': 'big-y', 'database': 'BLUEBERRY_DEV', 'min_ts': '2021-03-29T19:08:02.788000+00:00',
    'max_ts': '2022-08-10T15:40:44.845000+00:00'},
    {'client': 'kroger', 'database': 'EIGHTYONE_DEV', 'min_ts': '2021-05-24T13:53:50.123000+00:00',
     'max_ts': '2022-08-11T09:27:09.745000+00:00'},
    {'client': 'loblaws', 'database': 'LOBSTER_DEV', 'min_ts': '2021-02-11T14:00:02.006000+00:00',
     'max_ts': '2022-09-21T11:30:12.306000+00:00'},
    {'client': 'maf', 'database': 'MAF_DEV', 'min_ts': '2021-03-08T19:19:56.002000+00:00',
     'max_ts': '2022-08-10T15:33:11.392000+00:00'},
    {'client': 'sedanos', 'database': 'SUNBIRD_DEV', 'min_ts': '2021-02-11T14:05:39.070000+00:00',
     'max_ts': '2022-02-17T05:10:09.938000+00:00'},
    {'client': 'woolworths', 'database': 'WINGS_DEV', 'min_ts': '2021-02-11T14:03:26.028000+00:00',
     'max_ts': '2022-09-12T15:06:07.816000+00:00'},
    {'client': 'wakefern', 'database': 'WINTER_DEV', 'min_ts': '2021-05-24T14:09:21.118000+00:00',
     'max_ts': '2022-09-23T08:50:29.419000+00:00'},
    {'client': 'tangerine-albertsons', 'database': 'TANGERINE_DEV',
     'min_ts': '2021-03-22T20:38:35.270000+00:00', 'max_ts': '2022-03-30T00:23:28.992000+00:00'}
]



mapping_prod = [
    {'client': 'albertsons', 'database': 'ABS', 'min_ts': '2021-11-11T19:15:55.055000+00:00',
    'max_ts': '2022-09-19T16:46:24.743353+00:00'},
    {'client': 'ahold', 'database': 'ALPHA', 'min_ts': '2021-05-24T13:41:07.709000+00:00',
     'max_ts': '2022-09-20T13:25:51.563742+00:00'},
    {'client': 'big-y', 'database': 'BLUEBERRY', 'min_ts': '2021-03-29T19:08:02.788000+00:00',
    'max_ts': '2022-09-20T15:41:47.367233+00:00'},
    {'client': 'kroger', 'database': 'EIGHTYONE', 'min_ts': '2021-05-24T13:53:50.123000+00:00',
     'max_ts': '2022-09-19T23:28:06.087239+00:00'},
    {'client': 'loblaws', 'database': 'LOBSTER', 'min_ts': '2021-02-11T14:00:02.006000+00:00',
     'max_ts': '2022-09-19T15:58:25.209559+00:00'},
    {'client': 'maf', 'database': 'MAF', 'min_ts': '2021-03-08T19:19:56.002000+00:00',
     'max_ts': '2022-09-19T16:21:33.978763+00:00'},
    {'client': 'sedanos', 'database': 'SUNBIRD', 'min_ts': '2021-02-11T14:05:39.070000+00:00',
     'max_ts': '2022-09-25T04:10:10.124000+00:00'},
    {'client': 'woolworths', 'database': 'WINGS', 'min_ts': '2021-02-11T14:03:26.028000+00:00',
     'max_ts': '2022-09-19T16:20:45.143096+00:00'},
    {'client': 'wakefern', 'database': 'WINTER', 'min_ts': '2021-05-24T14:09:21.118000+00:00',
     'max_ts': '2022-09-19T16:10:59.642534+00:00'},
    {'client': 'tangerine-albertsons', 'database': 'TANGERINE',
     'min_ts': '2021-03-22T20:38:35.270000+00:00', 'max_ts': '2022-03-30T00:23:28.992000+00:00'}
]

historical_sql = """copy into @json_unload_file_stage/{table}/{subdir}/{table}_json
             from (
		    select OBJECT_INSERT(
                              OBJECT_INSERT(
                                 OBJECT_INSERT(
                                    OBJECT_INSERT(
                                       OBJECT_INSERT(
                                          OBJECT_INSERT(
                                             OBJECT_INSERT(KEYS_TO_SNAKE(REMOVE_NULLS(DOC)),
                                             'attributes', TO_VARCHAR(doc:attributes), true),
                                          '__client_name', '{client}', true), 
                                       '__source_name', '{table}', true), 
                                    '__schema_version', 'snowflake_historical', true), 
                                 '__event_timestamp', TO_VARCHAR(created), true),
                              '__publish_timestamp', current_timestamp(), true),
                           '__ingest_timestamp', current_timestamp(), true)
                    from OSR_KISOFT_FEED_BIFROST_EXPORT
                    where created >= to_timestamp('{min_ts}') and created <= to_timestamp('{max_ts}')
                    and doc:action = 'move' and doc:subaction = 'stock'
                )
                HEADER = FALSE
                OVERWRITE=TRUE"""

raw_sql = """copy into @csv_unload_file_stage/{table}/{subdir}/{table}_csv
                 from (
                        select doc
                        from OSR_KISOFT_FEED_BIFROST_EXPORT
                        where doc:action = 'move' and doc:subaction = 'stock'
                            and created >= to_timestamp('{min_ts}') and created <= to_timestamp('{max_ts}')
                    )
                    HEADER = FALSE
                    OVERWRITE=TRUE"""

schema_version = "v1"

validation_sql = """
                SELECT COUNT(*) FROM (
                SELECT dl_service.delete_key(dl_service.remove_nulls(dl_service.format_ts(raw_data, ['creation_datetime', 'last_modified'])), ['index'])
                FROM datalake_{client}.raw_{table}
                EXCEPT DISTINCT
                SELECT dl_service.sort_json(dl_service.remove_nulls(to_json_string(t)))
                FROM (
                SELECT * EXCEPT(__client_name, __source_name, __schema_version, __event_timestamp, __publish_timestamp, __ingest_timestamp)
                FROM datalake_{client}.{table}
                WHERE __event_timestamp >= timestamp('{min_ts}') and __event_timestamp < timestamp('{max_ts}') 
                ) t
                ) a"""
