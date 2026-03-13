---
name: playwright-cli
description: Advanced browser automation using Playwright. Open pages, interact with elements, take screenshots, and automate complex web workflows.
metadata:
  {
    "openclaw":
      {
        "emoji": "🎭",
        "requires": { "bins": ["npx"], "env": [] },
      },
  }
---

# Playwright CLI

Enterprise-grade browser automation using Microsoft's Playwright framework.

## Quick Start

```bash
{baseDir}/scripts/automate.sh --url https://example.com --action screenshot
```

## Installation

Playwright installs browsers automatically on first run.

## Usage Examples

```bash
# Take screenshot
{baseDir}/scripts/automate.sh --url https://example.com --action screenshot --output screenshot.png

# Extract text
{baseDir}/scripts/automate.sh --url https://example.com --action extract-text

# Fill form
{baseDir}/scripts/automate.sh --url https://example.com/form --action fill-form --data '{"name":"John","email":"john@example.com"}'

# Click element
{baseDir}/scripts/automate.sh --url https://example.com --action click --selector "button.submit"

# Wait for element
{baseDir}/scripts/automate.sh --url https://example.com --action wait --selector ".loaded" --timeout 5000
```

## Supported Actions

- `screenshot` - Capture page screenshot
- `extract-text` - Extract all text content
- `fill-form` - Fill form fields
- `click` - Click on element
- `wait` - Wait for element
- `scroll` - Scroll page
- `evaluate` - Run JavaScript

## Supported Browsers

- Chromium (default)
- Firefox
- WebKit

## Advanced Features

- Auto-wait for elements
- Network interception
- Mobile emulation
- Geolocation
- Authentication state persistence
