#!/usr/bin/env python3
"""
NEXUS Trade Executor - Manual Execution Helper
Tracks manual trades and updates bot state
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

TRADING_DIR = Path.home() / 'clawd' / 'trading'
DATA_DIR = TRADING_DIR / 'data'
DATA_DIR.mkdir(parents=True, exist_ok=True)

def load_trades():
    """Load trade history"""
    trade_file = DATA_DIR / 'manual_trades.json'
    if trade_file.exists():
        with open(trade_file) as f:
            return json.load(f)
    return {'trades': [], 'total_invested': 0, 'total_value': 0}

def save_trades(data):
    """Save trade history"""
    trade_file = DATA_DIR / 'manual_trades.json'
    with open(trade_file, 'w') as f:
        json.dump(data, f, indent=2)

def add_trade(symbol: str, amount_usd: float, price: float, side: str = 'BUY'):
    """Record a manual trade"""
    data = load_trades()
    
    trade = {
        'timestamp': datetime.now().isoformat(),
        'symbol': symbol,
        'side': side,
        'amount_usd': amount_usd,
        'price': price,
        'quantity': amount_usd / price if price > 0 else 0,
        'fees': amount_usd * 0.006  # 0.6% Coinbase fee estimate
    }
    
    data['trades'].append(trade)
    data['total_invested'] += amount_usd
    
    save_trades(data)
    
    print(f"\n✅ Trade recorded!")
    print(f"  {symbol}: {side} ${amount_usd} @ ${price:,.2f}")
    print(f"  Got: {trade['quantity']:.6f} {symbol}")
    print(f"  Fee estimate: ${trade['fees']:.2f}")
    print(f"\n💰 Total invested: ${data['total_invested']:.2f}")

def show_portfolio():
    """Show current portfolio"""
    data = load_trades()
    
    print("\n" + "=" * 60)
    print("NEXUS TRADING PORTFOLIO")
    print("=" * 60)
    
    if not data['trades']:
        print("\nNo trades yet. Execute signals when ready!")
        return
    
    # Group by symbol
    positions = {}
    for trade in data['trades']:
        sym = trade['symbol']
        if sym not in positions:
            positions[sym] = {'qty': 0, 'cost': 0}
        
        if trade['side'] == 'BUY':
            positions[sym]['qty'] += trade['quantity']
            positions[sym]['cost'] += trade['amount_usd']
    
    print(f"\n💰 Total Invested: ${data['total_invested']:.2f}")
    print(f"📊 Total Trades: {len(data['trades'])}")
    print("\n📈 Positions:")
    
    for sym, pos in positions.items():
        avg_price = pos['cost'] / pos['qty'] if pos['qty'] > 0 else 0
        print(f"  {sym}: {pos['qty']:.6f} @ avg ${avg_price:,.2f} (cost: ${pos['cost']:.2f})")
    
    print("\n📝 Recent Trades:")
    for trade in data['trades'][-5:]:
        print(f"  {trade['timestamp'][:16]} | {trade['symbol']} | {trade['side']} ${trade['amount_usd']:.2f} @ ${trade['price']:,.2f}")
    
    print("\n" + "=" * 60)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Nexus Trade Executor')
    parser.add_argument('--add', action='store_true', help='Add a trade')
    parser.add_argument('--symbol', type=str, help='Symbol (BTC, ETH)')
    parser.add_argument('--amount', type=float, help='USD amount')
    parser.add_argument('--price', type=float, help='Price per unit')
    parser.add_argument('--side', type=str, default='BUY', choices=['BUY', 'SELL'])
    parser.add_argument('--portfolio', action='store_true', help='Show portfolio')
    
    args = parser.parse_args()
    
    if args.portfolio:
        show_portfolio()
    elif args.add and args.symbol and args.amount and args.price:
        add_trade(args.symbol.upper(), args.amount, args.price, args.side)
    else:
        print("""
╔══════════════════════════════════════════════════════════════╗
║           NEXUS TRADE EXECUTOR - MANUAL MODE                  ║
╚══════════════════════════════════════════════════════════════╝

USAGE:
  # Record a trade you executed on Coinbase
  python3 trade_executor.py --add --symbol BTC --amount 50 --price 67743

  # View your portfolio
  python3 trade_executor.py --portfolio

EXAMPLE SIGNAL EXECUTION:
  Signal: BUY $50 BTC @ $67,743
  1. Go to Coinbase → Buy BTC
  2. Enter $50 → Confirm
  3. Record: python3 trade_executor.py --add --symbol BTC --amount 50 --price 67743

Your trades are tracked in: ~/clawd/trading/data/manual_trades.json
        """)

if __name__ == '__main__':
    main()
