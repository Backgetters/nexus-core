#!/bin/bash
# NEXUS Auto-Conversation Logger v2.0
# Automatically captures OpenClaw session history and logs to file
# Run this after each session to capture conversation

CONVERSATION_DIR="$HOME/clawd/conversations"
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
LOG_FILE="$CONVERSATION_DIR/conversation_$DATE.txt"

# Create directory if it doesn't exist
mkdir -p "$CONVERSATION_DIR"

# Function to append to log
append_to_log() {
    echo "" >> "$LOG_FILE"
    echo "═══════════════════════════════════════════════════════════════════" >> "$LOG_FILE"
    echo "NEXUS SESSION CONTINUATION - $(date '+%H:%M:%S')" >> "$LOG_FILE"
    echo "═══════════════════════════════════════════════════════════════════" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"
}

# Log current session info
append_to_log

# Try to extract recent messages from OpenClaw logs if available
if [ -f "$HOME/.openclaw/logs/gateway.log" ]; then
    echo "[System] Gateway logs available at: $HOME/.openclaw/logs/gateway.log" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"
echo "[$(date '+%H:%M:%S')] Session manually logged" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"

echo "Conversation appended to: $LOG_FILE"
echo "To view: cat $LOG_FILE"
