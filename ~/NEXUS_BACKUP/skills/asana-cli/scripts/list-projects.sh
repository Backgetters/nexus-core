#!/bin/bash
# Asana Projects List Script
# Usage: list-projects.sh

ASANA_TOKEN="${ASANA_ACCESS_TOKEN:-}"

if [ -z "$ASANA_TOKEN" ]; then
  echo "Error: ASANA_ACCESS_TOKEN not set"
  exit 1
fi

echo "Fetching Asana projects..."

curl -s "https://app.asana.com/api/1.0/projects" \
  -H "Authorization: Bearer $ASANA_TOKEN" | \
  grep -o '"name":"[^"]*"' | cut -d'"' -f4
