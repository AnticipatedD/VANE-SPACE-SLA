resource "azurerm_user_assigned_identity" "storage_cmk" {
  name                = "${var.name_prefix}-storage-cmk"
  location            = azurerm_resource_group.telemetry.location
  resource_group_name = azurerm_resource_group.telemetry.name
  tags                = var.tags
}

resource "azurerm_role_assignment" "storage_key_access" {
  scope                = var.key_vault_id
  role_definition_name = "Key Vault Crypto Service Encryption User"
  principal_id         = azurerm_user_assigned_identity.storage_cmk.principal_id
  principal_type       = "ServicePrincipal"
}

resource "azurerm_storage_account_customer_managed_key" "telemetry" {
  storage_account_id        = azurerm_storage_account.telemetry.id
  key_vault_key_id          = var.key_vault_key_id
  user_assigned_identity_id = azurerm_user_assigned_identity.storage_cmk.id

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

resource "azurerm_network_security_group" "private_endpoints" {
  name                = "${var.name_prefix}-private-endpoints-nsg"
  location            = azurerm_resource_group.telemetry.location
  resource_group_name = azurerm_resource_group.telemetry.name
  tags                = var.tags
}

resource "azurerm_subnet_network_security_group_association" "private_endpoints" {
  subnet_id                 = azurerm_subnet.private_endpoints.id
  network_security_group_id = azurerm_network_security_group.private_endpoints.id
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
  registration_enabled  = false
  tags                  = var.tags
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
