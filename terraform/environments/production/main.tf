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
  source      = "../../modules/telemetry"
  environment = "production"
}

output "production_telemetry_status" {
  value       = module.telemetry_prod.validation_id
  description = "Production telemetry deployment verification identifier"
}
