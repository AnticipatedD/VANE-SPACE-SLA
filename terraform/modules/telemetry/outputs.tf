output "resource_group_name" {
  description = "Azure resource group containing the telemetry resources."
  value       = azurerm_resource_group.telemetry.name
}

output "storage_account_name" {
  description = "Storage account used for telemetry archives."
  value       = azurerm_storage_account.telemetry.name
}

output "telemetry_container_name" {
  description = "Private blob container for telemetry archives."
  value       = azurerm_storage_container.telemetry.name
}

output "log_analytics_workspace_id" {
  description = "Log Analytics workspace resource ID."
  value       = azurerm_log_analytics_workspace.telemetry.id
}

output "application_insights_name" {
  description = "Application Insights resource name."
  value       = azurerm_application_insights.telemetry.name
}

output "application_insights_connection_string" {
  description = "Connection string for instrumented application components."
  value       = azurerm_application_insights.telemetry.connection_string
  sensitive   = true
}

output "validation_id" {
  description = "Stable validation identifier for the telemetry module."
  value       = "${azurerm_log_analytics_workspace.telemetry.name}-${var.environment}"
}
