# Azure deployment

VANE-SPACE-SLA keeps its Python/Rust/JavaScript application core separate from its optional Azure infrastructure. The Terraform configuration in this repository provisions a reference telemetry platform; it does not automatically deploy the application or create billable resources during CI.

## What Terraform provisions

- A dedicated Azure resource group.
- A Standard Azure Storage account for telemetry archives, with HTTPS-only transport, TLS 1.2 minimum, infrastructure encryption, blob versioning, soft-delete retention, no anonymous container access, shared-key access disabled, and a deny-by-default storage firewall with the Azure trusted-services bypass.
- A private blob container for telemetry archives.
- A Log Analytics workspace.
- Workspace-based Application Insights for application telemetry.

The module exposes resource names and IDs as outputs. The Application Insights connection string is marked sensitive.

## Prerequisites

- Terraform 1.7.5 or newer.
- Azure CLI authenticated to the intended subscription (`az login`).
- An Azure subscription with permission to create the listed resources.
- A globally unique Storage account name containing only lowercase letters and digits (3-24 characters).

No AWS resources are required.

## Initialize and review a plan

From the repository root:

```bash
az login
az account set --subscription "<YOUR_SUBSCRIPTION_ID>"

terraform -chdir=terraform/environments/production init

terraform -chdir=terraform/environments/production plan \
  -var="location=<AZURE_REGION>" \
  -var="storage_account_name=<UNIQUE_STORAGE_ACCOUNT_NAME>"
```

Review the plan and estimated Azure charges before applying. A plan is not a deployment.

## Apply only after review

```bash
terraform -chdir=terraform/environments/production apply \
  -var="location=<AZURE_REGION>" \
  -var="storage_account_name=<UNIQUE_STORAGE_ACCOUNT_NAME>"
```

Terraform state contains infrastructure metadata and may contain sensitive values. Do not commit state files, plan files, credentials, or connection strings. The production configuration currently uses local state by default; configure a secured Azure Storage remote backend with restricted RBAC, encryption, versioning, and state locking before a team-managed production deployment. Backend provisioning is intentionally kept separate to avoid a bootstrap dependency.

## CI validation

The Terraform workflow runs formatting checks, initializes and validates the production configuration without creating infrastructure, executes mocked module tests, and scans the Terraform directory with Checkov. It does not run an authenticated Azure plan or apply and does not require cloud credentials.

## Local container workflow

The root Docker Compose configuration is a local test runner for the existing Python test suite. It does not claim to expose a production HTTP service.