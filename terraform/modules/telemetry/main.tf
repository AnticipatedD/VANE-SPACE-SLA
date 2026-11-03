terraform {
  required_version = ">= 1.5.0"
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2.1"
    }
  }
}

variable "environment" {
  type        = string
  description = "Target deployment environment for zero-trust telemetry engine"
  default     = "production"
}

resource "null_resource" "telemetry_validation" {
  triggers = {
    service     = "vane-space-sla"
    environment = var.environment
    enforced_at = "secure-ingress"
  }
}
