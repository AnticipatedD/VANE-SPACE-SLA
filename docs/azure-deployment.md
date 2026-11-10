# Azure deployment

VANE-SPACE-SLA keeps its Python/Rust/JavaScript application core separate from its optional Azure infrastructure. The Terraform configuration provisions a reference telemetry platform; CI does not deploy cloud resources.

## What Terraform provisions

- A dedicated Azure resource group.
- A Standard Azure Storage account with HTTPS-only transport, TLS 1.2 minimum, infrastructure encryption, geo-redundant replication by default, blob versioning, soft-delete retention, no anonymous container access, shared-key access disabled, and public network access disabled.
- A private blob container and a Blob private endpoint with private DNS and a VNet link.
- A dedicated VNet/subnet for the private endpoint.
- A user-assigned managed identity and Key Vault customer-managed encryption key for the storage account.
- Queue read/write/delete analytics logging and Blob read/write/delete diagnostic logs routed to Log Analytics.
- A Log Analytics workspace and workspace-based Application Insights.

The Application Insights connection string is marked sensitive.

## Prerequisites

- Terraform 1.7.5 or newer.
- Azure CLI authenticated to the intended subscription (az login).
- Permissions to create the listed resources, Key Vault keys, role assignments, private endpoints, and virtual networks.
- A globally unique Storage account name containing only lowercase letters and digits (3-24 characters).

For Terraform apply, the deployment runner's public IPv4 address must be allowed through the Key Vault firewall using key_vault_ip_rules. The Key Vault firewall otherwise denies data-plane access. Allow only the trusted deployment egress IP; never use 0.0.0.0/0.

## Initialize and review a plan

From the repository root:

```bash
az login
az account set --subscription "<YOUR_SUBSCRIPTION_ID>"

terraform -chdir=terraform/environments/production init

terraform -chdir=terraform/environments/production plan \
  -var="location=<AZURE_REGION>" \
  -var="storage_account_name=<UNIQUE_STORAGE_ACCOUNT_NAME>" \
  -var='key_vault_ip_rules=["<DEPLOYMENT_EGRESS_IP>/32"]'
```

Review the plan and estimated Azure charges before applying. Geo-redundant storage, Key Vault, a VNet, private DNS, a private endpoint, diagnostic ingestion, and Log Analytics can incur additional Azure charges. A plan is not a deployment.

## Apply only after review

```bash
terraform -chdir=terraform/environments/production apply \
  -var="location=<AZURE_REGION>" \
  -var="storage_account_name=<UNIQUE_STORAGE_ACCOUNT_NAME>" \
  -var='key_vault_ip_rules=["<DEPLOYMENT_EGRESS_IP>/32"]'
```

Terraform state may contain sensitive values. Do not commit state files, plan files, credentials, or connection strings. The production configuration currently uses local state by default; configure a secured Azure Storage remote backend with restricted RBAC, encryption, versioning, and state locking before team deployment.

## CI validation

The Terraform workflow runs formatting checks, initializes and validates the production configuration without creating infrastructure, executes mocked module tests, and scans the Terraform directory with Checkov. It does not run an authenticated Azure plan or apply and does not require cloud credentials.

## Local container workflow

The root Docker Compose configuration is a local test runner for the existing Python test suite. It does not claim to expose a production HTTP service.
