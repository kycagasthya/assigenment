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
        "min_ts": "2021-11-11T13:22:48.691811+00:00",
        "max_ts": "2022-05-29T06:06:05.498847+00:00"
    },
    {
        "client": "ahold",
        "database": "ALPHA",
        "min_ts": "2020-05-15T14:01:22.889203+00:00",
        "max_ts": "2022-05-29T06:06:05.337965+00:00"
    },
    {
        "client": "big-y",
        "database": "BLUEBERRY",
        "min_ts": "2021-03-30T06:16:13.668262+00:00",
        "max_ts": "2022-05-29T06:16:04.961381+00:00"
    },
    {
        "client": "kroger",
        "database": "EIGHTYONE",
        "min_ts": "2020-10-22T06:16:08.423455+00:00",
        "max_ts": "2022-05-29T06:16:05.364171+00:00"
    },
    {
        "client": "loblaws",
        "database": "LOBSTER",
        "min_ts": "2020-05-15T14:06:29.823797+00:00",
        "max_ts": "2022-05-29T06:06:04.637342+00:00"
    },
    {
        "client": "maf",
        "database": "MAF",
        "min_ts": "2021-01-27T06:16:20.305512+00:00",
        "max_ts": "2022-05-29T06:16:07.219172+00:00"
    },
    {
        "client": "sedanos",
        "database": "SUNBIRD",
        "min_ts": "2020-05-15T14:09:03.730698+00:00",
        "max_ts": "2022-05-29T06:06:05.093478+00:00"
    },
    {
        "client": "tangerine-albertsons",
        "database": "TANGERINE",
        "min_ts": "2020-05-15T14:34:19.054885+00:00",
        "max_ts": "2022-04-19T06:06:09.752751+00:00"
    },
    {
        "client": "woolworths",
        "database": "WINGS",
        "min_ts": "2020-09-24T19:56:16.142012+00:00",
        "max_ts": "2022-05-29T06:16:08.047208+00:00"
    },
    {
        "client": "wakefern",
        "database": "WINTER",
        "min_ts": "2020-05-15T14:13:04.160418+00:00",
        "max_ts": "2022-05-30T00:01:06.854218+00:00"
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
                                IS_NULL_VALUE(etl_data:location_id)
                                --or IS_NULL_VALUE(etl_data:is_enabled) 
                                or IS_NULL_VALUE(etl_data:location_city) 
                                or IS_NULL_VALUE(etl_data:location_code_retailer) 
                                or IS_NULL_VALUE(etl_data:location_code_tom) 
                                or IS_NULL_VALUE(etl_data:location_contact_phone) 
                                or IS_NULL_VALUE(etl_data:location_street) 
                                or IS_NULL_VALUE(etl_data:location_name) 
                                or IS_NULL_VALUE(etl_data:location_type_id) 
                                or IS_NULL_VALUE(etl_data:location_zip_code) 
                                or IS_NULL_VALUE(etl_data:state_iso_code) 
                                or IS_NULL_VALUE(etl_data:timezone)
                                or IS_NULL_VALUE(etl_data:location_id) is null
                             --   or IS_NULL_VALUE(etl_data:is_enabled) is null
                                or IS_NULL_VALUE(etl_data:location_city) is null
                                or IS_NULL_VALUE(etl_data:location_code_retailer) is null
                                or IS_NULL_VALUE(etl_data:location_code_tom) is null
                                or IS_NULL_VALUE(etl_data:location_contact_phone) is null
                                or IS_NULL_VALUE(etl_data:location_street) is null
                                or IS_NULL_VALUE(etl_data:location_name) is null
                                or IS_NULL_VALUE(etl_data:location_type_id) is null
                                or IS_NULL_VALUE(etl_data:location_zip_code) is null
                                or IS_NULL_VALUE(etl_data:state_iso_code) is null
                                or IS_NULL_VALUE(etl_data:timezone) is null
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
                                IS_NULL_VALUE(etl_data:location_id)
                                --or IS_NULL_VALUE(etl_data:is_enabled) 
                                or IS_NULL_VALUE(etl_data:location_city) 
                                or IS_NULL_VALUE(etl_data:location_code_retailer) 
                                or IS_NULL_VALUE(etl_data:location_code_tom) 
                                or IS_NULL_VALUE(etl_data:location_contact_phone) 
                                or IS_NULL_VALUE(etl_data:location_street) 
                                or IS_NULL_VALUE(etl_data:location_name) 
                                or IS_NULL_VALUE(etl_data:location_type_id) 
                                or IS_NULL_VALUE(etl_data:location_zip_code) 
                                or IS_NULL_VALUE(etl_data:state_iso_code) 
                                or IS_NULL_VALUE(etl_data:timezone)
                                or IS_NULL_VALUE(etl_data:location_id) is null
                             --   or IS_NULL_VALUE(etl_data:is_enabled) is null
                                or IS_NULL_VALUE(etl_data:location_city) is null
                                or IS_NULL_VALUE(etl_data:location_code_retailer) is null
                                or IS_NULL_VALUE(etl_data:location_code_tom) is null
                                or IS_NULL_VALUE(etl_data:location_contact_phone) is null
                                or IS_NULL_VALUE(etl_data:location_street) is null
                                or IS_NULL_VALUE(etl_data:location_name) is null
                                or IS_NULL_VALUE(etl_data:location_type_id) is null
                                or IS_NULL_VALUE(etl_data:location_zip_code) is null
                                or IS_NULL_VALUE(etl_data:state_iso_code) is null
                                or IS_NULL_VALUE(etl_data:timezone) is null
                            )
                    )
                    HEADER = FALSE
                    OVERWRITE=TRUE"""

schema_version = "v2"

validation_sql = """
                SELECT COUNT(*) FROM (
                SELECT dl_service.delete_key(dl_service.remove_nulls(raw_data), ['index', 'location_pickup_lon', 'location_pickup_lat'])
                FROM datalake_{client}.raw_{table}
                EXCEPT DISTINCT
                SELECT dl_service.sort_json(dl_service.remove_nulls(to_json_string(t)))
                FROM (
                SELECT * EXCEPT(__client_name, __source_name, __schema_version, __event_timestamp, __publish_timestamp, __ingest_timestamp,
                                location_pickup_lat, location_pickup_lon)
                FROM datalake_{client}.{table}
                WHERE __event_timestamp >= timestamp('{min_ts}') and __event_timestamp < timestamp('{max_ts}') 
                ) t
                ) a"""