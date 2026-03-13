---
name: salesforce-cli
description: Salesforce CRM automation. Manage leads, contacts, opportunities, accounts, and automate sales workflows.
metadata:
  {
    "openclaw":
      {
        "emoji": "☁️",
        "requires": { "env": ["SALESFORCE_USERNAME", "SALESFORCE_PASSWORD", "SALESFORCE_SECURITY_TOKEN"] },
        "primaryEnv": "SALESFORCE_USERNAME",
      },
  }
---

# Salesforce CLI

Enterprise CRM automation for sales teams.

## Quick Start

```bash
{baseDir}/scripts/query.sh --query "SELECT Id, Name FROM Account LIMIT 10"
```

## Environment Variables

- `SALESFORCE_USERNAME` - Your Salesforce username
- `SALESFORCE_PASSWORD` - Your Salesforce password
- `SALESFORCE_SECURITY_TOKEN` - Your security token
- `SALESFORCE_LOGIN_URL` - Login URL (default: login.salesforce.com)

## Usage Examples

```bash
# Query records
{baseDir}/scripts/query.sh --query "SELECT Id, Name, Email FROM Contact LIMIT 50"

# Create lead
{baseDir}/scripts/create-lead.sh --first-name "John" --last-name "Doe" --email "john@example.com" --company "Acme Inc"

# Get opportunity
{baseDir}/scripts/get-opportunity.sh --id <opportunity-id>

# Update account
{baseDir}/scripts/update-account.sh --id <account-id> --field "Phone" --value "+1-555-0123"

# List recent leads
{baseDir}/scripts/list-leads.sh --limit 20
```

## Supported Objects

- Leads
- Contacts
- Accounts
- Opportunities
- Cases
- Tasks
- Events
- Custom objects

## Setup

1. Get security token: Salesforce → Settings → Reset Security Token
2. Set environment variables
3. Test connection
