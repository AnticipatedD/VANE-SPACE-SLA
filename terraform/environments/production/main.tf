terraform {
  required_version = ">= 1.5.0"

  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2.1"
    }
  }
}

provider "null" {}

module "telemetry_prod" {
  source = "../../modules/telemetry"

  resource_group_name = "rg-vane-space-sla-prod"
  location            = "eastus"
  name_prefix         = "vaneprod"
  storage_account_name = "vaneprodtelemetry"
  key_vault_id        = "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-placeholder/providers/Microsoft.KeyVault/vaults/placeholder"
  key_vault_key_id    = "https://placeholder.vault.azure.net/keys/telemetry/00000000000000000000000000000"
}

output "production_telemetry_status" {
  value       = module.telemetry_prod.validation_id
  description = "Production telemetry deployment verification identifier"
}
