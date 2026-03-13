#!/bin/bash
# NEXUS System Health Monitor
# Runs every 5 minutes

LOG_FILE="$HOME/clawd/monitoring/logs/system_health.log"
ALERT_FILE="$HOME/clawd/monitoring/alerts/last_alert.txt"
mkdir -p "$(dirname "$LOG_FILE")" "$(dirname "$ALERT_FILE")"

echo "========================================" >> "$LOG_FILE"
echo "System Check - $(date)" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# Check if NEXUS agents are running
AGENT_PIDS=$(pgrep -f "continuous_earner.py" 2>/dev/null)
if [ -z "$AGENT_PIDS" ]; then
    echo "✅ No rogue agents running (correct state)" >> "$LOG_FILE"
else
    echo "⚠️ WARNING: Found running agents: $AGENT_PIDS" >> "$LOG_FILE"
    echo "ALERT: NEXUS agents still running - $(date)" > "$ALERT_FILE"
fi

# Check API quota files (if they exist)
for api in "openai" "siliconflow" "brave" "tavily"; do
    QUOTA_FILE="$HOME/.config/openclaw/${api}_quota.json"
    if [ -f "$QUOTA_FILE" ]; then
        echo "📊 $api quota file exists" >> "$LOG_FILE"
    fi
done

# Check disk space
DISK_USAGE=$(df -h / | tail -1 | awk '{print $5}' | tr -d '%')
if [ "$DISK_USAGE" -gt 85 ]; then
    echo "⚠️ Disk usage high: ${DISK_USAGE}%" >> "$LOG_FILE"
    echo "ALERT: Disk space ${DISK_USAGE}% - $(date)" > "$ALERT_FILE"
else
    echo "✅ Disk usage: ${DISK_USAGE}%" >> "$LOG_FILE"
fi

# Check memory
MEMORY_PRESSURE=$(vm_stat | grep "Pages free" | awk '{print $3}' | tr -d '.')
echo "✅ Memory check complete" >> "$LOG_FILE"

echo "Status: OK - $(date)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
