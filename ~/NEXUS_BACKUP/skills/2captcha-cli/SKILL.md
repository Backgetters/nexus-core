---
name: 2captcha-cli
description: Solve CAPTCHAs using 2Captcha service API. Supports reCAPTCHA v2/v3, hCaptcha, FunCaptcha, and more.
metadata:
  {
    "openclaw":
      {
        "emoji": "🧩",
        "requires": { "env": ["TWOCAPTCHA_API_KEY"] },
        "primaryEnv": "TWOCAPTCHA_API_KEY",
      },
  }
---

# 2Captcha CLI

Solve CAPTCHAs automatically using the 2Captcha service.

## Quick Start

```bash
{baseDir}/scripts/solve-captcha.sh --sitekey <sitekey> --url <url> --type recaptcha-v2
```

## Environment Variables

- `TWOCAPTCHA_API_KEY` - Your 2Captcha API key (get from 2captcha.com)

## Supported CAPTCHA Types

- `recaptcha-v2` - Google reCAPTCHA v2
- `recaptcha-v3` - Google reCAPTCHA v3
- `hcaptcha` - hCaptcha
- `funcaptcha` - FunCaptcha
- `geetest` - GeeTest CAPTCHA

## Usage Examples

```bash
# Solve reCAPTCHA v2
{baseDir}/scripts/solve-captcha.sh --sitekey 6Le... --url https://example.com --type recaptcha-v2

# Solve hCaptcha
{baseDir}/scripts/solve-captcha.sh --sitekey 123... --url https://example.com --type hcaptcha

# Get balance
{baseDir}/scripts/balance.sh
```

## Pricing

- reCAPTCHA v2: $2.99 per 1000 solves
- reCAPTCHA v3: $2.99 per 1000 solves
- hCaptcha: $2.99 per 1000 solves

## Setup

1. Create account at https://2captcha.com
2. Add funds ($10 minimum recommended)
3. Get API key from dashboard
4. Set `TWOCAPTCHA_API_KEY` environment variable
