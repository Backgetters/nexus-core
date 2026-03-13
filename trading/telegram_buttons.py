#!/usr/bin/env python3
"""
NEXUS Telegram Button Interface
Quick-action inline buttons for common commands
"""

import json
import os
from typing import Dict, List

# Button configurations
BUTTON_LAYOUTS = {
    "main_menu": [
        [
            {"text": "📊 Portfolio", "callback_data": "portfolio"},
            {"text": "💰 Balance", "callback_data": "balance"}
        ],
        [
            {"text": "📈 Market", "callback_data": "market"},
            {"text": "🔔 Alerts", "callback_data": "alerts"}
        ],
        [
            {"text": "⚡ Trading", "callback_data": "trading_menu"},
            {"text": "⚙️ Settings", "callback_data": "settings"}
        ]
    ],
    
    "trading_menu": [
        [
            {"text": "🟢 Start Bot", "callback_data": "trading_start"},
            {"text": "🔴 Stop Bot", "callback_data": "trading_stop"}
        ],
        [
            {"text": "📋 Status", "callback_data": "trading_status"},
            {"text": "📜 History", "callback_data": "trading_history"}
        ],
        [
            {"text": "💵 Paper Trade", "callback_data": "trading_paper"},
            {"text": "💎 Live Trade", "callback_data": "trading_live"}
        ],
        [
            {"text": "⬅️ Back", "callback_data": "main_menu"}
        ]
    ],
    
    "market_actions": [
        [
            {"text": "BTC", "callback_data": "price_BTC"},
            {"text": "ETH", "callback_data": "price_ETH"},
            {"text": "SOL", "callback_data": "price_SOL"}
        ],
        [
            {"text": "Scan Market", "callback_data": "market_scan"},
            {"text": "Top Movers", "callback_data": "market_movers"}
        ],
        [
            {"text": "⬅️ Back", "callback_data": "main_menu"}
        ]
    ],
    
    "system_controls": [
        [
            {"text": "🔄 Sync Repos", "callback_data": "sync_repos"},
            {"text": "📊 System Health", "callback_data": "system_health"}
        ],
        [
            {"text": "📝 Daily Report", "callback_data": "daily_report"},
            {"text": "🔍 Scan Git", "callback_data": "scan_git"}
        ],
        [
            {"text": "⬅️ Back", "callback_data": "main_menu"}
        ]
    ],
    
    "emergency": [
        [
            {"text": "🛑 FLATTEN ALL", "callback_data": "emergency_flatten", "style": "danger"}
        ],
        [
            {"text": "⚠️ Circuit Breaker", "callback_data": "emergency_breaker", "style": "danger"}
        ],
        [
            {"text": "📞 Contact Support", "callback_data": "emergency_support"}
        ],
        [
            {"text": "⬅️ Back", "callback_data": "main_menu"}
        ]
    ]
}

# Command mappings for button callbacks
CALLBACK_ACTIONS = {
    # Main menu
    "portfolio": "Show current portfolio with P&L",
    "balance": "Check wallet balances",
    "market": "Show market overview",
    "alerts": "List active alerts",
    "trading_menu": "Open trading submenu",
    "settings": "Show settings menu",
    
    # Trading
    "trading_start": "Start trading bot",
    "trading_stop": "Stop trading bot",
    "trading_status": "Show bot status",
    "trading_history": "Show trade history",
    "trading_paper": "Switch to paper trading",
    "trading_live": "Switch to live trading (confirmation required)",
    
    # Market
    "price_BTC": "Get BTC price and chart",
    "price_ETH": "Get ETH price and chart",
    "price_SOL": "Get SOL price and chart",
    "market_scan": "Scan for trading opportunities",
    "market_movers": "Show top gainers/losers",
    
    # System
    "sync_repos": "Sync all git repositories",
    "system_health": "Run system health check",
    "daily_report": "Generate daily summary",
    "scan_git": "Scan for new repositories",
    
    # Emergency
    "emergency_flatten": "Close all positions immediately",
    "emergency_breaker": "Activate circuit breaker (stop trading)",
    "emergency_support": "Show support contact info",
    
    # Navigation
    "main_menu": "Return to main menu"
}

def get_buttons(layout_name: str) -> List[List[Dict]]:
    """Get button layout by name"""
    return BUTTON_LAYOUTS.get(layout_name, BUTTON_LAYOUTS["main_menu"])

def format_for_openclaw(layout_name: str) -> str:
    """Format buttons for OpenClaw message tool"""
    buttons = get_buttons(layout_name)
    # Convert to JSON string for OpenClaw
    return json.dumps(buttons)

# Quick response templates
QUICK_RESPONSES = {
    "portfolio": "📊 **Portfolio Summary**\n\nLoading current positions...",
    "balance": "💰 **Wallet Balances**\n\nChecking balances...",
    "market": "📈 **Market Overview**\n\nFetching market data...",
    "trading_status": "⚡ **Trading Bot Status**\n\nChecking bot status...",
    "system_health": "🖥️ **System Health**\n\nRunning diagnostics...",
}

if __name__ == "__main__":
    # Print available layouts
    print("Available button layouts:")
    for name in BUTTON_LAYOUTS.keys():
        print(f"  - {name}")
    
    print("\nExample usage in OpenClaw:")
    print('  message(action="send", message="Choose action:", buttons=BUTTON_LAYOUTS["main_menu"])')
