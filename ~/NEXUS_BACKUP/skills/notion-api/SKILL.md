---
name: notion-api
description: Notion workspace automation. Manage pages, databases, create content, and organize knowledge bases programmatically.
metadata:
  {
    "openclaw":
      {
        "emoji": "📝",
        "requires": { "env": ["NOTION_API_KEY"] },
        "primaryEnv": "NOTION_API_KEY",
      },
  }
---

# Notion API

Workspace and knowledge management automation via Notion.

## Quick Start

```bash
{baseDir}/scripts/list-databases.sh
```

## Environment Variables

- `NOTION_API_KEY` - Your Notion integration token

## Usage Examples

```bash
# List databases
{baseDir}/scripts/list-databases.sh

# Query database
{baseDir}/scripts/query-database.sh --id <database-id> --filter '{"property":"Status","select":{"equals":"Done"}}'

# Create page
{baseDir}/scripts/create-page.sh --parent <parent-id> --title "New Page" --content "Page content here"

# Update page
{baseDir}/scripts/update-page.sh --id <page-id> --property "Status" --value "Complete"

# Create database entry
{baseDir}/scripts/create-entry.sh --database <database-id> --properties '{"Name":{"title":[{"text":{"content":"Task"}}]},"Status":{"select":{"name":"To Do"}}}'
```

## Supported Operations

- Pages (CRUD)
- Databases (query, create entries)
- Blocks (content)
- Users (workspace members)
- Search

## Setup

1. Create integration: notion.so/my-integrations
2. Share pages/databases with integration
3. Copy integration token
4. Set `NOTION_API_KEY` environment variable
