terraform {
  required_version = ">= 1.5.0"

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

module "telemetry_prod" {
  source = "../../modules/telemetry"

  resource_group_name  = "rg-vane-space-sla-prod"
  location             = "eastus"
  name_prefix          = "vaneprod"
  storage_account_name = "vaneprodtelemetry"
}

output "production_telemetry_status" {
  value       = module.telemetry_prod.validation_id
  description = "Production telemetry deployment verification identifier"
}
