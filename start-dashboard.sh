#!/bin/bash
# NEXUS Mission Control Dashboard Server
# Serves the web dashboard on localhost:8080

DASHBOARD_DIR="$HOME/clawd/dashboard"
PORT=8080

echo "⚡ NEXUS Mission Control Dashboard"
echo "=================================="
echo "Starting server on http://localhost:$PORT"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Check if Python is available
if command -v python3 &> /dev/null; then
    python3 -m http.server $PORT --directory "$DASHBOARD_DIR"
elif command -v python &> /dev/null; then
    python -m SimpleHTTPServer $PORT --directory "$DASHBOARD_DIR"
else
    echo "Error: Python not found. Please install Python."
    exit 1
fi
