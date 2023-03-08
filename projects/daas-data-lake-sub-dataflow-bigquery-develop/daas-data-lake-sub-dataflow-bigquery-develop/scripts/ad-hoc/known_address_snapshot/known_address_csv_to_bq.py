import pandas as pd
import argparse
import logging
import datetime
import json

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('project_id')
    parser.add_argument('source_csv')
    parser.add_argument('client')

    args = parser.parse_args()

    dest_cols = {
        "address": pd.Series(dtype='str'),
        "area": pd.Series(dtype='str'),
        "temp_zone": pd.Series(dtype='str'),
        "aisle": pd.Series(dtype='str'),
        "bay": pd.Series(dtype='str'),
        "stack": pd.Series(dtype='str'),
        "shelf": pd.Series(dtype='str'),

        "overstock": pd.Series(dtype='bool'),
        "dynamic": pd.Series(dtype='bool'),
        "pickable": pd.Series(dtype='bool'),
        "active": pd.Series(dtype='bool'),

        "mfc_id": pd.Series(dtype='str'),
        "pick_zone": pd.Series(dtype='str'),

        "pubsub_message_id": pd.Series(dtype='str'),
        "pubsub_publish_time": pd.Series(dtype='datetime64[ms]'),
        "attributes": pd.Series(dtype='str'),

        "__client_name": pd.Series(dtype='str'),
        "__source_name": pd.Series(dtype='str'),
        "__schema_version": pd.Series(dtype='str'),
        "__event_timestamp": pd.Series(dtype='datetime64[ms]'),
        "__ingest_timestamp": pd.Series(dtype='datetime64[ms]'),
        "__publish_timestamp": pd.Series(dtype='datetime64[ms]'),
        "__pubsub_message_id": pd.Series(dtype='str'),

    }
    num_cols = 12
    source_df = pd.read_csv(args.source_csv, delimiter=',',
                            header=None,
                            dtype={i: str for i in range(12)},
                            keep_default_na=False)

    result_df = pd.DataFrame(dest_cols)

    dt_now = datetime.datetime.utcnow()

    result_df["address"] = source_df[0]
    result_df["area"] = source_df[1]
    result_df["temp_zone"] = source_df[2]
    result_df["aisle"] = source_df[3]
    result_df["bay"] = source_df[4]
    result_df["stack"] = source_df[5]
    result_df["shelf"] = source_df[6]

    result_df["overstock"] = source_df[7].str.lower() == 't'
    result_df["dynamic"] = source_df[8].str.lower() == 't'
    result_df["pickable"] = source_df[9].str.lower() == 't'
    result_df["active"] = source_df[10].str.lower() == 't'

    result_df["mfc_id"] = source_df[11]
    result_df["pick_zone"] = None

    result_df["pubsub_message_id"] = None
    result_df["pubsub_publish_time"] = None
    result_df["attributes"] = "{}"

    result_df["__client_name"] = args.client if args.client != 'big_y' else 'big-y'
    result_df["__source_name"] = 'known_address'
    result_df["__schema_version"] = 'one_time_snapshot'
    result_df["__event_timestamp"] = dt_now
    result_df["__ingest_timestamp"] = dt_now
    result_df["__publish_timestamp"] = dt_now
    result_df["__pubsub_message_id"] = None

    dest_table = f'{args.project_id}.datalake_{args.client}.known_address'
    with open('known_address_schema.json', 'r') as f:
        schema = json.load(f)
    result_df.to_gbq(dest_table, table_schema=schema, if_exists='append')
