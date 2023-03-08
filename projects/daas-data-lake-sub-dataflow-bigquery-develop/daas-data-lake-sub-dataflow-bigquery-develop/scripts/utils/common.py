OPTIONAL_COLUMNS = [
    {
        "name": "__ingest_timestamp",
        "type": "TIMESTAMP",
        "mode": "NULLABLE",
        "description": "BigQuery ingestion timestamp"
    },
    {
        "name": "__publish_timestamp",
        "type": "TIMESTAMP",
        "mode": "NULLABLE",
        "description": "PubSub publish timestamp"
    },
    {
        "name": "__pubsub_message_id",
        "type": "STRING",
        "mode": "NULLABLE",
        "description": "ID of the message assigned by PubSub"
    }
]
