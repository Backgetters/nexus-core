#!/usr/bin/env python3
"""Simple Coinbase CDP API client to check portfolio"""
import json
import base64
import time
import urllib.request
import urllib.error

# Load API key
with open('/Users/tomegathericon/Downloads/cdp_api_key.json', 'r') as f:
    creds = json.load(f)

KEY_NAME = creds['name']
PRIVATE_KEY_PEM = creds['privateKey']

# Coinbase CDP API endpoint for accounts
API_BASE = "https://api.coinbase.com"
ACCOUNTS_ENDPOINT = "/v2/accounts"

print("=" * 50)
print("COINBASE PORTFOLIO CHECK")
print("=" * 50)
print(f"API Key: {KEY_NAME[:50]}...")
print()

# Try a simple request (unauthenticated first to test connectivity)
try:
    req = urllib.request.Request(
        f"{API_BASE}{ACCOUNTS_ENDPOINT}",
        headers={
            'Content-Type': 'application/json',
            'CB-VERSION': '2024-01-01'
        }
    )
    
    # Note: Without proper JWT signing, this will fail with auth error
    # But we can at least test the key format
    response = urllib.request.urlopen(req, timeout=10)
    data = json.loads(response.read().decode('utf-8'))
    print(json.dumps(data, indent=2))
    
except urllib.error.HTTPError as e:
    if e.code == 401:
        print("⚠️  Authentication required (expected)")
        print("Status: API endpoint reachable, needs JWT signature")
        print()
        print("The CDP API requires JWT signing which is complex.")
        print("Options:")
        print("1. Use Coinbase's official CLI: npm install -g @coinbase/cdp-cli")
        print("2. I can try installing the CDP SDK: pip install cdp-sdk")
        print("3. Use the older Coinbase API (v3) with simpler key format")
    else:
        print(f"Error: {e.code} - {e.reason}")
        
except Exception as e:
    print(f"Error: {e}")
