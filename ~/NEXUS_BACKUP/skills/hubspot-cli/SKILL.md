---
name: hubspot-cli
description: HubSpot CRM and marketing automation. Manage contacts, deals, tickets, and automate marketing workflows.
metadata:
  {
    "openclaw":
      {
        "emoji": "🎯",
        "requires": { "env": ["HUBSPOT_API_KEY"] },
        "primaryEnv": "HUBSPOT_API_KEY",
      },
  }
---

# HubSpot CLI

CRM and marketing automation via HubSpot.

## Quick Start

```bash
{baseDir}/scripts/list-contacts.sh --limit 10
```

## Environment Variables

- `HUBSPOT_API_KEY` - Your HubSpot private app token

## Usage Examples

```bash
# List contacts
{baseDir}/scripts/list-contacts.sh --limit 50

# Create contact
{baseDir}/scripts/create-contact.sh --email "john@example.com" --firstname "John" --lastname "Doe"

# Get deal
{baseDir}/scripts/get-deal.sh --id <deal-id>

# Create deal
{baseDir}/scripts/create-deal.sh --name "New Deal" --amount 10000 --stage "appointmentscheduled"

# List deals
{baseDir}/scripts/list-deals.sh --limit 20

# Create ticket
{baseDir}/scripts/create-ticket.sh --subject "Support Request" --content "Help needed"
```

## Supported Objects

- Contacts
- Companies
- Deals
- Tickets
- Products
- Line items
- Quotes
- Marketing events

## Setup

1. Create private app: HubSpot → Settings → Integrations → Private Apps
2. Enable scopes (crm.objects.contacts.read, crm.objects.deals.write, etc.)
3. Copy access token
4. Set `HUBSPOT_API_KEY` environment variable
