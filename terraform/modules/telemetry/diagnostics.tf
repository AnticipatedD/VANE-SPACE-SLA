resource "azurerm_monitor_diagnostic_setting" "blob_service" {
  name                       = "${var.name_prefix}-blob-diagnostics"
  target_resource_id         = "${azurerm_storage_account.telemetry.id}/blobServices/default"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.telemetry.id

  enabled_log {
    category = "StorageRead"
  }

  enabled_log {
    category = "StorageWrite"
  }

  enabled_log {
    category = "StorageDelete"
  }

  metric {
    category = "Transaction"
    enabled  = true
  }
}
