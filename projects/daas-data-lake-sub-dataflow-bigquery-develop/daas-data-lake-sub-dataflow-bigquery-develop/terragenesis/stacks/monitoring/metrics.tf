resource "google_logging_metric" "bq_log_errors" {
  name             = "bq_log_errors"
  filter           = "resource.type=\"bigquery_project\" resource.labels.location=\"US\" severity>=\"ERROR\""
  label_extractors = {}
  metric_descriptor {
    metric_kind  = "DELTA"
    value_type   = "INT64"
    display_name = "BigQuery errors"
  }
}

resource "google_logging_metric" "df_int_errors" {
  name             = "df_int_errors"
  filter           = "resource.type=\"dataflow_step\" severity>=\"ERROR\" labels.\"dataflow.googleapis.com/log_type\"!=\"system\" jsonPayload.message!~\"This is expected during autoscaling events\""
  label_extractors = {}
  metric_descriptor {
    metric_kind  = "DELTA"
    value_type   = "INT64"
    display_name = "Dataflow non-system errors"
  }
}

resource "google_logging_metric" "df_ext_errors" {
  name             = "df_ext_errors"
  filter           = "resource.type=\"dataflow_step\" severity>=\"ERROR\" labels.\"dataflow.googleapis.com/log_type\"=\"system\""
  label_extractors = {}
  metric_descriptor {
    metric_kind  = "DELTA"
    value_type   = "INT64"
    display_name = "Dataflow system errors"
  }
}
