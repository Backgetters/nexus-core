#!/bin/bash
# NEXUS Top GitHub Repos Clone Script
# Highly-starred repos for automation, AI, trading, and business

echo "⚡ Cloning Top GitHub Repositories"
echo "==================================="
echo ""

REPO_BASE="/Users/tomegathericon/clawd/repos-top"
mkdir -p "$REPO_BASE"
cd "$REPO_BASE"

# Track stats
CLONED=0
FAILED=0
EXISTING=0

git_clone_smart() {
    local url="$1"
    local name=$(basename "$url" .git)
    
    if [ -d "$name" ]; then
        echo "  ○ $name exists"
        EXISTING=$((EXISTING + 1))
        return 0
    fi
    
    if git clone --depth 1 "$url" "$name" 2>/dev/null; then
        echo "  ✓ $name cloned"
        CLONED=$((CLONED + 1))
        return 0
    else
        echo "  ✗ $name failed"
        FAILED=$((FAILED + 1))
        return 1
    fi
}

echo "📦 AI Agents & Automation"
echo "--------------------------"
git_clone_smart "https://github.com/Shubhamsaboo/awesome-llm-apps.git"
git_clone_smart "https://github.com/google-gemini/gemini-cli.git"
git_clone_smart "https://github.com/browser-use/browser-use.git"
git_clone_smart "https://github.com/crewAIInc/crewAI.git"
git_clone_smart "https://github.com/mem0ai/mem0.git"
git_clone_smart "https://github.com/microsoft/ai-agents-for-beginners.git"

echo ""
echo "📦 Trading Bots"
echo "---------------"
git_clone_smart "https://github.com/freqtrade/freqtrade.git"
git_clone_smart "https://github.com/hummingbot/hummingbot.git"
git_clone_smart "https://github.com/jesse-ai/jesse.git"
git_clone_smart "https://github.com/Drakkar-Software/OctoBot.git"
git_clone_smart "https://github.com/chrisleekr/binance-trading-bot.git"

echo ""
echo "📦 Job Application Automation"
echo "------------------------------"
git_clone_smart "https://github.com/imon333/Job-apply-AI-agent.git"
git_clone_smart "https://github.com/Schlaflied/job-autopilot.git"
git_clone_smart "https://github.com/ishaannarula/job-application-automation.git"

echo ""
echo "📦 Web Scraping"
echo "---------------"
git_clone_smart "https://github.com/apify/crawlee.git"
git_clone_smart "https://github.com/apify/crawlee-python.git"
git_clone_smart "https://github.com/D4Vinci/Scrapling.git"
git_clone_smart "https://github.com/getmaxun/maxun.git"
git_clone_smart "https://github.com/firecrawl/firecrawl-mcp-server.git"

echo ""
echo "📦 Business Intelligence"
echo "------------------------"
git_clone_smart "https://github.com/metabase/metabase.git"
git_clone_smart "https://github.com/OpenBB-finance/OpenBB.git"
git_clone_smart "https://github.com/ToolJet/ToolJet.git"
git_clone_smart "https://github.com/FlowiseAI/Flowise.git"

echo ""
echo "📦 Workflow Automation (n8n)"
echo "-----------------------------"
git_clone_smart "https://github.com/n8n-io/n8n.git"
git_clone_smart "https://github.com/makafeli/n8n-workflow-builder.git"
git_clone_smart "https://github.com/salacoste/mcp-n8n-workflow-builder.git"

echo ""
echo "📦 Data & Analytics"
echo "-------------------"
git_clone_smart "https://github.com/dbt-labs/dbt-core.git"
git_clone_smart "https://github.com/duckdb/duckdb.git"
git_clone_smart "https://github.com/apache/superset.git"

echo ""
echo "==================================="
echo "✅ Top Repos Clone Complete"
echo "==================================="
echo "Cloned: $CLONED"
echo "Existing: $EXISTING"
echo "Failed: $FAILED"
echo ""
echo "Total in $REPO_BASE:"
ls -1 | wc -l
echo ""
echo "Disk usage:"
du -sh .
