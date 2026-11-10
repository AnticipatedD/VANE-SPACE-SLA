output "resource_group_name" {
  description = "Production resource group."
  value       = module.telemetry_prod.resource_group_name
}

output "storage_account_name" {
  description = "Telemetry archive storage account."
  value       = module.telemetry_prod.storage_account_name
}

output "telemetry_container_name" {
  description = "Private telemetry archive container."
  value       = module.telemetry_prod.telemetry_container_name
}

output "log_analytics_workspace_id" {
  description = "Log Analytics workspace resource ID."
  value       = module.telemetry_prod.log_analytics_workspace_id
}

output "application_insights_name" {
  description = "Application Insights resource name."
  value       = module.telemetry_prod.application_insights_name
}

output "application_insights_connection_string" {
  description = "Sensitive Application Insights connection string."
  value       = module.telemetry_prod.application_insights_connection_string
  sensitive   = true
}
