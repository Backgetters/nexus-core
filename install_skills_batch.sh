#!/bin/bash
# Batch skill installer for NEXUS
LOGFILE="~/clawd/skill_install_logs/batch_$(date +%Y%m%d_%H%M%S).log"
mkdir -p ~/clawd/skill_install_logs

# List of high-value skills to install from awesome list
SKILLS=(
  "achurch"
  "agent-config"
  "agent-council"
  "agent-identity-kit"
  "agenticflow-skill"
  "agentlens"
  "agentskills-io"
  "apple-hig"
  "arbiter"
  "aster"
  "avatar-video-messages"
  "backend-patterns"
  "bidclub"
  "botpress-adk"
  "browse"
  "buildlog"
  "cc-godmode"
  "cellcog"
  "claude-optimised"
  "claude-team"
  "clawder"
  "code-mentor"
  "codebuddy-code"
  "codeconductor"
  "coder-workspaces"
  "codex-account-switcher"
  "codex-monitor"
  "codex-orchestration"
  "codex-quota"
  "cold-email"
  "competitor-monitor"
  "content-creator"
  "content-id-guide"
  "cto-advisor"
  "cursor-agent"
  "data-analyst"
  "debug-pro"
  "dnd-character-creator"
  "doc-coauthoring"
  "doc-indexer"
  "docker-cli"
  "docker-compose-manager"
  "docker-essentials"
)

INSTALLED=0
FAILED=0

for skill in "${SKILLS[@]}"; do
    echo "Installing: $skill" | tee -a "$LOGFILE"
    if clawhub install "$skill" 2>&1 | tee -a "$LOGFILE"; then
        ((INSTALLED++))
        echo "✅ Installed: $skill" | tee -a "$LOGFILE"
    else
        ((FAILED++))
        echo "❌ Failed: $skill" | tee -a "$LOGFILE"
    fi
    sleep 1
done

echo "" | tee -a "$LOGFILE"
echo "========================================" | tee -a "$LOGFILE"
echo "Batch Complete!" | tee -a "$LOGFILE"
echo "Installed: $INSTALLED" | tee -a "$LOGFILE"
echo "Failed: $FAILED" | tee -a "$LOGFILE"
echo "========================================" | tee -a "$LOGFILE"
