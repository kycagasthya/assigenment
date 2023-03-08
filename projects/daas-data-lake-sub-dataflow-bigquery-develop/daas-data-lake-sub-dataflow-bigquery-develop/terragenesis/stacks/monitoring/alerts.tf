resource "time_sleep" "wait_30_seconds" {
  depends_on = [google_logging_metric.bq_log_errors]

  create_duration = "10s"
}

resource "google_monitoring_alert_policy" "bq_errors" {
  display_name = "P3: BQ Error Log Entries"
  combiner     = "OR"
  conditions {
    display_name = "BigQuery Project - Errors Count"
    condition_threshold {
      filter          = "resource.type=\"bigquery_project\" AND metric.type=\"logging.googleapis.com/user/${google_logging_metric.bq_log_errors.name}\""
      duration        = "0s"
      comparison      = "COMPARISON_GT"
      threshold_value = 0
      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_SUM"
        group_by_fields    = []
      }
      trigger {
        count = 1
      }
    }
  }
  alert_strategy {
    auto_close = "604800s"
  }
  enabled               = true
  notification_channels = [data.terraform_remote_state.infrastructure.outputs.opsgenie_channel]
  user_labels           = var.labels
  depends_on            = [time_sleep.wait_30_seconds]
}

resource "google_monitoring_alert_policy" "df_errors" {
  display_name = "P3: Dataflow Error Log Entries"
  combiner     = "OR"
  conditions {
    display_name = "Dataflow Internal - Errors Count"
    condition_threshold {
      filter          = "resource.type=\"dataflow_job\" AND metric.type=\"logging.googleapis.com/user/${google_logging_metric.df_int_errors.name}\""
      duration        = "0s"
      comparison      = "COMPARISON_GT"
      threshold_value = 0
      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_SUM"
        group_by_fields    = []
      }
      trigger {
        count = 1
      }
    }
  }
  alert_strategy {
    auto_close = "604800s"
  }
  enabled               = true
  notification_channels = [data.terraform_remote_state.infrastructure.outputs.opsgenie_channel]
  user_labels           = var.labels
  depends_on            = [time_sleep.wait_30_seconds]
}

resource "google_monitoring_alert_policy" "invalid_publish_events" {
  display_name = "P2: Invalid Publish events - # of batches"
  combiner     = "OR"
  documentation {
    content   = "If # of invalid Pub/Sub POST API calls messages increase 2, this means that publishers send invalid JSON data to the Pub/Sub topic and topic schema validation fails.\nCheck publisher DataFlow job and validate JSON data format coming to the target Pub/Sub topic."
    mime_type = "text/markdown"
  }
  conditions {
    display_name = "Cloud Pub/Sub Topic - Invalid Publish requests"
    condition_threshold {
      filter          = "metric.type=\"pubsub.googleapis.com/topic/send_request_count\" resource.type=\"pubsub_topic\" metric.label.\"response_class\"=\"invalid\""
      duration        = "0s"
      comparison      = "COMPARISON_GT"
      threshold_value = 2
      trigger {
        count = 1
      }
      aggregations {
        alignment_period     = "60s"
        per_series_aligner   = "ALIGN_SUM"
        cross_series_reducer = "REDUCE_SUM"
        group_by_fields      = ["resource.label.topic_id"]
      }
    }
  }
  alert_strategy {
    auto_close = "604800s"
  }
  enabled               = true
  notification_channels = [data.terraform_remote_state.infrastructure.outputs.opsgenie_channel]
  user_labels           = var.labels
}

resource "google_monitoring_alert_policy" "df_system_lag" {
  display_name = "P3: Dataflow processing delay"
  combiner     = "OR"
  conditions {
    display_name = "Dataflow Job - System lag"
    condition_threshold {
      filter          = "resource.type = \"dataflow_job\" AND metric.type = \"dataflow.googleapis.com/job/system_lag\""
      duration        = "0s"
      comparison      = "COMPARISON_GT"
      threshold_value = 300
      trigger {
        count = 1
      }
      aggregations {
        alignment_period   = "600s"
        per_series_aligner = "ALIGN_MEAN"
        group_by_fields    = []
      }
    }
  }
  alert_strategy {
    auto_close = "604800s"
  }
  enabled               = true
  notification_channels = [data.terraform_remote_state.infrastructure.outputs.opsgenie_channel]
  user_labels           = var.labels
}

resource "google_monitoring_alert_policy" "ingest_errors" {
  display_name = "P2: BQ Ingest Errors"
  combiner     = "OR"
  conditions {
    display_name = "BigQuery Dataset - Ingest Errors"
    condition_threshold {
      filter          = "resource.type = \"bigquery_dataset\" AND metric.type = \"bigquery.googleapis.com/storage/uploaded_row_count\" AND metric.labels.table = \"ingest_errors\""
      duration        = "0s"
      comparison      = "COMPARISON_GT"
      threshold_value = 0
      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_DELTA"
        group_by_fields    = []
      }
      trigger {
        count = 1
      }
    }
  }
  alert_strategy {
    auto_close = "604800s"
  }
  enabled               = true
  notification_channels = [data.terraform_remote_state.infrastructure.outputs.opsgenie_channel]
  user_labels           = var.labels
}

resource "google_monitoring_alert_policy" "datalake_availability" {
  display_name = "P2: Burn rate on 99,9% - Datalake Subscriber Availability"
  combiner     = "OR"
  conditions {
    display_name = "Datalake Subscriber Availability - Fast Burn Rate"
    condition_threshold {
      filter          = "select_slo_burn_rate(\"${google_monitoring_slo.datalake_availability.name}\", \"1800s\")"
      duration        = "0s"
      comparison      = "COMPARISON_GT"
      threshold_value = 20
      aggregations {
        alignment_period   = "300s"
        per_series_aligner = "ALIGN_INTERPOLATE"
        group_by_fields    = []
      }
      trigger {
        count = 1
      }
    }
  }
  alert_strategy {
    auto_close = "604800s"
  }
  enabled               = true
  notification_channels = [data.terraform_remote_state.infrastructure.outputs.opsgenie_channel]
  user_labels           = var.labels
}
