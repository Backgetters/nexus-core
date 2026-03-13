#!/bin/bash
# NEXUS Model Provider Switcher

echo "🔄 NEXUS Model Provider Switcher"
echo "================================"
echo ""
echo "Current: Kimi (moonshot/kimi-k2.5) - PRIMARY"
echo ""
echo "Options:"
echo "1) Use Kimi (Primary) - Current"
echo "2) Use OmniRoute (SiliconFlow → OpenAI → Others)"
echo "3) Start OmniRoute backup system"
echo "4) Stop OmniRoute backup system"
echo "5) Check OmniRoute status"
echo ""
read -p "Select option (1-5): " choice

case $choice in
  1)
    echo "✅ Using Kimi as primary (current setting)"
    echo "   No changes needed."
    ;;
  2)
    echo "🔄 Switching to OmniRoute..."
    echo "   Update your OpenClaw config to use:"
    echo "   Base URL: http://localhost:20128/v1"
    echo "   API Key: (any value)"
    ;;
  3)
    echo "🚀 Starting OmniRoute..."
    cd ~/clawd/super-repo/skills/ai-gateway/omniroute-source
    cp ../../config/omniroute/.env.template .env
    ./../../config/omniroute/start-omniroute.sh &
    echo "   OmniRoute starting on http://localhost:20128"
    ;;
  4)
    echo "🛑 Stopping OmniRoute..."
    pkill -f "omniroute" || echo "   OmniRoute not running"
    ;;
  5)
    echo "📊 Checking OmniRoute status..."
    if curl -s http://localhost:20128/health > /dev/null 2>&1; then
      echo "   ✅ OmniRoute is running"
      echo "   Dashboard: http://localhost:20128"
    else
      echo "   ❌ OmniRoute is not running"
      echo "   Start it with option 3"
    fi
    ;;
  *)
    echo "❌ Invalid option"
    ;;
esac
