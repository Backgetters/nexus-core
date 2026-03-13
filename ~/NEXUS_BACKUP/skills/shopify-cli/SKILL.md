---
name: shopify-cli
description: Shopify store management. Manage products, orders, customers, inventory, and automate e-commerce operations.
metadata:
  {
    "openclaw":
      {
        "emoji": "🛒",
        "requires": { "env": ["SHOPIFY_ACCESS_TOKEN", "SHOPIFY_SHOP_DOMAIN"] },
        "primaryEnv": "SHOPIFY_ACCESS_TOKEN",
      },
  }
---

# Shopify CLI

E-commerce automation for Shopify stores.

## Quick Start

```bash
{baseDir}/scripts/list-products.sh --limit 10
```

## Environment Variables

- `SHOPIFY_ACCESS_TOKEN` - Your Shopify admin API access token
- `SHOPIFY_SHOP_DOMAIN` - Your shop domain (e.g., mystore.myshopify.com)

## Usage Examples

```bash
# List products
{baseDir}/scripts/list-products.sh --limit 50

# Create product
{baseDir}/scripts/create-product.sh --title "New Product" --price 29.99

# Get orders
{baseDir}/scripts/list-orders.sh --status open

# Update inventory
{baseDir}/scripts/update-inventory.sh --variant <id> --quantity 100

# Get customer
{baseDir}/scripts/get-customer.sh --id <customer-id>

# Create discount
{baseDir}/scripts/create-discount.sh --code SAVE20 --percentage 20
```

## Supported Operations

- Products (CRUD)
- Orders (management)
- Customers (CRM)
- Inventory (stock management)
- Discounts (promotions)
- Fulfillments (shipping)

## Setup

1. Create private app: Shopify Admin → Apps → Develop apps
2. Enable Admin API access
3. Get access token
4. Set `SHOPIFY_ACCESS_TOKEN` and `SHOPIFY_SHOP_DOMAIN`
