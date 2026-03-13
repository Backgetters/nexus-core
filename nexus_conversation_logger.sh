#!/bin/bash
# NEXUS Conversation Logger v1.0
# Automatically logs all conversations to timestamped files
# Location: ~/Desktop/NEXUS_Conversations/

CONVERSATION_DIR="$HOME/Desktop/NEXUS_Conversations"
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
LOG_FILE="$CONVERSATION_DIR/conversation_$DATE.txt"

# Create directory if it doesn't exist
mkdir -p "$CONVERSATION_DIR"

# Function to log a message
log_message() {
    local speaker="$1"
    local message="$2"
    local time=$(date '+%H:%M:%S')
    
    echo "" >> "$LOG_FILE"
    echo "[$time] $speaker:" >> "$LOG_FILE"
    echo "$message" >> "$LOG_FILE"
    echo "---" >> "$LOG_FILE"
}

# If arguments provided, log them
if [ $# -ge 2 ]; then
    log_message "$1" "$2"
fi

echo "Conversation logged to: $LOG_FILE"
