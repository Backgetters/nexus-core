#!/usr/bin/env python3
"""
CDP Server Wallet Creator
Creates and configures a managed wallet for automated trading
"""

import os
import sys
import json
import asyncio
import ssl
import certifi
from pathlib import Path
from datetime import datetime

# Fix SSL certificates on macOS
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

TRADING_DIR = Path.home() / 'clawd' / 'trading'
DATA_DIR = TRADING_DIR / 'data'
DATA_DIR.mkdir(parents=True, exist_ok=True)

def load_env():
    """Load environment from .env.nexus"""
    env_file = TRADING_DIR / '.env.nexus'
    if env_file.exists():
        import subprocess
        result = subprocess.run(
            ['bash', '-c', f'source "{env_file}" && env'],
            capture_output=True, text=True
        )
        for line in result.stdout.strip().split('\n'):
            if '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

load_env()

async def create_wallet():
    """Create CDP Server Wallet"""
    from cdp import CdpClient
    
    print("=" * 60)
    print("NEXUS CDP WALLET CREATOR")
    print("=" * 60)
    print()
    
    # Check credentials
    key_id = os.getenv('CDP_API_KEY_ID') or os.getenv('CDP_KEY_ID')
    key_secret = os.getenv('CDP_API_KEY_SECRET') or os.getenv('CDP_KEY_SECRET')
    
    if not key_id or not key_secret:
        print("❌ ERROR: CDP_API_KEY_ID and CDP_API_KEY_SECRET required")
        print("Set them in ~/clawd/trading/.env.nexus")
        return
    
    print(f"✓ API Key ID: {key_id[:50]}...")
    print(f"✓ API Key Secret: {len(key_secret)} chars")
    print()
    
    try:
        print("🔄 Connecting to CDP...")
        cdp = CdpClient()
        print("✓ Connected to CDP")
        print()
        
        # Create wallet
        wallet_name = "NexusTrading"
        print(f"🔄 Creating wallet: {wallet_name}...")
        
        account = await cdp.evm.get_or_create_account(name=wallet_name)
        
        wallet_data = {
            'name': wallet_name,
            'address': account.address,
            'network': 'base',
            'created_at': datetime.now().isoformat(),
            'status': 'active'
        }
        
        # Save wallet info
        wallet_file = DATA_DIR / 'cdp_wallet.json'
        with open(wallet_file, 'w') as f:
            json.dump(wallet_data, f, indent=2)
        
        print()
        print("=" * 60)
        print("✅ WALLET CREATED SUCCESSFULLY")
        print("=" * 60)
        print()
        print(f"Wallet Name: {wallet_name}")
        print(f"Address: {account.address}")
        print(f"Network: Base (Ethereum L2)")
        print()
        print("📋 NEXT STEPS:")
        print("1. Fund this wallet with USDC on Base network")
        print(f"2. Send USDC to: {account.address}")
        print("3. Minimum: $100 for trading")
        print()
        print(f"💾 Wallet saved to: {wallet_file}")
        print()
        
        # Get balance
        try:
            balance = await account.get_balance()
            print(f"💰 Current Balance: {balance} ETH (Base)")
        except:
            print("💰 Balance: Unable to fetch (wallet may need funding)")
        
        print()
        print("The bot can now use this wallet for automated trading!")
        print("=" * 60)
        
    except Exception as e:
        print()
        print("❌ ERROR CREATING WALLET")
        print(f"Error: {e}")
        print()
        print("Troubleshooting:")
        print("- Check API key permissions in CDP portal")
        print("- Ensure key has 'Wallet' permissions")
        print("- Verify network connectivity")
        print()
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    try:
        asyncio.run(create_wallet())
    except KeyboardInterrupt:
        print("\nCancelled by user")
    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback
        traceback.print_exc()
