terraform {
  required_version = ">= 1.7.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}
resource "azurerm_resource_group" "telemetry" {
  name     = var.resource_group_name
  location = var.location
  tags     = var.tags
}
resource "azurerm_storage_account" "telemetry" {
  name                              = var.storage_account_name
  resource_group_name               = azurerm_resource_group.telemetry.name
  location                          = azurerm_resource_group.telemetry.location
  account_tier                      = "Standard"
  account_replication_type          = var.storage_replication_type
  min_tls_version                   = "TLS1_2"
  https_traffic_only_enabled        = true
  allow_nested_items_to_be_public   = false
  shared_access_key_enabled         = false
  infrastructure_encryption_enabled = true
  public_network_access_enabled     = false
  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.storage.id]
  }
  network_rules {
    default_action = "Deny"
    bypass         = ["AzureServices"]
    ip_rules       = []
  }
  blob_properties {
    versioning_enabled = true
    delete_retention_policy {
      days = var.blob_retention_days
    }
    container_delete_retention_policy {
      days = var.blob_retention_days
    }
  }
  queue_properties {
    logging {
      delete                = true
      read                  = true
      write                 = true
      version               = "1.0"
      retention_policy_days = var.blob_retention_days
    }
  }
  tags = var.tags
}
resource "azurerm_storage_container" "telemetry" {
  name                  = var.container_name
  storage_account_id    = azurerm_storage_account.telemetry.id
  container_access_type = "private"
}
resource "azurerm_log_analytics_workspace" "telemetry" {
  name                = "${var.name_prefix}-logs"
  location            = azurerm_resource_group.telemetry.location
  resource_group_name = azurerm_resource_group.telemetry.name
  sku                 = "PerGB2018"
  retention_in_days   = var.log_retention_days
  tags                = var.tags
}
resource "azurerm_monitor_diagnostic_setting" "blob" {
  name                       = "${var.name_prefix}-blob-audit"
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
}
resource "azurerm_application_insights" "telemetry" {
  name                = "${var.name_prefix}-appinsights"
  location            = azurerm_resource_group.telemetry.location
  resource_group_name = azurerm_resource_group.telemetry.name
  application_type    = "web"
  workspace_id        = azurerm_log_analytics_workspace.telemetry.id
  tags                = var.tags
}
