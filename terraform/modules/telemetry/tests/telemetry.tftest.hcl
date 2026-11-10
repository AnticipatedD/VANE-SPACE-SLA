mock_provider "azurerm" {}

run "creates_private_encrypted_telemetry_storage" {
  command = plan

  variables {
    resource_group_name  = "rg-vane-test"
    location             = "eastus"
    name_prefix          = "vane-test"
    storage_account_name = "vaneslatest001"
    key_vault_id         = "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-vane-test/providers/Microsoft.KeyVault/vaults/kv-vane-test"
    key_vault_key_id     = "https://kv-vane-test.vault.azure.net/keys/telemetry-cmk"
    tags                 = { environment = "test" }
  }

  assert {
    condition     = azurerm_storage_account.telemetry.min_tls_version == "TLS1_2"
    error_message = "Telemetry storage must require TLS 1.2 or newer."
  }

  assert {
    condition     = azurerm_storage_account.telemetry.https_traffic_only_enabled
    error_message = "Telemetry storage must reject unencrypted transport."
  }

  assert {
    condition     = azurerm_storage_account.telemetry.allow_nested_items_to_be_public == false
    error_message = "Telemetry storage must not permit public blob/container access."
  }

  assert {
    condition     = azurerm_storage_account.telemetry.public_network_access_enabled == false
    error_message = "Telemetry storage must disable public network access."
  }

  assert {
    condition     = azurerm_storage_account.telemetry.account_replication_type != "LRS"
    error_message = "Telemetry storage must use zone- or geo-redundant replication."
  }

  assert {
    condition     = azurerm_storage_account.telemetry.shared_access_key_enabled == false
    error_message = "Telemetry storage must use identity-based access rather than shared keys."
  }

  assert {
    condition     = azurerm_storage_account.telemetry.network_rules[0].default_action == "Deny"
    error_message = "Telemetry storage must deny untrusted network traffic by default."
  }

  assert {
    condition     = azurerm_storage_account.telemetry.queue_properties[0].logging[0].read && azurerm_storage_account.telemetry.queue_properties[0].logging[0].write && azurerm_storage_account.telemetry.queue_properties[0].logging[0].delete
    error_message = "Queue read, write, and delete requests must be logged."
  }

  assert {
    condition     = azurerm_storage_container.telemetry.container_access_type == "private"
    error_message = "Telemetry archive container must remain private."
  }

  assert {
    condition     = azurerm_storage_account_customer_managed_key.telemetry.key_vault_key_id == var.key_vault_key_id
    error_message = "Telemetry storage must use the supplied customer-managed key."
  }
}

run "rejects_invalid_storage_account_name" {
  command = plan

  variables {
    resource_group_name  = "rg-vane-test"
    location             = "eastus"
    name_prefix          = "vane-test"
    storage_account_name = "Vane_Invalid_Name"
    key_vault_id         = "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-vane-test/providers/Microsoft.KeyVault/vaults/kv-vane-test"
    key_vault_key_id     = "https://kv-vane-test.vault.azure.net/keys/telemetry-cmk"
  }

  expect_failures = [var.storage_account_name]
}
