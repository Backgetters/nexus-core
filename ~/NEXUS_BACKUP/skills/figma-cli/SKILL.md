---
name: figma-cli
description: Figma API integration for design automation. Read files, export assets, update designs, and manage design systems programmatically.
metadata:
  {
    "openclaw":
      {
        "emoji": "🎨",
        "requires": { "env": ["FIGMA_ACCESS_TOKEN"] },
        "primaryEnv": "FIGMA_ACCESS_TOKEN",
      },
  }
---

# Figma CLI

Automate Figma designs and assets via the Figma API.

## Quick Start

```bash
{baseDir}/scripts/export-assets.sh --file <file-key> --format svg
```

## Environment Variables

- `FIGMA_ACCESS_TOKEN` - Your Figma personal access token

## Usage Examples

```bash
# Export assets from file
{baseDir}/scripts/export-assets.sh --file abc123 --format png --scale 2

# Get file components
{baseDir}/scripts/get-components.sh --file abc123

# Export specific node
{baseDir}/scripts/export-node.sh --file abc123 --node-id 123:456 --format svg

# List projects
{baseDir}/scripts/list-projects.sh

# Get file comments
{baseDir}/scripts/get-comments.sh --file abc123
```

## Supported Formats

- SVG (vector)
- PNG (raster)
- PDF (document)
- JPG (compressed)

## Setup

1. Get Figma access token: https://www.figma.com/developers/api#access-tokens
2. Set `FIGMA_ACCESS_TOKEN` environment variable
