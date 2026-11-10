# Azure deployment

VANE-SPACE-SLA keeps its Python/Rust/JavaScript application core separate from its optional Azure infrastructure. CI validates the Terraform configuration and runs mocked tests; it does not deploy cloud resources.

## What Terraform provisions

- A dedicated Azure resource group.
- A Standard Azure Storage account with HTTPS-only transport, TLS 1.2 minimum, infrastructure encryption, geo-redundant replication by default, blob versioning, soft-delete retention, no anonymous container access, shared-key access disabled, and public network access disabled.
- A private blob container and a Blob private endpoint with a private DNS zone and VNet link.
- A dedicated VNet/subnet and NSG for the Blob private endpoint.
- A user-assigned managed identity and RBAC assignment connecting the Storage account to a customer-managed Key Vault key.
- Queue read/write/delete analytics logging and Blob read/write/delete diagnostic logs routed to Log Analytics.
- A Log Analytics workspace and workspace-based Application Insights.

## Bring-your-own Key Vault prerequisite

The module intentionally does not create or expose a Key Vault. Supply an existing private Azure Key Vault and a **versionless** key URL through key_vault_id and key_vault_key_id. The vault must:

- Have RBAC authorization enabled and a private endpoint.
- Use the Premium SKU and an HSM-backed RSA key.
- Have purge protection and soft delete enabled.
- Have a key expiry date configured.
- Be reachable from the deployment runner during Terraform apply.

The Terraform module grants its user-assigned identity the Key Vault Crypto Service Encryption User role and attaches the supplied key to the Storage account. Keep the vault private; do not enable public access just to make CI pass. Run apply from a self-hosted runner or administrator workstation with network connectivity to the vault's private endpoint.

## Prerequisites

- Terraform 1.7.5 or newer.
- Azure CLI authenticated to the intended subscription (az login).
- Permissions to create the listed resources, role assignments, private endpoints, virtual networks, and NSGs.
- An existing private Key Vault and HSM-backed key meeting the requirements above.
- A globally unique Storage account name containing only lowercase letters and digits (3-24 characters).

## Initialize and review a plan

From the repository root:

```bash
az login
az account set --subscription "<YOUR_SUBSCRIPTION_ID>"

terraform -chdir=terraform/environments/production init

terraform -chdir=terraform/environments/production plan \
  -var="location=<AZURE_REGION>" \
  -var="storage_account_name=<UNIQUE_STORAGE_ACCOUNT_NAME>" \
  -var="key_vault_id=<KEY_VAULT_RESOURCE_ID>" \
  -var="key_vault_key_id=<VERSIONLESS_HSM_KEY_URL>"
```

Review the plan and estimated Azure charges before applying. Geo-redundant storage, private endpoints, Key Vault, diagnostic ingestion, and Log Analytics can incur additional Azure charges. A plan is not a deployment.

## Apply only after review

```bash
terraform -chdir=terraform/environments/production apply \
  -var="location=<AZURE_REGION>" \
  -var="storage_account_name=<UNIQUE_STORAGE_ACCOUNT_NAME>" \
  -var="key_vault_id=<KEY_VAULT_RESOURCE_ID>" \
  -var="key_vault_key_id=<VERSIONLESS_HSM_KEY_URL>"
```

Terraform state may contain sensitive values. Do not commit state files, plan files, credentials, or connection strings. The production configuration currently uses local state by default; configure a secured Azure Storage remote backend with restricted RBAC, encryption, versioning, and state locking before team deployment.

## CI validation

The Terraform workflow runs formatting checks, initializes and validates the production configuration without creating infrastructure, executes mocked module tests, and scans the Terraform directory with Checkov. It does not run an authenticated Azure plan or apply and does not require cloud credentials.

## Local container workflow

The root Docker Compose configuration is a local test runner for the existing Python test suite. It does not claim to expose a production HTTP service.
