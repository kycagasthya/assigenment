mapping_dev = [
    {
        "client": "albertsons",
        "database": "ABS_DEV",
        "min_ts": "2021-11-01 00:00:00",
        "max_ts": "2021-12-01 00:00:00"
    },
    {
        "client": "ahold",
        "database": "ALPHA_DEV",
        "min_ts": "2021-11-01 00:00:00",
        "max_ts": "2021-12-01 00:00:00"
    },
    {
        "client": "big-y",
        "database": "BLUEBERRY_DEV",
        "min_ts": "2021-11-01 00:00:00",
        "max_ts": "2021-12-01 00:00:00"
    },
    {
        "client": "kroger",
        "database": "EIGHTYONE_DEV",
        "min_ts": "2021-11-01 00:00:00",
        "max_ts": "2021-12-01 00:00:00"
    },
    {
        "client": "loblaws",
        "database": "LOBSTER_DEV",
        "min_ts": "2021-11-01 00:00:00",
        "max_ts": "2021-12-01 00:00:00"
    },
    {
        "client": "maf",
        "database": "MAF_DEV",
        "min_ts": "2021-11-01 00:00:00",
        "max_ts": "2021-12-01 00:00:00"
    },
    {
        "client": "sedanos",
        "database": "SUNBIRD_DEV",
        "min_ts": "2021-11-01 00:00:00",
        "max_ts": "2021-12-01 00:00:00"
    },
    {
        "client": "tangerine-albertsons",
        "database": "TANGERINE_DEV",
        "min_ts": "2021-11-01 00:00:00",
        "max_ts": "2021-12-01 00:00:00"
    },
    {
        "client": "woolworths",
        "database": "WINGS_DEV",
        "min_ts": "2021-11-01 00:00:00",
        "max_ts": "2021-12-01 00:00:00"
    },
    {
        "client": "wakefern",
        "database": "WINTER_DEV",
        "min_ts": "2021-11-01 00:00:00",
        "max_ts": "2021-12-01 00:00:00"
    }
]

mapping_prod = [
    {
        "client": "albertsons",
        "database": "ABS",
        "min_ts": "2021-11-11T13:37:09.346556+00:00",
        "max_ts": "2022-06-10T15:37:05.247339+00:00"
    },
    {
        "client": "ahold",
        "database": "ALPHA",
        "min_ts": "2020-03-18T13:19:14.155000+00:00",
        "max_ts": "2022-06-10T15:33:05.388622+00:00"
    },
    {
        "client": "big-y",
        "database": "BLUEBERRY",
        "min_ts": "2021-04-01T20:27:20.394056+00:00",
        "max_ts": "2022-06-10T15:27:05.935634+00:00"
    },
    {
        "client": "kroger",
        "database": "EIGHTYONE",
        "min_ts": "2021-05-21T07:13:57.875394+00:00",
        "max_ts": "2022-06-10T15:27:05.854174+00:00"
    },
    {
        "client": "loblaws",
        "database": "LOBSTER",
        "min_ts": "2020-04-24T14:31:54.982000+00:00",
        "max_ts": "2022-06-10T15:54:05.199919+00:00"
    },
    {
        "client": "maf",
        "database": "MAF",
        "min_ts": "2021-02-11T18:27:16.985641+00:00",
        "max_ts": "2022-06-10T15:27:09.926752+00:00"
    },
    {
        "client": "sedanos",
        "database": "SUNBIRD",
        "min_ts": "2020-10-01T20:27:24.616257+00:00",
        "max_ts": "2022-01-21T19:21:12.530023+00:00"
    },
    {
        "client": "tangerine-albertsons",
        "database": "TANGERINE",
        "min_ts": "2020-05-22T11:11:26.297338+00:00",
        "max_ts": "2022-03-30T04:07:07.232199+00:00"
    },
    {
        "client": "woolworths",
        "database": "WINGS",
        "min_ts": "2020-09-25T17:59:05.274459+00:00",
        "max_ts": "2022-06-10T15:46:08.012718+00:00"
    },
    {
        "client": "wakefern",
        "database": "WINTER",
        "min_ts": "2020-03-18T12:54:03.157000+00:00",
        "max_ts": "2022-06-10T15:31:07.869184+00:00"
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
                    from {table}
                    where created >= to_timestamp('{min_ts}') and created < to_timestamp('{max_ts}')
                    and not (
                        IS_NULL_VALUE(etl_data:order_id)
                        or IS_NULL_VALUE(etl_data:store_id)
                        or IS_NULL_VALUE(etl_data:service_type)
                        or IS_NULL_VALUE(etl_data:spoke_id)
                        or IS_NULL_VALUE(etl_data:ecom_status)
                        or IS_NULL_VALUE(etl_data:route_number)
                        or IS_NULL_VALUE(etl_data:splitted)
                        or IS_NULL_VALUE(etl_data:empty_tom_items)
                        or IS_NULL_VALUE(etl_data:cancelled_by_client)
                        or IS_NULL_VALUE(etl_data:splitted_by_client)
                        or IS_NULL_VALUE(etl_data:batch_created)
                        or IS_NULL_VALUE(etl_data:order_id) is null
                        or IS_NULL_VALUE(etl_data:store_id) is null
                        or IS_NULL_VALUE(etl_data:service_type) is null
                        or IS_NULL_VALUE(etl_data:spoke_id) is null
                        or IS_NULL_VALUE(etl_data:ecom_status) is null
                        or IS_NULL_VALUE(etl_data:route_number) is null
                        or IS_NULL_VALUE(etl_data:splitted) is null
                        or IS_NULL_VALUE(etl_data:empty_tom_items) is null
                        or IS_NULL_VALUE(etl_data:cancelled_by_client) is null
                        or IS_NULL_VALUE(etl_data:splitted_by_client) is null
                        or IS_NULL_VALUE(etl_data:batch_created) is null
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
                        IS_NULL_VALUE(etl_data:order_id)
                        or IS_NULL_VALUE(etl_data:store_id)
                        or IS_NULL_VALUE(etl_data:service_type)
                        or IS_NULL_VALUE(etl_data:spoke_id)
                        or IS_NULL_VALUE(etl_data:ecom_status)
                        or IS_NULL_VALUE(etl_data:route_number)
                        or IS_NULL_VALUE(etl_data:splitted)
                        or IS_NULL_VALUE(etl_data:empty_tom_items)
                        or IS_NULL_VALUE(etl_data:cancelled_by_client)
                        or IS_NULL_VALUE(etl_data:splitted_by_client)
                        or IS_NULL_VALUE(etl_data:batch_created)
                        or IS_NULL_VALUE(etl_data:order_id) is null
                        or IS_NULL_VALUE(etl_data:store_id) is null
                        or IS_NULL_VALUE(etl_data:service_type) is null
                        or IS_NULL_VALUE(etl_data:spoke_id) is null
                        or IS_NULL_VALUE(etl_data:ecom_status) is null
                        or IS_NULL_VALUE(etl_data:route_number) is null
                        or IS_NULL_VALUE(etl_data:splitted) is null
                        or IS_NULL_VALUE(etl_data:empty_tom_items) is null
                        or IS_NULL_VALUE(etl_data:cancelled_by_client) is null
                        or IS_NULL_VALUE(etl_data:splitted_by_client) is null
                        or IS_NULL_VALUE(etl_data:batch_created) is null
                    )
                    )
                    HEADER = FALSE
                    OVERWRITE=TRUE"""

schema_version = "v1"

validation_sql = """
                SELECT COUNT(*) FROM (
                SELECT dl_service.delete_key(dl_service.remove_nulls(dl_service.format_ts(raw_data, ['creation_datetime', 
                'fulfillment_datetime', 'stage_by_datetime', 'cutoff_datetime', 'service_window_start', 'last_modified'])), ['index', 'shipping_label'])
                FROM datalake_{client}.raw_{table}
                EXCEPT DISTINCT
                SELECT dl_service.sort_json(dl_service.remove_nulls(to_json_string(t)))
                FROM (
                SELECT * EXCEPT(__client_name, __source_name, __schema_version, __event_timestamp, __publish_timestamp, __ingest_timestamp, shipping_label)
                FROM datalake_{client}.{table}
                WHERE __event_timestamp >= timestamp('{min_ts}') and __event_timestamp < timestamp('{max_ts}') 
                ) t
                ) a"""

