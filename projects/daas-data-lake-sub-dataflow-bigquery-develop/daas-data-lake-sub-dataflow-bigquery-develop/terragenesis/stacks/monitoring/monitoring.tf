resource "google_monitoring_dashboard" "datalake_house" {
  dashboard_json = file("../../src/schemas/datalake_house.json")
}

resource "google_monitoring_slo" "datalake_availability" {
  service      = data.terraform_remote_state.infrastructure.outputs.service_id
  display_name = "99,9% - Datalake Subscriber Availability SLO Monitoring"

  goal            = 0.999
  calendar_period = "MONTH"

  windows_based_sli {
    window_period = "300s"
    metric_mean_in_range {
      time_series = "metric.type=\"custom.googleapis.com/datalake_availability\" resource.type=\"global\""
      range {
        min = 0.8
        max = 1
      }
    }
  }
}
