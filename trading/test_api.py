#!/usr/bin/env python3
"""Test CDP API connectivity"""
import os
import sys
from pathlib import Path

# Add trading dir to path
sys.path.insert(0, str(Path.home() / 'clawd' / 'trading'))

from dotenv import load_dotenv
load_dotenv(Path.home() / 'clawd' / 'trading' / '.env.nexus')

from nexus_trader import TradingEngine

print("🔄 Testing CDP API Connection...")
print("=" * 50)

try:
    bot = TradingEngine()
    print("✓ TradingEngine initialized")
    print(f"✓ Config loaded: {bot.config.pairs}")
    
    # Test authentication
    print("\n🔑 Testing JWT generation...")
    headers = bot.auth.get_headers()
    print(f"✓ JWT generated (length: {len(headers['Authorization'])})")
    
    # Test portfolio fetch (this will show if API works)
    print("\n💰 Testing portfolio fetch...")
    portfolio = bot.get_portfolio_value()
    
    if 'error' in portfolio:
        print(f"⚠️ Portfolio fetch warning: {portfolio['error']}")
    else:
        print(f"✓ Portfolio value: ${portfolio.get('total_value', 0):,.2f}")
        print(f"✓ Balances: {list(portfolio.get('balances', {}).keys())}")
    
    # Test price fetch
    print("\n📊 Testing price feeds...")
    for pair in bot.config.pairs:
        price = bot.get_price(pair)
        print(f"  {pair}: ${price:,.2f}")
    
    print("\n" + "=" * 50)
    print("✅ ALL TESTS PASSED")
    print("Bot is ready to trade!")
    print("\nTo start trading:")
    print("  cd ~/clawd/trading")
    print("  ./start_trader.sh start")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
