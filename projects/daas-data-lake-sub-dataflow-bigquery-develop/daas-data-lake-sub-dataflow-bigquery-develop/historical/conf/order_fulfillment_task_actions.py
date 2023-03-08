mapping_dev = [
    {
        "client": "albertsons",
        "database": "ABS_DEV",
        "min_ts": "2022-08-16T00:00:00.000+00:00",
        "max_ts": "2022-11-04T00:00:00.000+00:00",
        "json_unload_file_stage": "json_unload_file_stage_target_stg",
        "csv_unload_file_stage": "csv_unload_file_stage_target_stg"
    },
    # {   # no data on Snowflake dev
    #     "client": "ahold",
    #     "database": "ALPHA_DEV",
    #     "min_ts": "2021-06-07T00:00:00.000+00:00",
    #     "max_ts": "2022-08-11T00:00:00.000+00:00",
    #     "json_unload_file_stage": "json_unload_file_stage_target_stg",
    #     "csv_unload_file_stage": "csv_unload_file_stage_target_stg"
    # },
    {
        "client": "big-y",
        "database": "BLUEBERRY_DEV",
        "min_ts": "2022-06-22T00:00:00.000+00:00",
        "max_ts": "2022-11-07T00:00:00.000+00:00",
        "json_unload_file_stage": "json_unload_file_stage_target_stg",
        "csv_unload_file_stage": "csv_unload_file_stage_target_stg"
    },
    # {   # no data on Snowflake dev
    #     "client": "kroger",
    #     "database": "EIGHTYONE_DEV",
    #     "min_ts": "2021-06-08T00:00:00.000+00:00",
    #     "max_ts": "2022-08-12T00:00:00.000+00:00",
    #     "json_unload_file_stage": "json_unload_file_stage_target_stg",
    #     "csv_unload_file_stage": "csv_unload_file_stage_target_stg"
    # },
    {
        "client": "loblaws",
        "database": "LOBSTER_DEV",
        "min_ts": "2022-08-15T00:00:00.000+00:00",
        "max_ts": "2022-11-11T00:00:00.000+00:00",
        "json_unload_file_stage": "json_unload_file_stage_target_stg",
        "csv_unload_file_stage": "csv_unload_file_stage_target_stg"
    },
    {
        "client": "maf",
        "database": "MAF_DEV",
        "min_ts": "2022-09-02T00:00:00.000+00:00",
        "max_ts": "2022-09-16T00:00:00.000+00:00",
        "json_unload_file_stage": "json_unload_file_stage_target_stg",
        "csv_unload_file_stage": "csv_unload_file_stage_target_stg"
    },
    # {   # table does not exist on Snowflake dev
    #     "client": "sedanos",
    #     "database": "SUNBIRD_DEV",
    #     "min_ts": "2021-04-27T00:00:00.000+00:00",
    #     "max_ts": "2021-11-30T00:00:00.000+00:00",
    #     "json_unload_file_stage": "json_unload_file_stage_target_stg",
    #     "csv_unload_file_stage": "csv_unload_file_stage_target_stg"
    # },
    # {   # no data on Snowflake dev
    #     "client": "smu",
    #     "database": "SMU_DEV",
    #     "min_ts": "2021-04-27T00:00:00.000+00:00",
    #     "max_ts": "2021-11-30T00:00:00.000+00:00",
    #     "json_unload_file_stage": "json_unload_file_stage_target_stg",
    #     "csv_unload_file_stage": "csv_unload_file_stage_target_stg"
    # },
    {
        "client": "wakefern",
        "database": "WINTER_DEV",
        "min_ts": "2022-07-20T00:00:00.000+00:00",
        "max_ts": "2022-10-03T00:00:00.000+00:00",
        "json_unload_file_stage": "json_unload_file_stage_target_stg",
        "csv_unload_file_stage": "csv_unload_file_stage_target_stg"
    },
    {
        "client": "woolworths",
        "database": "WINGS_DEV",
        "min_ts": "2022-08-24T00:00:00.000+00:00",
        "max_ts": "2022-08-25T00:00:00.000+00:00",
        "json_unload_file_stage": "json_unload_file_stage_target_stg",
        "csv_unload_file_stage": "csv_unload_file_stage_target_stg"
    }
]

mapping_prod = [
    {
        "client": "albertsons",
        "database": "ABS",
        "min_ts": "2022-06-16T00:00:00.000+00:00",
        "max_ts": "2022-09-15T00:00:00.000+00:00"
    },
    {
        "client": "ahold",
        "database": "ALPHA",
        "min_ts": "2022-09-14T00:00:00.000+00:00",
        "max_ts": "2022-09-15T00:00:00.000+00:00"
    },
    {
        "client": "big-y",
        "database": "BLUEBERRY",
        "min_ts": "2022-06-22T00:00:00.000+00:00",
        "max_ts": "2022-10-20T00:00:00.000+00:00"
    },
    # {   # no data on Snowflake PROD
    #     "client": "kroger",
    #     "database": "EIGHTYONE",
    #     "min_ts": "2021-06-08T00:00:00.000+00:00",
    #     "max_ts": "2022-08-12T00:00:00.000+00:00"
    # },
    {
        "client": "loblaws",
        "database": "LOBSTER",
        "min_ts": "2022-08-15T00:00:00.000+00:00",
        "max_ts": "2022-10-28T13:23:10.000+00:00"
    },
    {
        "client": "maf",
        "database": "MAF",
        "min_ts": "2022-09-02T00:00:00.000+00:00",
        "max_ts": "2022-09-16T00:00:00.000+00:00"
    },
    # {   # table does not exist on Snowflake PROD
    #     "client": "sedanos",
    #     "database": "SUNBIRD",
    #     "min_ts": "2021-04-27T00:00:00.000+00:00",
    #     "max_ts": "2021-11-30T00:00:00.000+00:00"
    # },
    # {   # no data on Snowflake PROD
    #     "client": "smu",
    #     "database": "SMU",
    #     "min_ts": "2021-04-27T00:00:00.000+00:00",
    #     "max_ts": "2021-11-30T00:00:00.000+00:00"
    # },
    {
        "client": "wakefern",
        "database": "WINTER",
        "min_ts": "2022-07-20T00:00:00.000+00:00",
        "max_ts": "2022-10-03T00:00:00.000+00:00"
    },
    {
        "client": "woolworths",
        "database": "WINGS",
        "min_ts": "2022-08-24T00:00:00.000+00:00",
        "max_ts": "2022-10-11T00:00:00.000+00:00"
    }
]

historical_sql = """copy into @{json_unload_file_stage}/{table}/{subdir}/{table}_json
             from (
                    select ADD_MISSING_EMBEDDED_COLUMNS(
                             OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(REMOVE_NULLS(DOC) , 'attributes', TO_VARCHAR(doc:attributes), true), 
                                  '__client_name', '{client}', true), 
                                  '__source_name', '{table}', true), 
                                  '__schema_version', 'snowflake_historical', true), 
                                  '__event_timestamp', TO_VARCHAR(created), true),
                                  '__publish_timestamp', null, true),
                                  '__ingest_timestamp', current_timestamp(), true),
                                  'pick', object_delete(doc['pick'], 'needsManualEntry'), true),
                                  'newStep', null, true),
                            'pick.barcodes', 'checkDigit')
                    from ORDER_FULFILLMENT_TASK_ACTIONS
                    where 1=1
                      and IS_NULL_VALUE(DOC['order_part_id']) is null
                      and created >= to_timestamp('{min_ts}') and created < to_timestamp('{max_ts}')
                )
                HEADER = FALSE
                OVERWRITE=TRUE"""

raw_sql = """copy into @{csv_unload_file_stage}/{table}/{subdir}/{table}_csv
                 from (
                        select doc
                        from ORDER_FULFILLMENT_TASK_ACTIONS
                        where 1=1
                          and IS_NULL_VALUE(DOC['order_part_id']) is null
                          and created >= to_timestamp('{min_ts}') and created < to_timestamp('{max_ts}')
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
