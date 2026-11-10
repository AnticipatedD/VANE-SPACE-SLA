variable "resource_group_name" {
  description = "Azure resource group for the production telemetry stack."
  type        = string
  default     = "rg-vane-space-sla-prod"
}
variable "location" {
  description = "Azure region for production resources."
  type        = string
}
variable "name_prefix" {
  description = "Lowercase prefix for Azure resource names."
  type        = string
  default     = "vane-space-sla"
}
variable "storage_account_name" {
  description = "Globally unique 3-24 character Azure Storage account name."
  type        = string
}
variable "storage_replication_type" {
  description = "Storage replication tier."
  type        = string
  default     = "GRS"
}
variable "blob_retention_days" {
  description = "Soft-delete retention for telemetry blobs and containers."
  type        = number
  default     = 30
}
variable "log_retention_days" {
  description = "Log Analytics retention in days."
  type        = number
  default     = 30
}
variable "key_vault_ip_rules" {
  description = "Optional public IPv4 CIDRs allowed to reach the Key Vault data plane during deployment."
  type        = list(string)
  default     = []
}
variable "tags" {
  description = "Tags applied to all Azure resources."
  type        = map(string)
  default = {
    application = "VANE-SPACE-SLA"
    environment = "production"
    managed_by  = "terraform"
  }
}
