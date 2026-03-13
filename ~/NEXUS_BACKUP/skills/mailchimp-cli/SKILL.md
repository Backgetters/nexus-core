---
name: mailchimp-cli
description: Mailchimp email marketing automation. Manage lists, campaigns, audiences, and automate email workflows.
metadata:
  {
    "openclaw":
      {
        "emoji": "📧",
        "requires": { "env": ["MAILCHIMP_API_KEY", "MAILCHIMP_SERVER_PREFIX"] },
        "primaryEnv": "MAILCHIMP_API_KEY",
      },
  }
---

# Mailchimp CLI

Email marketing automation via Mailchimp.

## Quick Start

```bash
{baseDir}/scripts/list-audiences.sh
```

## Environment Variables

- `MAILCHIMP_API_KEY` - Your Mailchimp API key
- `MAILCHIMP_SERVER_PREFIX` - Server prefix (e.g., us1, us2)

## Usage Examples

```bash
# List audiences
{baseDir}/scripts/list-audiences.sh

# Add subscriber
{baseDir}/scripts/add-subscriber.sh --audience <id> --email "john@example.com" --firstname "John" --lastname "Doe"

# Create campaign
{baseDir}/scripts/create-campaign.sh --type regular --title "Newsletter" --subject "Monthly Update"

# Send campaign
{baseDir}/scripts/send-campaign.sh --id <campaign-id>

# Get reports
{baseDir}/scripts/campaign-reports.sh --id <campaign-id>
```

## Supported Operations

- Audiences (lists)
- Subscribers (contacts)
- Campaigns (emails)
- Templates
- Reports (analytics)
- Automations
- Tags and segments

## Setup

1. Get API key: Mailchimp → Account → Extras → API Keys
2. Note server prefix from API key (e.g., us1)
3. Set environment variables
