#!/bin/bash
# NEXUS Configuration Recovery Script
# Run this to restore all configurations after a fresh start

echo "⚡ NEXUS Configuration Recovery"
echo "==============================="
echo ""

# Check if we're in the right directory
if [ ! -f "IDENTITY.md" ]; then
    echo "❌ Error: Must run from ~/clawd directory"
    echo "   cd ~/clawd && bash recover_configs.sh"
    exit 1
fi

echo "📂 Checking configuration files..."

# Essential files to verify
ESSENTIAL_FILES=(
    "IDENTITY.md"
    "USER.md"
    "SOUL.md"
    "HEARTBEAT.md"
    "CONFIG_ARCHIVE.md"
    "trading/nexus_trader_config.py"
    "trading/telegram_buttons.py"
    "jobs/config/james_profile.json"
    "jobs/auto_apply.py"
)

MISSING=0
for file in "${ESSENTIAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file (MISSING)"
        MISSING=$((MISSING + 1))
    fi
done

echo ""
echo "📊 Status: $MISSING files missing"

if [ $MISSING -eq 0 ]; then
    echo ""
    echo "✅ All configurations present!"
    echo ""
    echo "Quick commands:"
    echo "   System health:  bash monitoring/system_health.sh"
    echo "   Sync repos:     ~/NEXUS/scripts/sync_repos.sh"
    echo "   Job scraper:    cd jobs && python3 quick_scrape.py"
    echo "   Trading bot:    cd trading && python3 nexus_trader.py"
else
    echo ""
    echo "⚠️  Some files missing. Check git status or restore from backup:"
    echo "   tar -xzf ~/Desktop/NEXUS_CONFIG_BACKUP_2026-03-13.tar.gz"
fi

echo ""
echo "==============================="
echo "NEXUS ready for command. ⚡"
