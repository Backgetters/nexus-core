#!/bin/bash
# n8n Workflow Trigger Script
# Usage: trigger-workflow.sh --id <workflow-id> [--data <json>]

N8N_BASE_URL="${N8N_BASE_URL:-http://localhost:5678}"
N8N_API_KEY="${N8N_API_KEY:-YOUR_API_KEY_HERE}"
WORKFLOW_ID=""
DATA="{}"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --id) WORKFLOW_ID="$2"; shift 2 ;;
    --data) DATA="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [ -z "$WORKFLOW_ID" ]; then
  echo "Usage: trigger-workflow.sh --id <workflow-id> [--data <json>]"
  exit 1
fi

echo "Triggering n8n workflow: $WORKFLOW_ID"
echo "Base URL: $N8N_BASE_URL"

# Trigger workflow via webhook or API
if [[ "$WORKFLOW_ID" == webhook-* ]]; then
  # Webhook trigger
  WEBHOOK_PATH="${WORKFLOW_ID#webhook-}"
  RESPONSE=$(curl -s -X POST "$N8N_BASE_URL/webhook/$WEBHOOK_PATH" \
    -H "Content-Type: application/json" \
    -d "$DATA")
  echo "Webhook response: $RESPONSE"
else
  # API trigger
  RESPONSE=$(curl -s -X POST "$N8N_BASE_URL/api/v1/workflows/$WORKFLOW_ID/execute" \
    -H "X-N8N-API-KEY: $N8N_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"data\":$DATA}")
  echo "Execution response: $RESPONSE"
fi
