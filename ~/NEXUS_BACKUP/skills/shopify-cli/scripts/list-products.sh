#!/bin/bash
# Shopify Products List Script
# Usage: list-products.sh [--limit <number>]

SHOPIFY_TOKEN="${SHOPIFY_ACCESS_TOKEN:-YOUR_TOKEN}"
SHOPIFY_DOMAIN="${SHOPIFY_SHOP_DOMAIN:-your-store.myshopify.com}"
LIMIT="${1:-10}"

echo "Fetching products from $SHOPIFY_DOMAIN..."
echo "Limit: $LIMIT"

RESPONSE=$(curl -s "https://$SHOPIFY_DOMAIN/admin/api/2024-01/products.json?limit=$LIMIT" \
  -H "X-Shopify-Access-Token: $SHOPIFY_TOKEN")

if echo "$RESPONSE" | grep -q '"errors"'; then
  echo "Error:"
  echo "$RESPONSE"
  exit 1
fi

echo "Products:"
echo "$RESPONSE" | grep -o '"title":"[^"]*"' | cut -d'"' -f4
