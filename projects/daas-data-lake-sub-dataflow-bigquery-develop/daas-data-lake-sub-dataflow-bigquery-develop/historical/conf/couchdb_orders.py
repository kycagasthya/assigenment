mapping_dev = [
    {
        "client": "albertsons",
        "database": "ABS_DEV",
        "min_ts": "2021-11-15T12:31:11.883000+00:00",
        "max_ts": "2022-09-21T10:57:23.205000+00:00"
    },
    {
        "client": "ahold",
        "database": "ALPHA_DEV",
        "min_ts": "2020-05-01T15:16:22.000000+00:00",
        "max_ts": "2022-08-10T11:58:47.477000+00:00"
    },
    {
        "client": "big-y",
        "database": "BLUEBERRY_DEV",
        "min_ts": "2021-03-29T19:13:41.221000+00:00",
        "max_ts": "2022-08-10T15:37:47.396000+00:00"
    },
    {
        "client": "kroger",
        "database": "EIGHTYONE_DEV",
        "min_ts": "2021-05-18T21:25:17.985000+00:00",
        "max_ts": "2022-08-11T09:19:47.215000+00:00"
    },
    {
        "client": "loblaws",
        "database": "LOBSTER_DEV",
        "min_ts": "2020-04-24T14:29:12.793000+00:00",
        "max_ts": "2022-09-21T08:04:14.845000+00:00"
    },
    {
        "client": "maf",
        "database": "MAF_DEV",
        "min_ts": "2021-02-03T07:48:21.071000+00:00",
        "max_ts": "2022-08-10T15:33:25.273000+00:00"
    },
    {
        "client": "sedanos",
        "database": "SUNBIRD_DEV",
        "min_ts": "2020-04-27T19:42:37.978000+00:00",
        "max_ts": "2022-01-21T18:55:33.256000+00:00"
    },
    {
        "client": "tangerine-albertsons",
        "database": "TANGERINE_DEV",
        "min_ts": "2020-05-04T13:48:48.372000+00:00",
        "max_ts": "2022-03-30T00:15:56.655000+00:00"
    },
    {
        "client": "woolworths",
        "database": "WINGS_DEV",
        "min_ts": "2020-09-24T19:46:25.138000+00:00",
        "max_ts": "2022-09-12T14:57:49.438000+00:00"
    },
    {
        "client": "wakefern",
        "database": "WINTER_DEV",
        "min_ts": "2020-05-01T15:17:15.232000+00:00",
        "max_ts": "2022-09-26T12:18:33.386000+00:00"
    },
    {
        "client": "smu",
        "database": "SMU_DEV",
        "min_ts": "2022-07-22T12:57:08.731000+00:00",
        "max_ts": "2022-07-22T12:57:08.736000+00:00"
    }
]

mapping_prod = [
    {
        "client": "albertsons",
        "database": "ABS",
        "min_ts": "2021-11-15T12:31:11.883000+00:00",
        "max_ts": "2022-09-29T20:43:04.564000+00:00"
    },
    {
        "client": "ahold",
        "database": "ALPHA",
        "min_ts": "2020-05-01T15:16:22.000000+00:00",
        "max_ts": "2022-09-29T20:41:03.257000+00:00"
    },
    {
        "client": "big-y",
        "database": "BLUEBERRY",
        "min_ts": "2021-03-29T19:13:41.221000+00:00",
        "max_ts": "2022-09-29T18:57:32.309000+00:00"
    },
    {
        "client": "kroger",
        "database": "EIGHTYONE",
        "min_ts": "2021-05-18T21:25:17.985000+00:00",
        "max_ts": "2022-09-29T20:41:09.007000+00:00"
    },
    {
        "client": "loblaws",
        "database": "LOBSTER",
        "min_ts": "2020-04-24T14:29:12.793000+00:00",
        "max_ts": "2022-09-29T15:31:41.667000+00:00"
    },
    {
        "client": "maf",
        "database": "MAF",
        "min_ts": "2021-02-03T07:48:21.071000+00:00",
        "max_ts": "2022-09-29T19:51:03.227000+00:00"
    },
    {
        "client": "sedanos",
        "database": "SUNBIRD",
        "min_ts": "2020-04-27T19:42:37.978000+00:00",
        "max_ts": "2022-08-12T14:39:29.905000+00:00"
    },
    {
        "client": "tangerine-albertsons",
        "database": "TANGERINE",
        "min_ts": "2020-05-04T13:48:48.372000+00:00",
        "max_ts": "2022-03-30T00:15:56.655000+00:00"
    },
    {
        "client": "woolworths",
        "database": "WINGS",
        "min_ts": "2020-09-24T19:46:25.138000+00:00",
        "max_ts": "2022-09-29T20:39:38.294000+00:00"
    },
    {
        "client": "wakefern",
        "database": "WINTER",
        "min_ts": "2020-05-01T15:17:15.232000+00:00",
        "max_ts": "2022-09-29T20:47:30.405000+00:00"
    },
    {
        "client": "smu",
        "database": "SMU",
        "min_ts": "2022-07-22T12:57:08.731000+00:00",
        "max_ts": "2022-09-29T17:14:05.394000+00:00"
    }
]

historical_sql = """copy into @json_unload_file_stage/{table}/{subdir}/{table}_json
             from (
                    with orders as (
                          select *
                          from tom_o
                          where created >= to_timestamp('{min_ts}') and created <= to_timestamp('{max_ts}')
                        )
                        , items as (
                          select tom_o_pk, array_agg(object_delete(value, 'base_price', 'unit_price')) as items_arr
                          from orders, lateral flatten(doc:items)
                          group by tom_o_pk
                        )
                        select OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT( KEYS_TO_SNAKE(REMOVE_NULLS(
                                OBJECT_INSERT(OBJECT_INSERT(OBJECT_PICK(doc, ['_id', '_rev', '_deleted', 'batch_order_id', 'boxes', 'boxes_retrieved'
                                                 , 'boxes_retrieved_time', 'client_id', 'created' , 'delivery_contract_id', 'delivery_contract_params'
                                                 , 'items', 'location_id', 'packer_id', 'picker_id', 'picking_method', 'route_number', 'secret'
                                                 , 'sent_to_queue', 'served', 'shift_number', 'stage_by_datetime', 'stage_location', 'status'
                                                 , 'stop_number', 'tax', 'totes_unstaged', 'totes_unstaged_time', 'totes_unstaging_error_reason']), 
                                         'delivery_contract_params', object_delete(doc:delivery_contract_params, 'dump'), true),
                                        'items', items.items_arr, true))),
                                        '__client_name', '{client}', true), 
                                        '__source_name', '{table}', true), 
                                        '__schema_version', 'snowflake_historical', true), 
                                        '__event_timestamp', TO_VARCHAR(created), true),
                                        '__publish_timestamp', null, true),
                                        '__ingestion_timestamp', null, true)
                        from orders 
                        left join items on orders.tom_o_pk = items.tom_o_pk
                )
                HEADER = FALSE
                OVERWRITE=TRUE"""

raw_sql = """copy into @csv_unload_file_stage/{table}/{subdir}/{table}_csv
                 from (
                        select doc
                        from tom_o
                        where created >= to_timestamp('{min_ts}') and created <= to_timestamp('{max_ts}')
                    )
                    HEADER = FALSE
                    OVERWRITE=TRUE"""

schema_version = "v2"

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
