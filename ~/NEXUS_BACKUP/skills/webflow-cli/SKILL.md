---
name: webflow-cli
description: Webflow CMS and site management. Update content, manage collections, deploy sites, and automate web workflows.
metadata:
  {
    "openclaw":
      {
        "emoji": "🌐",
        "requires": { "env": ["WEBFLOW_API_TOKEN"] },
        "primaryEnv": "WEBFLOW_API_TOKEN",
      },
  }
---

# Webflow CLI

Manage Webflow sites and CMS content programmatically.

## Quick Start

```bash
{baseDir}/scripts/list-sites.sh
```

## Environment Variables

- `WEBFLOW_API_TOKEN` - Your Webflow API token

## Usage Examples

```bash
# List sites
{baseDir}/scripts/list-sites.sh

# Get site info
{baseDir}/scripts/get-site.sh --site-id <site-id>

# List collections
{baseDir}/scripts/list-collections.sh --site-id <site-id>

# Create CMS item
{baseDir}/scripts/create-item.sh --collection <id> --data '{"name":"New Item"}'

# Update item
{baseDir}/scripts/update-item.sh --collection <id> --item <id> --data '{"name":"Updated"}'

# Publish site
{baseDir}/scripts/publish.sh --site-id <site-id>
```

## Supported Operations

- Sites (list, get info)
- Collections (CMS databases)
- Items (CMS content)
- Pages (static pages)
- Publishing (deploy sites)
- E-commerce (products, orders)

## Setup

1. Get API token: Webflow Dashboard → Project Settings → Integrations
2. Set `WEBFLOW_API_TOKEN` environment variable
