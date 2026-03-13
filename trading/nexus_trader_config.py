"""
NEXUS Trading Configuration v5.0
Enhanced with swarm-trader risk management principles
"""

import os
from dataclasses import dataclass
from typing import List, Dict

# =============================================================================
# PORTFOLIO CONFIGURATION
# =============================================================================

@dataclass
class PortfolioConfig:
    """Portfolio allocation and risk parameters"""
    total_capital: float = 1000.0
    base_trade_usd: float = 100.0
    
    # Risk Management (from swarm-trader)
    max_risk_per_trade: float = 0.02       # Risk 2% per trade
    max_portfolio_heat: float = 0.10       # Max 10% at risk
    max_position_size: float = 0.15        # No position > 15%
    default_stop_pct: float = 0.02         # 2% stop loss
    default_target_multiplier: float = 2.0 # 2:1 reward:risk
    
    # Daily Limits
    max_daily_loss_pct: float = 3.0        # Circuit breaker at 3%
    max_daily_trades: int = 20             # Max trades per day
    min_confidence: float = 0.55           # 55% min confidence
    
    # Position Management
    max_position_pct: float = 15.0         # Legacy: max 15% in one position
    min_order_size_usd: float = 10.0       # Minimum trade size
    
    # Time-based
    flatten_by: str = "15:45"              # Flatten risky by 3:45 PM ET
    check_interval_minutes: int = 60       # Check every hour
    
    @classmethod
    def from_env(cls) -> 'PortfolioConfig':
        """Load from environment variables"""
        return cls(
            total_capital=float(os.getenv('NEXUS_TOTAL_CAPITAL', '1000')),
            base_trade_usd=float(os.getenv('NEXUS_BASE_TRADE_USD', '100')),
            max_risk_per_trade=float(os.getenv('NEXUS_MAX_RISK_PER_TRADE', '0.02')),
            max_portfolio_heat=float(os.getenv('NEXUS_MAX_PORTFOLIO_HEAT', '0.10')),
            max_position_size=float(os.getenv('NEXUS_MAX_POSITION_SIZE', '0.15')),
            default_stop_pct=float(os.getenv('NEXUS_DEFAULT_STOP_PCT', '0.02')),
            default_target_multiplier=float(os.getenv('NEXUS_TARGET_MULTIPLIER', '2.0')),
            max_daily_loss_pct=float(os.getenv('NEXUS_MAX_DAILY_LOSS_PCT', '3.0')),
            max_daily_trades=int(os.getenv('NEXUS_MAX_DAILY_TRADES', '20')),
            min_confidence=float(os.getenv('NEXUS_MIN_CONFIDENCE', '0.55')),
            flatten_by=os.getenv('NEXUS_FLATTEN_BY', '15:45'),
            check_interval_minutes=int(os.getenv('NEXUS_CHECK_INTERVAL', '60')),
        )


# =============================================================================
# TRADING UNIVERSES
# =============================================================================

# Crypto Day Trading Universe (liquid, high volume)
CRYPTO_DAY_TRADE_UNIVERSE = {
    "majors": {
        "label": "Major Cryptos",
        "pairs": ["BTC-USD", "ETH-USD"],
        "target_pct": 0.50,
    },
    "alts": {
        "label": "Alt Coins",
        "pairs": ["SOL-USD", "AVAX-USD", "LINK-USD", "UNI-USD"],
        "target_pct": 0.35,
    },
    "defi": {
        "label": "DeFi Tokens",
        "pairs": ["AAVE-USD", "COMP-USD", "MKR-USD"],
        "target_pct": 0.15,
    },
}

# Swing Trading Universe (hold 1-7 days)
CRYPTO_SWING_UNIVERSE = {
    "infrastructure": {
        "label": "Layer 1 Infrastructure",
        "pairs": ["ETH-USD", "SOL-USD", "AVAX-USD", "NEAR-USD"],
        "target_pct": 0.40,
    },
    "momentum": {
        "label": "Momentum Plays",
        "pairs": ["LINK-USD", "UNI-USD", "AAVE-USD", "SNX-USD"],
        "target_pct": 0.30,
    },
    "hedge": {
        "label": "Stable/BTC Hedge",
        "pairs": ["BTC-USD", "USDC-USD"],
        "target_pct": 0.30,
    },
}

ALL_DAY_TRADE_PAIRS = [p for cat in CRYPTO_DAY_TRADE_UNIVERSE.values() for p in cat["pairs"]]
ALL_SWING_PAIRS = [p for cat in CRYPTO_SWING_UNIVERSE.values() for p in cat["pairs"]]


# =============================================================================
# EXCHANGE CONFIGURATION
# =============================================================================

EXCHANGE_CONFIG = {
    "coinbase": {
        "sandbox": True,  # Paper trading by default
        "fee_maker": 0.006,  # 0.6%
        "fee_taker": 0.008,  # 0.8%
        "min_order_size": 10.0,
    },
    "binance": {
        "sandbox": True,
        "fee_maker": 0.001,  # 0.1%
        "fee_taker": 0.001,
        "min_order_size": 10.0,
    },
}


# =============================================================================
# SAFETY RAILS (Hardcoded Protections)
# =============================================================================

SAFETY_RAILS = {
    # Circuit breakers
    "daily_loss_circuit_breaker": 0.03,  # Stop at 3% daily loss
    "consecutive_loss_limit": 3,         # Stop after 3 consecutive losses
    
    # Order protections
    "max_slippage_pct": 1.0,             # Max 1% slippage
    "mandatory_stop_loss": True,         # Every trade must have stop
    "paper_only_default": True,          # Default to paper trading
    
    # Time protections
    "no_new_positions_after": "15:30",   # No new entries after 3:30 PM
    "flatten_all_by": "15:45",           # Close risky by 3:45 PM
    "weekend_trading": False,            # No weekend trading by default
}


# =============================================================================
# AGENT CONFIGURATION
# =============================================================================

AGENT_PERSONAS = {
    "conservative": {
        "description": "Risk-averse, focuses on capital preservation",
        "min_confidence": 0.70,
        "position_size_mult": 0.5,
        "stop_tightness": 1.5,  # 1.5x tighter stops
    },
    "balanced": {
        "description": "Balanced risk/reward approach",
        "min_confidence": 0.55,
        "position_size_mult": 1.0,
        "stop_tightness": 1.0,
    },
    "aggressive": {
        "description": "Higher risk tolerance, more active trading",
        "min_confidence": 0.45,
        "position_size_mult": 1.5,
        "stop_tightness": 0.8,  # Looser stops
    },
}


# =============================================================================
# NOTIFICATION CONFIG
# =============================================================================

NOTIFICATION_CHANNELS = {
    "telegram": {
        "enabled": True,
        "chat_id": os.getenv("TELEGRAM_CHAT_ID", ""),
        "events": ["trade", "circuit_breaker", "daily_summary", "error"],
    },
    "email": {
        "enabled": False,
        "address": os.getenv("ALERT_EMAIL", ""),
        "events": ["circuit_breaker", "daily_summary"],
    },
}
