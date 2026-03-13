#!/bin/bash
# NEXUS Trading Cron Jobs
# Automated trading schedule with swarm-trader principles
# Created: 2026-03-13

echo "⚡ Setting up NEXUS Trading Cron Jobs..."
echo "======================================="

# Check if running in isolated session (required for trading)
if [ -z "$OPENCLAW_SESSION" ]; then
    echo "Note: These jobs should be added via 'openclaw cron add' for isolated execution"
fi

# =============================================================================
# TRADING SCHEDULE
# =============================================================================

echo ""
echo "📊 Proposed Trading Schedule:"
echo "-----------------------------"

cat << 'EOF'

Market Hours (ET):
  9:30 AM  - Market Open
  11:00 AM - Mid-morning check
  1:00 PM  - Lunch session
  3:00 PM  - Late afternoon
  3:45 PM  - FLATTEN (close risky positions)
  4:00 PM  - Market Close

Cron Jobs to Add:
=================

# 1. Pre-Market Portfolio Check (9:00 AM ET, Mon-Fri)
openclaw cron add --name nexus-portfolio-check \
  --cron "0 9 * * 1-5" \
  --tz "America/New_York" \
  --session isolated \
  --agent nexus \
  --model "anthropic/claude-sonnet-4-6" \
  --announce \
  --message "Pre-market portfolio check. Review positions, check overnight moves, verify API connectivity."

# 2. Market Open (9:30 AM ET, Mon-Fri)
openclaw cron add --name nexus-market-open \
  --cron "30 9 * * 1-5" \
  --tz "America/New_York" \
  --session isolated \
  --agent nexus \
  --model "anthropic/claude-sonnet-4-6" \
  --announce \
  --message "Market open. Scan for opportunities, analyze major pairs, execute high-confidence setups with mandatory stops."

# 3. Mid-Morning Check (11:00 AM ET, Mon-Fri)
openclaw cron add --name nexus-midmorning \
  --cron "0 11 * * 1-5" \
  --tz "America/New_York" \
  --session isolated \
  --agent nexus \
  --model "anthropic/claude-sonnet-4-6" \
  --announce \
  --message "Mid-morning check. Review existing positions, adjust stops to breakeven, look for new setups."

# 4. Lunch Session (1:00 PM ET, Mon-Fri)
openclaw cron add --name nexus-lunch \
  --cron "0 13 * * 1-5" \
  --tz "America/New_York" \
  --session isolated \
  --agent nexus \
  --model "anthropic/claude-sonnet-4-6" \
  --announce \
  --message "Lunch session. Light trading, range plays only. Reduce exposure if choppy."

# 5. Late Afternoon (3:00 PM ET, Mon-Fri)
openclaw cron add --name nexus-late \
  --cron "0 15 * * 1-5" \
  --tz "America/New_York" \
  --session isolated \
  --agent nexus \
  --model "anthropic/claude-sonnet-4-6" \
  --announce \
  --message "Late afternoon. Last chance for major moves. Prepare flatten list for 3:45 PM."

# 6. FLATTEN (3:45 PM ET, Mon-Fri) - CRITICAL
openclaw cron add --name nexus-flatten \
  --cron "45 15 * * 1-5" \
  --tz "America/New_York" \
  --session isolated \
  --agent nexus \
  --model "anthropic/claude-sonnet-4-6" \
  --announce \
  --message "FLATTEN RISKY POSITIONS. Close speculative trades, reduce exposure before close. NO EXCEPTIONS."

# 7. Post-Market Summary (4:30 PM ET, Mon-Fri)
openclaw cron add --name nexus-post-market \
  --cron "30 16 * * 1-5" \
  --tz "America/New_York" \
  --session isolated \
  --agent nexus \
  --model "anthropic/claude-sonnet-4-6" \
  --announce \
  --message "Post-market summary. Calculate daily P&L, update trade journal, prepare for tomorrow."

# 8. Daily Report (9:00 PM ET, Daily)
openclaw cron add --name nexus-daily-report \
  --cron "0 21 * * *" \
  --tz "America/New_York" \
  --session isolated \
  --agent nexus \
  --model "anthropic/claude-sonnet-4-6" \
  --announce \
  --message "Generate daily trading report. Summary of trades, P&L, lessons learned."

EOF

echo ""
echo "======================================="
echo "✅ Cron job templates generated!"
echo ""
echo "To activate these jobs:"
echo "  1. Review the commands above"
echo "  2. Run each 'openclaw cron add' command"
echo "  3. Verify with: openclaw cron list"
echo ""
echo "Risk Management Reminders:"
echo "  • Max 2% risk per trade"
echo "  • Max 10% portfolio heat"
echo "  • Daily circuit breaker at 3% loss"
echo "  • Mandatory flatten at 3:45 PM"
echo "  • Paper trading by default"
echo ""
