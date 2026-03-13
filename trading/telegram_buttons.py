#!/usr/bin/env python3
"""
NEXUS Telegram Button Interface v2.0
Quick-action inline buttons with streamlined yes/no responses
"""

import json
from typing import Dict, List

# =============================================================================
# MAIN BUTTON LAYOUTS
# =============================================================================

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
    ],
    
    # =============================================================================
    # YES/NO CONFIRMATION BUTTONS
    # =============================================================================
    
    "confirm_trade": [
        [
            {"text": "✅ YES - Execute", "callback_data": "confirm_yes", "style": "success"},
            {"text": "❌ NO - Cancel", "callback_data": "confirm_no", "style": "danger"}
        ]
    ],
    
    "confirm_live": [
        [
            {"text": "✅ YES - Go Live", "callback_data": "live_yes", "style": "success"},
            {"text": "❌ NO - Stay Paper", "callback_data": "live_no", "style": "danger"}
        ]
    ],
    
    "confirm_flatten": [
        [
            {"text": "✅ YES - Flatten All", "callback_data": "flatten_yes", "style": "success"},
            {"text": "❌ NO - Keep Positions", "callback_data": "flatten_no", "style": "danger"}
        ]
    ],
    
    "confirm_stop": [
        [
            {"text": "✅ YES - Stop Bot", "callback_data": "stop_yes", "style": "success"},
            {"text": "❌ NO - Keep Running", "callback_data": "stop_no", "style": "danger"}
        ]
    ],
    
    "confirm_restart": [
        [
            {"text": "✅ YES - Restart", "callback_data": "restart_yes", "style": "success"},
            {"text": "❌ NO - Stay Current", "callback_data": "restart_no", "style": "danger"}
        ]
    ],
    
    "confirm_delete": [
        [
            {"text": "✅ YES - Delete", "callback_data": "delete_yes", "style": "success"},
            {"text": "❌ NO - Keep", "callback_data": "delete_no", "style": "danger"}
        ]
    ],
    
    "confirm_sync": [
        [
            {"text": "✅ YES - Sync Now", "callback_data": "sync_yes", "style": "success"},
            {"text": "❌ NO - Skip", "callback_data": "sync_no", "style": "danger"}
        ]
    ],
    
    "confirm_update": [
        [
            {"text": "✅ YES - Update", "callback_data": "update_yes", "style": "success"},
            {"text": "❌ NO - Skip", "callback_data": "update_no", "style": "danger"}
        ]
    ],
}

# =============================================================================
# QUICK RESPONSE TEMPLATES
# =============================================================================

QUICK_RESPONSES = {
    # Standard responses
    "portfolio": "📊 **Portfolio Summary**\n\nLoading current positions...",
    "balance": "💰 **Wallet Balances**\n\nChecking balances...",
    "market": "📈 **Market Overview**\n\nFetching market data...",
    "trading_status": "⚡ **Trading Bot Status**\n\nChecking bot status...",
    "system_health": "🖥️ **System Health**\n\nRunning diagnostics...",
    
    # Yes/No confirmation prompts
    "confirm_trade_prompt": "🤖 **Confirm Trade**\n\nExecute this trade?\n\nTap YES to proceed or NO to cancel.",
    "confirm_live_prompt": "⚠️ **Switch to LIVE Trading?**\n\nThis will use REAL money.\n\nTap YES to confirm or NO to stay in paper mode.",
    "confirm_flatten_prompt": "🛑 **FLATTEN ALL POSITIONS?**\n\nThis will close ALL open trades.\n\nTap YES to flatten or NO to keep positions.",
    "confirm_stop_prompt": "🔴 **STOP Trading Bot?**\n\nThis will halt all trading activity.\n\nTap YES to stop or NO to keep running.",
    "confirm_restart_prompt": "🔄 **RESTART Trading Bot?**\n\nThis will restart the bot with current settings.\n\nTap YES to restart or NO to continue.",
    "confirm_delete_prompt": "🗑️ **DELETE Confirmation**\n\nThis action cannot be undone.\n\nTap YES to delete or NO to keep.",
    "confirm_sync_prompt": "🔄 **SYNC Repositories?**\n\nThis will pull latest changes from all repos.\n\nTap YES to sync or NO to skip.",
    "confirm_update_prompt": "⬆️ **UPDATE Available**\n\nNew version ready to install.\n\nTap YES to update or NO to skip.",
    
    # Yes responses
    "yes_trade": "✅ **Trade Executed**\n\nOrder submitted successfully.",
    "yes_live": "⚠️ **LIVE MODE ACTIVATED**\n\nBot is now trading with REAL money. Monitor closely.",
    "yes_flatten": "🛑 **FLATTEN COMPLETE**\n\nAll positions closed. Account is flat.",
    "yes_stop": "🔴 **BOT STOPPED**\n\nTrading halted. No new orders will be placed.",
    "yes_restart": "🔄 **BOT RESTARTED**\n\nTrading bot restarted successfully.",
    "yes_delete": "🗑️ **DELETED**\n\nItem removed successfully.",
    "yes_sync": "✅ **SYNC COMPLETE**\n\nAll repositories updated.",
    "yes_update": "⬆️ **UPDATE INSTALLED**\n\nSystem updated to latest version.",
    
    # No responses
    "no_trade": "❌ **Trade Cancelled**\n\nNo action taken.",
    "no_live": "✅ **Paper Mode Continues**\n\nStaying in safe paper trading mode.",
    "no_flatten": "✅ **Positions Kept**\n\nAll positions remain open.",
    "no_stop": "✅ **Bot Continues**\n\nTrading bot keeps running.",
    "no_restart": "✅ **No Restart**\n\nContinuing with current session.",
    "no_delete": "✅ **Item Kept**\n\nNo changes made.",
    "no_sync": "✅ **Sync Skipped**\n\nRepositories unchanged.",
    "no_update": "✅ **Update Skipped**\n\nStaying on current version.",
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_buttons(layout_name: str) -> List[List[Dict]]:
    """Get button layout by name"""
    return BUTTON_LAYOUTS.get(layout_name, BUTTON_LAYOUTS["main_menu"])

def get_yes_no_buttons(action: str) -> List[List[Dict]]:
    """Get yes/no buttons for specific action"""
    layout_map = {
        "trade": "confirm_trade",
        "live": "confirm_live",
        "flatten": "confirm_flatten",
        "stop": "confirm_stop",
        "restart": "confirm_restart",
        "delete": "confirm_delete",
        "sync": "confirm_sync",
        "update": "confirm_update",
    }
    layout_name = layout_map.get(action, "confirm_trade")
    return BUTTON_LAYOUTS.get(layout_name, BUTTON_LAYOUTS["confirm_trade"])

def format_for_openclaw(layout_name: str) -> str:
    """Format buttons for OpenClaw message tool"""
    buttons = get_buttons(layout_name)
    return json.dumps(buttons)

# =============================================================================
# STREAMLINED RESPONSE HANDLER
# =============================================================================

def handle_callback(callback_data: str) -> Dict:
    """Handle button callback and return appropriate response"""
    
    # Yes responses
    if callback_data.endswith("_yes"):
        action = callback_data.replace("_yes", "")
        response_key = f"yes_{action}"
        return {
            "message": QUICK_RESPONSES.get(response_key, "✅ Confirmed"),
            "buttons": BUTTON_LAYOUTS["main_menu"]
        }
    
    # No responses
    elif callback_data.endswith("_no"):
        action = callback_data.replace("_no", "")
        response_key = f"no_{action}"
        return {
            "message": QUICK_RESPONSES.get(response_key, "❌ Cancelled"),
            "buttons": BUTTON_LAYOUTS["main_menu"]
        }
    
    # Standard menu navigation
    elif callback_data in BUTTON_LAYOUTS:
        return {
            "message": f"📍 **{callback_data.replace('_', ' ').title()}**",
            "buttons": BUTTON_LAYOUTS[callback_data]
        }
    
    # Default
    return {
        "message": "❓ Unknown action",
        "buttons": BUTTON_LAYOUTS["main_menu"]
    }

if __name__ == "__main__":
    print("Available button layouts:")
    for name in BUTTON_LAYOUTS.keys():
        print(f"  - {name}")
    
    print("\nYes/No layouts available for:")
    yes_no_actions = ["trade", "live", "flatten", "stop", "restart", "delete", "sync", "update"]
    for action in yes_no_actions:
        print(f"  - {action}")
