terraform {
  required_version = ">= 1.7.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  features {}
}

module "telemetry" {
  source = "../../modules/telemetry"

  resource_group_name      = var.resource_group_name
  location                 = var.location
  name_prefix              = var.name_prefix
  storage_account_name     = var.storage_account_name
  storage_replication_type = var.storage_replication_type
  blob_retention_days      = var.blob_retention_days
  log_retention_days       = var.log_retention_days
  tags                     = var.tags
}
