---
name: asana-cli
description: Asana project and task management. Create projects, manage tasks, track progress, and automate workflows.
metadata:
  {
    "openclaw":
      {
        "emoji": "✅",
        "requires": { "env": ["ASANA_ACCESS_TOKEN"] },
        "primaryEnv": "ASANA_ACCESS_TOKEN",
      },
  }
---

# Asana CLI

Project management automation via Asana.

## Quick Start

```bash
{baseDir}/scripts/list-projects.sh
```

## Environment Variables

- `ASANA_ACCESS_TOKEN` - Your Asana personal access token

## Usage Examples

```bash
# List projects
{baseDir}/scripts/list-projects.sh

# Create task
{baseDir}/scripts/create-task.sh --project <project-id> --name "New Task" --assignee <user-id>

# List tasks
{baseDir}/scripts/list-tasks.sh --project <project-id>

# Complete task
{baseDir}/scripts/complete-task.sh --id <task-id>

# Create project
{baseDir}/scripts/create-project.sh --name "New Project" --team <team-id>
```

## Supported Operations

- Projects (create, update, delete)
- Tasks (CRUD, assign, complete)
- Sections (organization)
- Tags (categorization)
- Users (team management)
- Workspaces

## Setup

1. Get access token: Asana → My Profile Settings → Apps → Manage Developer Apps
2. Create personal access token
3. Set `ASANA_ACCESS_TOKEN` environment variable
