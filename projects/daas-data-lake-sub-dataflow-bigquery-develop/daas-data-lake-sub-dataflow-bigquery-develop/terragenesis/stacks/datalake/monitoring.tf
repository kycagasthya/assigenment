resource "google_monitoring_slo" "datalake_data_freshness" {
  service      = data.terraform_remote_state.infrastructure.outputs.service_id
  display_name = "95% - ${var.client_id} - Datalake Subscriber Data Freshness"

  goal            = 0.95
  calendar_period = "MONTH"

  windows_based_sli {
    window_period = "900s"
    metric_mean_in_range {
      time_series = "metric.type=\"dataflow.googleapis.com/job/data_watermark_age\" resource.type=\"dataflow_job\" resource.labels.job_name=\"${var.client_id}-dl-ingest\""
      range {
        min = -9007199254740991
        max = 120
      }
    }
  }
}

resource "google_monitoring_slo" "datalake_system_latency" {
  service      = data.terraform_remote_state.infrastructure.outputs.service_id
  display_name = "95% - ${var.client_id} - Datalake Subscriber System Latency"

  goal            = 0.95
  calendar_period = "MONTH"

  windows_based_sli {
    window_period = "900s"
    metric_mean_in_range {
      time_series = "metric.type=\"dataflow.googleapis.com/job/system_lag\" resource.type=\"dataflow_job\" resource.labels.job_name=\"${var.client_id}-dl-ingest\""
      range {
        min = -9007199254740991
        max = 300
      }
    }
  }
}

resource "google_monitoring_alert_policy" "datalake_data_completeness_alert" {
  display_name = "P2: Data completeness value below 99.99% - ${var.client_id} - Datalake Subscriber Data Completeness"
  combiner     = "OR"
  conditions {
    display_name = "Global - Data completeness for ${var.client_id}"
    condition_threshold {
      filter          = "resource.type = \"global\" AND metric.type = \"custom.googleapis.com/data_completeness__${replace(var.client_id, "-", "_")}\""
      duration        = "0s"
      comparison      = "COMPARISON_LT"
      threshold_value = 0.9999
      aggregations {
        alignment_period   = "21600s"
        per_series_aligner = "ALIGN_MEAN"
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
  depends_on = [
    google_monitoring_metric_descriptor.datalake_data_completeness_descriptor
  ]
}

resource "google_monitoring_alert_policy" "datalake_data_freshness" {
  display_name = "P2: Burn rate on 95% - ${var.client_id} - Datalake Subscriber Data Freshness"
  combiner     = "OR"
  conditions {
    display_name = "Datalake Subscriber Data Freshness - Fast Burn Rate"
    condition_threshold {
      filter          = "select_slo_burn_rate(\"${google_monitoring_slo.datalake_data_freshness.name}\", \"1800s\")"
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

resource "google_monitoring_alert_policy" "datalake_system_latency" {
  display_name = "P2: Burn rate on 95% - ${var.client_id} - Datalake Subscriber System Latency"
  combiner     = "OR"
  conditions {
    display_name = "Datalake Subscriber System Latency - Fast Burn Rate"
    condition_threshold {
      filter          = "select_slo_burn_rate(\"${google_monitoring_slo.datalake_system_latency.name}\", \"1800s\")"
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

resource "google_monitoring_metric_descriptor" "datalake_missed_records_metric_descriptor" {
  description  = "A metric that indicates missed records number for ${var.client_id} client during the last 8 hours"
  display_name = "Missed records for ${var.client_id}"
  type         = "custom.googleapis.com/missed_records__${replace(var.client_id, "-", "_")}"
  metric_kind  = "GAUGE"
  value_type   = "INT64"
  project      = var.project
  labels {
    key         = "data_source"
    value_type  = "STRING"
    description = "Data Source name"
  }
}

resource "google_monitoring_metric_descriptor" "datalake_raw_records_metric_descriptor" {
  description  = "A metric that indicates raw records number for ${var.client_id} client during the last 8 hours"
  display_name = "Raw records for ${var.client_id}"
  type         = "custom.googleapis.com/raw_records__${replace(var.client_id, "-", "_")}"
  metric_kind  = "GAUGE"
  value_type   = "INT64"
  project      = var.project
  labels {
    key         = "data_source"
    value_type  = "STRING"
    description = "Data Source name"
  }
}

resource "google_monitoring_metric_descriptor" "datalake_data_completeness_descriptor" {
  description  = "A metric that indicates data completeness for ${var.client_id} client during the last 8 hours"
  display_name = "Data completeness for ${var.client_id}"
  type         = "custom.googleapis.com/data_completeness__${replace(var.client_id, "-", "_")}"
  metric_kind  = "GAUGE"
  value_type   = "DOUBLE"
  project      = var.project
}

resource "google_monitoring_metric_descriptor" "datalake_records_tracking_metric_descriptor" {
  description  = "A metric that show records number by type (all, missed, succeeded) for ${var.client_id} client during the last 8 hours"
  display_name = "Records tracking for ${var.client_id}"
  type         = "custom.googleapis.com/records_tracking__${replace(var.client_id, "-", "_")}"
  metric_kind  = "CUMULATIVE"
  value_type   = "INT64"
  project      = var.project
  labels {
    key         = "records_type"
    value_type  = "STRING"
    description = "Records type"
  }
}

resource "google_monitoring_slo" "datalake_data_completeness" {
  service      = data.terraform_remote_state.infrastructure.outputs.service_id
  display_name = "99.99% - ${var.client_id} - Datalake Subscriber Data Completeness"

  goal            = 0.999
  calendar_period = "MONTH"

  windows_based_sli {
    window_period = "28800s"
    metric_mean_in_range {
      time_series = "metric.type=\"custom.googleapis.com/data_completeness__${replace(var.client_id, "-", "_")}\" resource.type=\"global\""
      range {
        min = 0.9999
        max = 1
      }
    }
  }
  depends_on = [
    google_monitoring_metric_descriptor.datalake_data_completeness_descriptor
  ]
}
