---
name: n8n-cli
description: Workflow automation with n8n. Create, manage, and execute automated workflows connecting 400+ apps and services.
metadata:
  {
    "openclaw":
      {
        "emoji": "⚡",
        "requires": { "bins": ["npx"], "env": ["N8N_API_KEY"] },
        "primaryEnv": "N8N_API_KEY",
      },
  }
---

# n8n CLI

Workflow automation platform with 400+ integrations.

## Quick Start

```bash
{baseDir}/scripts/trigger-workflow.sh --id <workflow-id>
```

## Environment Variables

- `N8N_API_KEY` - Your n8n API key
- `N8N_BASE_URL` - Your n8n instance URL (default: http://localhost:5678)

## Usage Examples

```bash
# Trigger workflow
{baseDir}/scripts/trigger-workflow.sh --id workflow-123 --data '{"key":"value"}'

# List workflows
{baseDir}/scripts/list-workflows.sh

# Get workflow status
{baseDir}/scripts/workflow-status.sh --id workflow-123

# Create webhook trigger
{baseDir}/scripts/create-webhook.sh --workflow workflow-123 --path my-webhook
```

## Popular Integrations

- Google Sheets, Gmail, Google Calendar
- Slack, Discord, Microsoft Teams
- Shopify, WooCommerce, Stripe
- Airtable, Notion, Coda
- Twitter/X, LinkedIn, Instagram
- 400+ more

## Use Cases

- Email automation
- Social media posting
- E-commerce order processing
- CRM updates
- Data synchronization
- Lead nurturing

## Setup

1. Install n8n: `npm install -g n8n`
2. Start n8n: `n8n start`
3. Create API key in n8n settings
4. Set `N8N_API_KEY` environment variable
