#!/bin/bash
# 2Captcha Solver Script
# Usage: solve-captcha.sh --sitekey <key> --url <url> --type <type>

API_KEY="${TWOCAPTCHA_API_KEY:-YOUR_API_KEY_HERE}"
SITEKEY=""
URL=""
TYPE="recaptcha-v2"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --sitekey) SITEKEY="$2"; shift 2 ;;
    --url) URL="$2"; shift 2 ;;
    --type) TYPE="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [ -z "$SITEKEY" ] || [ -z "$URL" ]; then
  echo "Usage: solve-captcha.sh --sitekey <sitekey> --url <url> [--type <type>]"
  exit 1
fi

echo "Submitting CAPTCHA to 2Captcha..."
echo "Type: $TYPE"
echo "URL: $URL"

# Submit CAPTCHA
case $TYPE in
  recaptcha-v2)
    RESPONSE=$(curl -s "http://2captcha.com/in.php?key=$API_KEY&method=userrecaptcha&googlekey=$SITEKEY&pageurl=$URL&json=1")
    ;;
  recaptcha-v3)
    RESPONSE=$(curl -s "http://2captcha.com/in.php?key=$API_KEY&method=userrecaptcha&version=v3&googlekey=$SITEKEY&pageurl=$URL&json=1")
    ;;
  hcaptcha)
    RESPONSE=$(curl -s "http://2captcha.com/in.php?key=$API_KEY&method=hcaptcha&sitekey=$SITEKEY&pageurl=$URL&json=1")
    ;;
  *)
    echo "Unsupported CAPTCHA type: $TYPE"
    exit 1
    ;;
esac

CAPTCHA_ID=$(echo "$RESPONSE" | grep -o '"request":"[^"]*"' | cut -d'"' -f4)

if [ "$CAPTCHA_ID" = "ERROR_WRONG_USER_KEY" ]; then
  echo "Error: Invalid API key"
  exit 1
fi

if [ -z "$CAPTCHA_ID" ]; then
  echo "Error: Failed to submit CAPTCHA"
  echo "Response: $RESPONSE"
  exit 1
fi

echo "CAPTCHA submitted. ID: $CAPTCHA_ID"
echo "Waiting for solution (this may take 10-60 seconds)..."

# Poll for result
for i in {1..30}; do
  sleep 5
  RESULT=$(curl -s "http://2captcha.com/res.php?key=$API_KEY&action=get&id=$CAPTCHA_ID&json=1")
  STATUS=$(echo "$RESULT" | grep -o '"status":[0-9]*' | cut -d':' -f2)
  
  if [ "$STATUS" = "1" ]; then
    SOLUTION=$(echo "$RESULT" | grep -o '"request":"[^"]*"' | cut -d'"' -f4)
    echo "CAPTCHA solved!"
    echo "Solution: $SOLUTION"
    exit 0
  fi
  
  echo -n "."
done

echo ""
echo "Timeout waiting for solution"
exit 1
