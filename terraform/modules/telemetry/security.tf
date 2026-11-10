data "azurerm_client_config" "current" {}

resource "azurerm_user_assigned_identity" "storage" {
  name                = "${var.name_prefix}-storage-cmk"
  location            = azurerm_resource_group.telemetry.location
  resource_group_name = azurerm_resource_group.telemetry.name
  tags                = var.tags
}

resource "azurerm_key_vault" "telemetry" {
  name                          = substr("${var.storage_account_name}kv", 0, 24)
  location                      = azurerm_resource_group.telemetry.location
  resource_group_name           = azurerm_resource_group.telemetry.name
  tenant_id                     = data.azurerm_client_config.current.tenant_id
  sku_name                      = "standard"
  enable_rbac_authorization     = true
  purge_protection_enabled      = true
  soft_delete_retention_days    = 30
  public_network_access_enabled = true

  network_acls {
    bypass         = "AzureServices"
    default_action = "Deny"
    ip_rules       = var.key_vault_ip_rules
  }

  tags = var.tags
}

resource "azurerm_key_vault_key" "telemetry" {
  name         = "telemetry-cmk"
  key_vault_id = azurerm_key_vault.telemetry.id
  key_type     = "RSA"
  key_size     = 2048
  key_opts     = ["decrypt", "encrypt", "unwrapKey", "wrapKey"]
}

resource "azurerm_role_assignment" "storage_key_access" {
  scope                = azurerm_key_vault.telemetry.id
  role_definition_name = "Key Vault Crypto Service Encryption User"
  principal_id         = azurerm_user_assigned_identity.storage.principal_id
  principal_type       = "ServicePrincipal"
}

resource "azurerm_storage_account_customer_managed_key" "telemetry" {
  storage_account_id = azurerm_storage_account.telemetry.id
  key_vault_key_id   = azurerm_key_vault_key.telemetry.id

  user_assigned_identity_id = azurerm_user_assigned_identity.storage.id

  depends_on = [azurerm_role_assignment.storage_key_access]
}

resource "azurerm_virtual_network" "telemetry" {
  name                = "${var.name_prefix}-telemetry-vnet"
  address_space       = ["10.42.0.0/16"]
  location            = azurerm_resource_group.telemetry.location
  resource_group_name = azurerm_resource_group.telemetry.name
  tags                = var.tags
}

resource "azurerm_subnet" "private_endpoints" {
  name                 = "private-endpoints"
  resource_group_name  = azurerm_resource_group.telemetry.name
  virtual_network_name = azurerm_virtual_network.telemetry.name
  address_prefixes     = ["10.42.1.0/24"]

  private_endpoint_network_policies = "Disabled"
}

resource "azurerm_private_dns_zone" "blob" {
  name                = "privatelink.blob.core.windows.net"
  resource_group_name = azurerm_resource_group.telemetry.name
  tags                = var.tags
}

resource "azurerm_private_dns_zone_virtual_network_link" "blob" {
  name                  = "${var.name_prefix}-blob-dns-link"
  resource_group_name   = azurerm_resource_group.telemetry.name
  private_dns_zone_name = azurerm_private_dns_zone.blob.name
  virtual_network_id    = azurerm_virtual_network.telemetry.id
  registration_enabled = false
  tags                 = var.tags
}

resource "azurerm_private_endpoint" "blob" {
  name                = "${var.name_prefix}-blob-private-endpoint"
  location            = azurerm_resource_group.telemetry.location
  resource_group_name = azurerm_resource_group.telemetry.name
  subnet_id           = azurerm_subnet.private_endpoints.id
  tags                = var.tags

  private_service_connection {
    name                           = "${var.name_prefix}-blob-private-connection"
    private_connection_resource_id = azurerm_storage_account.telemetry.id
    subresource_names              = ["blob"]
    is_manual_connection           = false
  }

  private_dns_zone_group {
    name                 = "blob-dns-zone-group"
    private_dns_zone_ids = [azurerm_private_dns_zone.blob.id]
  }
}
