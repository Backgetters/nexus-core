#!/bin/bash
# Nexus Trading Bot Launcher v2
# Usage: ./start_trader.sh [start|stop|restart|status|logs]

TRADER_DIR="$HOME/clawd/trading"
PID_FILE="$TRADER_DIR/nexus_trader.pid"

start_trader() {
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        echo "Trader already running (PID: $(cat $PID_FILE))"
        exit 1
    fi
    
    echo "🚀 Starting Nexus Trading Bot v2.0..."
    cd "$TRADER_DIR"
    
    # Source environment
    if [ -f ".env.nexus" ]; then
        set -a
        source .env.nexus
        set +a
    fi
    
    # Run in background with logging
    nohup python3 nexus_trader.py > logs/trader_output.log 2>&1 &
    echo $! > "$PID_FILE"
    
    echo "✅ Trader started (PID: $(cat $PID_FILE))"
    echo "📊 Logs: tail -f $TRADER_DIR/logs/nexus_trader.log"
    echo "⏱️  First trade cycle in ~10 seconds..."
}

stop_trader() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "🛑 Stopping trader (PID: $PID)..."
            kill "$PID"
            rm "$PID_FILE"
            echo "✅ Trader stopped"
        else
            echo "Trader not running (stale PID file removed)"
            rm "$PID_FILE"
        fi
    else
        echo "Trader not running"
    fi
}

status_trader() {
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        echo "🟢 Trader RUNNING (PID: $(cat $PID_FILE))"
        echo ""
        echo "Recent logs:"
        tail -15 "$TRADER_DIR/logs/nexus_trader.log" 2>/dev/null || echo "No logs yet"
    else
        echo "🔴 Trader STOPPED"
    fi
}

show_logs() {
    tail -f "$TRADER_DIR/logs/nexus_trader.log"
}

case "${1:-start}" in
    start)
        start_trader
        ;;
    stop)
        stop_trader
        ;;
    restart)
        stop_trader
        sleep 2
        start_trader
        ;;
    status)
        status_trader
        ;;
    logs)
        show_logs
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs}"
        exit 1
        ;;
esac
