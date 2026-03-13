---
name: stripe-cli
description: Stripe payment processing integration. Create charges, manage customers, handle subscriptions, and process refunds.
metadata:
  {
    "openclaw":
      {
        "emoji": "💳",
        "requires": { "env": ["STRIPE_SECRET_KEY"] },
        "primaryEnv": "STRIPE_SECRET_KEY",
      },
  }
---

# Stripe CLI

Payment processing and financial operations via Stripe.

## Quick Start

```bash
{baseDir}/scripts/create-charge.sh --amount 1000 --currency usd --source tok_visa
```

## Environment Variables

- `STRIPE_SECRET_KEY` - Your Stripe secret key (sk_test_... or sk_live_...)

## Usage Examples

```bash
# Create charge
{baseDir}/scripts/create-charge.sh --amount 5000 --currency cad --customer cus_123

# Create customer
{baseDir}/scripts/create-customer.sh --email customer@example.com --name "John Doe"

# List charges
{baseDir}/scripts/list-charges.sh --limit 10

# Create subscription
{baseDir}/scripts/create-subscription.sh --customer cus_123 --price price_123

# Issue refund
{baseDir}/scripts/refund.sh --charge ch_123

# Get balance
{baseDir}/scripts/balance.sh
```

## Supported Operations

- Charges (one-time payments)
- Customers (CRM)
- Subscriptions (recurring billing)
- Refunds
- Invoices
- Products & Prices
- Webhooks

## Setup

1. Create Stripe account: https://stripe.com
2. Get API keys from Dashboard → Developers → API keys
3. Set `STRIPE_SECRET_KEY` environment variable
4. Use test mode for development (keys start with sk_test_)
