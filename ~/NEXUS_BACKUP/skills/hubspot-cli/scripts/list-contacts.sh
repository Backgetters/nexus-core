#!/bin/bash
# HubSpot Contacts List Script
# Usage: list-contacts.sh [--limit <number>]

HUBSPOT_KEY="${HUBSPOT_API_KEY:-}"
LIMIT="${1:-10}"

if [ -z "$HUBSPOT_KEY" ]; then
  echo "Error: HUBSPOT_API_KEY not set"
  exit 1
fi

echo "Fetching HubSpot contacts (limit: $LIMIT)..."

curl -s "https://api.hubapi.com/crm/v3/objects/contacts?limit=$LIMIT" \
  -H "Authorization: Bearer $HUBSPOT_KEY" | \
  grep -o '"email":"[^"]*"' | cut -d'"' -f4
