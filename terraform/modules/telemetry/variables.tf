variable "environment" {
  description = "Deployment environment name."
  type        = string
  default     = "production"
}

variable "resource_group_name" {
  description = "Name of the Azure resource group for VANE-SPACE-SLA telemetry."
  type        = string
}

variable "location" {
  description = "Azure region in which telemetry resources are deployed."
  type        = string
}

variable "name_prefix" {
  description = "Short lowercase prefix used for resource names."
  type        = string
  validation {
    condition     = can(regex("^[a-z0-9-]{3,18}$", var.name_prefix))
    error_message = "name_prefix must be 3-18 lowercase letters, digits, or hyphens."
  }
}

variable "storage_account_name" {
  description = "Globally unique Azure Storage account name (3-24 lowercase letters and digits)."
  type        = string
  validation {
    condition     = can(regex("^[a-z0-9]{3,24}$", var.storage_account_name))
    error_message = "storage_account_name must contain 3-24 lowercase letters and digits only."
  }
}

variable "container_name" {
  description = "Private blob container used for telemetry archives."
  type        = string
  default     = "telemetry"
}

variable "storage_replication_type" {
  description = "Azure Storage replication tier; geo-redundant by default."
  type        = string
  default     = "GRS"
  validation {
    condition     = contains(["LRS", "ZRS", "GRS", "RAGRS", "GZRS", "RAGZRS"], var.storage_replication_type)
    error_message = "Choose a supported Azure Storage replication type."
  }
}

variable "blob_retention_days" {
  description = "Soft-delete retention for blobs and containers."
  type        = number
  default     = 30
  validation {
    condition     = var.blob_retention_days >= 1 && var.blob_retention_days <= 365
    error_message = "blob_retention_days must be between 1 and 365."
  }
}

variable "log_retention_days" {
  description = "Log Analytics retention period."
  type        = number
  default     = 30
  validation {
    condition     = var.log_retention_days >= 30 && var.log_retention_days <= 730
    error_message = "log_retention_days must be between 30 and 730."
  }
}

variable "key_vault_id" {
  description = "Azure Resource Manager ID of an existing private Key Vault with RBAC enabled."
  type        = string
  default     = ""
}

variable "key_vault_key_id" {
  description = "Versionless HTTPS key ID of an existing Premium HSM-backed Key Vault key with an expiry date."
  type        = string
  default     = ""
}

variable "tags" {
  description = "Tags applied to Azure resources."
  type        = map(string)
  default     = {}
}
