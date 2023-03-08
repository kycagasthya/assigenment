output "cb_log_bucket_name" {
  value       = module.cb_log_bucket.name
  description = "Logs bucket name for cloud build triggers"
}