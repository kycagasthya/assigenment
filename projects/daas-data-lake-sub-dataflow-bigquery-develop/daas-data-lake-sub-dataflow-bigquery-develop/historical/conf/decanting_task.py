mapping_dev = [
    {
        "client": "albertsons",
        "database": "ABS_DEV",
        "min_ts": "2022-06-22T15:38:10.151821+00:00",
        "max_ts": "2022-07-22T11:23:05.041177+00:00"
    },
    {
        "client": "ahold",
        "database": "ALPHA_DEV",
        "min_ts": "2022-06-22T10:00:14.810960+00:00",
        "max_ts": "2022-07-22T11:53:04.818415+00:00"
    },
    {
        "client": "big-y",
        "database": "BLUEBERRY_DEV",
        "min_ts": "2022-06-22T19:23:34.299513+00:00",
        "max_ts": "2022-07-22T11:53:04.273786+00:00"
    },
    {
        "client": "kroger",
        "database": "EIGHTYONE_DEV",
        "min_ts": "2022-06-21T14:38:15.162972+00:00",
        "max_ts": "2022-07-21T06:53:05.239949+00:00"
    },
    {
        "client": "loblaws",
        "database": "LOBSTER_DEV",
        "min_ts": "2022-06-22T19:23:11.326394+00:00",
        "max_ts": "2022-07-22T11:38:04.049674+00:00"
    },
    {
        "client": "maf",
        "database": "MAF_DEV",
        "min_ts": "2022-06-22T03:23:20.028428+00:00",
        "max_ts": "2022-07-22T12:23:06.344214+00:00"
    },
    {
        "client": "sedanos",
        "database": "SUNBIRD_DEV",
        "min_ts": "2021-12-20T10:00:15.163633+00:00",
        "max_ts": "2022-01-20T16:23:13.854457+00:00"
    },
    {
        "client": "woolworths",
        "database": "WINGS_DEV",
        "min_ts": "2022-06-22T21:38:14.777026+00:00",
        "max_ts": "2022-07-22T13:53:07.266598+00:00"
    },
    {
        "client": "tangerine-albertsons",
        "database": "TANGERINE_DEV",
        "min_ts": "2022-02-27T09:45:13.996064+00:00",
        "max_ts": "2022-03-30T03:53:12.845738+00:00"
    },
    {
        "client": "wakefern",
        "database": "WINTER_DEV",
        "min_ts": "2022-06-21T10:30:09.789616+00:00",
        "max_ts": "2022-07-21T10:53:04.528354+00:00"
    }
]

mapping_prod = [
    {
        "client": "albertsons",
        "database": "ABS",
        "min_ts": "2021-11-17T15:38:10.151821+00:00",
        "max_ts": "2022-08-02T21:38:05.388561+00:00"
    },
    {
        "client": "ahold",
        "database": "ALPHA",
        "min_ts": "2020-11-09T10:00:14.810960+00:00",
        "max_ts": "2022-08-02T21:38:04.280572+00:00"
    },
    {
        "client": "big-y",
        "database": "BLUEBERRY",
        "min_ts": "2021-03-29T19:23:34.299513+00:00",
        "max_ts": "2022-08-02T18:23:04.430393+00:00"
    },
    {
        "client": "kroger",
        "database": "EIGHTYONE",
        "min_ts": "2020-11-18T14:38:15.162972+00:0",
        "max_ts": "2022-08-02T04:23:06.070285+00:00"
    },
    {
        "client": "loblaws",
        "database": "LOBSTER",
        "min_ts": "2020-11-30T19:23:11.326394+00:00",
        "max_ts": "2022-08-02T21:38:04.273177+00:00"
    },
    {
        "client": "maf",
        "database": "MAF",
        "min_ts": "2021-02-02T03:23:20.028428+00:00",
        "max_ts": "2022-08-02T21:38:06.383379+00:00"
    },
    {
        "client": "sedanos",
        "database": "SUNBIRD",
        "min_ts": "2020-11-09T10:00:15.163633+00:00",
        "max_ts": "2022-01-20T16:23:13.854457+00:00"
    },
    {
        "client": "tangerine-albertsons",
        "database": "TANGERINE",
        "min_ts": "2020-11-09T09:45:13.996064+00:00",
        "max_ts": "2022-03-30T03:53:12.845738+00:00"
    },
    {
        "client": "woolworths",
        "database": "WINGS",
        "min_ts": "2020-11-18T21:38:14.777026+00:00",
        "max_ts": "2022-08-02T21:38:06.929572+00:00"
    },
    {
        "client": "wakefern",
        "database": "WINTER",
        "min_ts": "2020-11-09T10:30:09.789616+00:00",
        "max_ts": "2022-08-02T21:38:05.052539+00:00"
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
                            IS_NULL_VALUE(etl_data:id)
                            or IS_NULL_VALUE(etl_data:purchase_order)
                            or IS_NULL_VALUE(etl_data:created)
                            or IS_NULL_VALUE(etl_data:mfc)
                            or IS_NULL_VALUE(etl_data:status)
                            or IS_NULL_VALUE(etl_data:id) is NULL
                            or IS_NULL_VALUE(etl_data:purchase_order) is NULL
                            or IS_NULL_VALUE(etl_data:created) is NULL
                            or IS_NULL_VALUE(etl_data:mfc) is NULL
                            or IS_NULL_VALUE(etl_data:status) is NULL
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
                            IS_NULL_VALUE(etl_data:id)
                            or IS_NULL_VALUE(etl_data:purchase_order)
                            or IS_NULL_VALUE(etl_data:created)
                            or IS_NULL_VALUE(etl_data:mfc)
                            or IS_NULL_VALUE(etl_data:status)
                            or IS_NULL_VALUE(etl_data:id) is NULL
                            or IS_NULL_VALUE(etl_data:purchase_order) is NULL
                            or IS_NULL_VALUE(etl_data:created) is NULL
                            or IS_NULL_VALUE(etl_data:mfc) is NULL
                            or IS_NULL_VALUE(etl_data:status) is NULL
                        )
                )
                    HEADER = FALSE
                    OVERWRITE=TRUE"""

schema_version = "v1"

validation_sql = """
                SELECT COUNT(*) FROM (
                SELECT dl_service.delete_key(dl_service.remove_nulls(dl_service.format_ts(raw_data, ['created', 'date_expected', 'last_modified'])), ['index'])
                FROM datalake_{client}.raw_{table}
                EXCEPT DISTINCT
                SELECT dl_service.sort_json(dl_service.remove_nulls(to_json_string(t)))
                FROM (
                SELECT * EXCEPT(__client_name, __source_name, __schema_version, __event_timestamp, __publish_timestamp, __ingest_timestamp)
                FROM datalake_{client}.{table}
                WHERE __event_timestamp >= timestamp('{min_ts}') and __event_timestamp < timestamp('{max_ts}') 
                ) t
                ) a"""
