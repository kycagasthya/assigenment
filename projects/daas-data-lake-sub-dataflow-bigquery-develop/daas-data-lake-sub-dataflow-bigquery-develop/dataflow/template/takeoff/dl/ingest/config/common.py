# PubSub message field names
EVENT_TIMESTAMP_FIELD = "__event_timestamp"
CLIENT_FIELD = "__client_name"
SOURCE_FIELD = "__source_name"
SCHEMA_FIELD = "__schema_version"
INGEST_TIMESTAMP_FIELD = "__ingest_timestamp"
PUBLISH_TIMESTAMP_FIELD = "__publish_timestamp"
MANDATORY_TECHNICAL_FIELDS = [EVENT_TIMESTAMP_FIELD, CLIENT_FIELD, SOURCE_FIELD, SCHEMA_FIELD,
                              INGEST_TIMESTAMP_FIELD, PUBLISH_TIMESTAMP_FIELD]
PUBSUB_MESSAGE_ID_FIELD = "__pubsub_message_id"

# BigQuery
SERVICE_DATASET = "dl_service"
INGEST_ERRORS_TABLE = "ingest_errors"
PUBSUB_SUBSCRIPTION_FIELD = "pubsub_subscription"
ERROR_TYPE_FIELD = "error_type"
MESSAGE_FIELD = "message"

# errors
INVALID_CLIENT = "invalid_client"
INVALID_SOURCE = "invalid_source"
VALID_RECORD = "valid"
INVALID_RECORD = 'invalid_message'
INVALID_RECORD_SCHEMA = 'invalid_message_schema'
INSERT_FAILED = "insert_failed"

# default column values
UNKNOWN_STRING_VALUE = 'unknown'
EMPTY_MESSAGE_SUBSTITUTE = r'{"__received_empty_message": "__received_empty_message"}'
WRONG_MESSAGE_FORMAT_SUBSTITUTE = '__received_wrong_format_message'
