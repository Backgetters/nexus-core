#!/bin/bash
# Stripe Charge Creation Script
# Usage: create-charge.sh --amount <amount> --currency <currency> [--customer <id> | --source <token>]

STRIPE_KEY="${STRIPE_SECRET_KEY:-YOUR_KEY_HERE}"
AMOUNT=""
CURRENCY="usd"
CUSTOMER=""
SOURCE=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --amount) AMOUNT="$2"; shift 2 ;;
    --currency) CURRENCY="$2"; shift 2 ;;
    --customer) CUSTOMER="$2"; shift 2 ;;
    --source) SOURCE="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [ -z "$AMOUNT" ]; then
  echo "Usage: create-charge.sh --amount <amount> --currency <currency> [--customer <id> | --source <token>]"
  echo "Amount is in cents (e.g., 1000 = $10.00)"
  exit 1
fi

echo "Creating Stripe charge..."
echo "Amount: $AMOUNT $CURRENCY"

if [ -n "$CUSTOMER" ]; then
  RESPONSE=$(curl -s https://api.stripe.com/v1/charges \
    -u "$STRIPE_KEY:" \
    -d amount="$AMOUNT" \
    -d currency="$CURRENCY" \
    -d customer="$CUSTOMER")
elif [ -n "$SOURCE" ]; then
  RESPONSE=$(curl -s https://api.stripe.com/v1/charges \
    -u "$STRIPE_KEY:" \
    -d amount="$AMOUNT" \
    -d currency="$CURRENCY" \
    -d source="$SOURCE")
else
  echo "Error: Either --customer or --source required"
  exit 1
fi

if echo "$RESPONSE" | grep -q '"error"'; then
  echo "Error:"
  echo "$RESPONSE" | grep -o '"message": "[^"]*"'
  exit 1
fi

CHARGE_ID=$(echo "$RESPONSE" | grep -o '"id": "ch_[^"]*"' | head -1 | cut -d'"' -f4)
STATUS=$(echo "$RESPONSE" | grep -o '"status": "[^"]*"' | head -1 | cut -d'"' -f4)

echo "Charge created successfully!"
echo "ID: $CHARGE_ID"
echo "Status: $STATUS"
