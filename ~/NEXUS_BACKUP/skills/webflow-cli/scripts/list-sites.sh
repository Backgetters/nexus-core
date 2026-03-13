#!/bin/bash
# Webflow Sites List Script
# Usage: list-sites.sh

WEBFLOW_TOKEN="${WEBFLOW_API_TOKEN:-YOUR_TOKEN_HERE}"

echo "Fetching Webflow sites..."

RESPONSE=$(curl -s https://api.webflow.com/sites \
  -H "Authorization: Bearer $WEBFLOW_TOKEN" \
  -H "accept: application/json")

if echo "$RESPONSE" | grep -q '"code"'; then
  echo "Error:"
  echo "$RESPONSE" | grep -o '"message":"[^"]*"'
  exit 1
fi

echo "Sites:"
echo "$RESPONSE" | grep -o '"name":"[^"]*"' | cut -d'"' -f4
echo ""
echo "Site IDs:"
echo "$RESPONSE" | grep -o '"_id":"[^"]*"' | cut -d'"' -f4
