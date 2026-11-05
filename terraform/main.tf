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

module "root_telemetry" {
  source      = "./modules/telemetry"
  environment = "production"
}

output "telemetry_validation_status" {
  value       = module.telemetry.validation_id
  description = "Active deployment validation identifier from telemetry module"
}
