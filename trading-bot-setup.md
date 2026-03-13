# Trading Bot Setup Guide

Complete guide for setting up automated trading bots on Mac (local) and server (cloud) environments.

---

## Part 1: Mac (Local) Setup

### Prerequisites
- macOS 12+ (Monterey or later)
- Python 3.9+ installed
- Homebrew
- API keys from exchanges (Binance, Coinbase, Kraken, etc.)

### Step 1: Install Dependencies

```bash
# Install Homebrew if not present
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and tools
brew install python@3.11 pipx node redis

# Ensure pipx is in PATH
pipx ensurepath

# Install trading tools
pipx install ccxt
pipx install freqtrade
pipx install hummingbot
```

### Step 2: Install NEXUS Trading Skills

```bash
# Install crypto trading skill
openclaw skills install crypto-trader

# Install portfolio tracking
openclaw skills install portfolio-tracker

# Install stock screener (for traditional markets)
openclaw skills install stock-screener

# Install DeFi analyzer
openclaw skills install defi-analyzer
```

### Step 3: Configure API Keys (Secure)

```bash
# Create secure config directory
mkdir -p ~/.trading/config
chmod 700 ~/.trading/config

# Set up API keys via NEXUS skills
crypto-trader init

# Add exchange credentials (NEVER commit these)
crypto-trader exchange add binance \
  --api-key="YOUR_BINANCE_API_KEY" \
  --api-secret="YOUR_BINANCE_SECRET"

crypto-trader exchange add coinbase \
  --api-key="YOUR_COINBASE_API_KEY" \
  --api-secret="YOUR_COINBASE_SECRET" \
  --passphrase="YOUR_COINBASE_PASSPHRASE"
```

### Step 4: Test Connection

```bash
# Check balances
crypto-trader balance

# Get current price
crypto-trader price --symbol=BTC/USDT

# Run paper trading test
crypto-trader paper --strategy=macd --symbol=BTC/USDT --balance=10000 --duration=24h
```

### Step 5: Create Trading Strategy

```bash
# Create strategy directory
mkdir -p ~/trading-strategies

# Example: Simple MACD strategy
cat > ~/trading-strategies/macd_strategy.json << 'EOF'
{
  "name": "MACD_Crossover",
  "exchange": "binance",
  "pair": "BTC/USDT",
  "timeframe": "1h",
  "strategy": {
    "type": "macd",
    "fast": 12,
    "slow": 26,
    "signal": 9
  },
  "risk_management": {
    "max_position_size": 100,
    "stop_loss_percent": 2,
    "take_profit_percent": 4
  }
}
EOF
```

### Step 6: Run Trading Bot

```bash
# Start with paper trading (recommended first)
crypto-trader trade \
  --strategy=macd \
  --symbol=BTC/USDT \
  --timeframe=1h \
  --paper \
  --balance=10000

# When ready for live trading:
# crypto-trader trade \
#   --strategy=macd \
#   --symbol=BTC/USDT \
#   --timeframe=1h \
#   --live \
#   --amount=100
```

### Step 7: Set Up Monitoring (Mac)

```bash
# Create launchd plist for auto-start
cat > ~/Library/LaunchAgents/com.nexus.tradingbot.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.nexus.tradingbot</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/crypto-trader</string>
        <string>trade</string>
        <string>--strategy=macd</string>
        <string>--symbol=BTC/USDT</string>
        <string>--config=/Users/YOUR_USERNAME/.trading/config/trading.json</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/YOUR_USERNAME/.trading/logs/trading.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/YOUR_USERNAME/.trading/logs/trading.error.log</string>
</dict>
</plist>
EOF

# Load the service
launchctl load ~/Library/LaunchAgents/com.nexus.tradingbot.plist

# Check status
launchctl list | grep com.nexus.tradingbot
```

---

## Part 2: Server (Cloud) Setup

### Option A: VPS (DigitalOcean/Linode/AWS Lightsail)

#### Step 1: Create Server

```bash
# Recommended specs for trading bot:
# - 2 vCPU
# - 4GB RAM
# - 80GB SSD
# - Ubuntu 22.04 LTS

# SSH into your server
ssh root@YOUR_SERVER_IP
```

#### Step 2: Server Hardening

```bash
# Update system
apt update && apt upgrade -y

# Create non-root user
adduser nexus-trader
usermod -aG sudo nexus-trader

# Set up firewall
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 8080/tcp  # Trading dashboard
ufw enable

# Install fail2ban
apt install fail2ban -y
systemctl enable fail2ban
```

#### Step 3: Install Trading Stack

```bash
# Install dependencies
apt install -y python3-pip python3-venv git redis-server nginx

# Install Node.js (for some trading tools)
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs

# Create trading user environment
su - nexus-trader

# Set up Python virtual environment
python3 -m venv ~/trading-venv
source ~/trading-venv/bin/activate

# Install trading packages
pip install ccxt pandas numpy ta-lib freqtrade hummingbot
```

#### Step 4: Install NEXUS Skills on Server

```bash
# Install OpenClaw on server
curl -fsSL https://openclaw.ai/install.sh | bash

# Install trading skills
openclaw skills install crypto-trader
openclaw skills install portfolio-tracker
openclaw skills install defi-analyzer
```

#### Step 5: Configure Trading Bot as System Service

```bash
# Create systemd service
sudo tee /etc/systemd/system/nexus-trader.service << 'EOF'
[Unit]
Description=NEXUS Trading Bot
After=network.target redis.service

[Service]
Type=simple
User=nexus-trader
WorkingDirectory=/home/nexus-trader
Environment=PATH=/home/nexus-trader/trading-venv/bin
Environment=PYTHONPATH=/home/nexus-trader/trading-venv/lib/python3.10/site-packages
ExecStart=/home/nexus-trader/trading-venv/bin/crypto-trader trade \
  --strategy=macd \
  --symbol=BTC/USDT \
  --timeframe=1h \
  --config=/home/nexus-trader/.trading/config/production.json
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable nexus-trader
sudo systemctl start nexus-trader

# Check status
sudo systemctl status nexus-trader
sudo journalctl -u nexus-trader -f
```

#### Step 6: Set Up Web Dashboard (Optional)

```bash
# Install freqtrade with web UI
pip install freqtrade

# Initialize freqtrade
freqtrade create-userdir --userdir ~/freqtrade
freqtrade new-config --config ~/freqtrade/config.json

# Edit config for your exchange
nano ~/freqtrade/config.json

# Start with web UI
freqtrade trade --config ~/freqtrade/config.json --strategy SampleStrategy

# Access dashboard at http://YOUR_SERVER_IP:8080
```

#### Step 7: Set Up Reverse Proxy (Nginx)

```bash
# Install nginx
sudo apt install nginx -y

# Create nginx config
sudo tee /etc/nginx/sites-available/trading << 'EOF'
server {
    listen 80;
    server_name YOUR_DOMAIN_OR_IP;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/trading /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Part 3: Docker Deployment (Recommended for Production)

### Docker Compose Setup

```yaml
# docker-compose.yml
version: '3.8'

services:
  trading-bot:
    image: freqtradeorg/freqtrade:stable
    container_name: nexus-trader
    volumes:
      - ./user_data:/freqtrade/user_data
      - ./config.json:/freqtrade/config.json:ro
      - ./strategies:/freqtrade/user_data/strategies
    ports:
      - "8080:8080"
    environment:
      - EXCHANGE_API_KEY=${EXCHANGE_API_KEY}
      - EXCHANGE_SECRET=${EXCHANGE_SECRET}
    command: >
      trade
      --config /freqtrade/config.json
      --strategy SampleStrategy
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  redis:
    image: redis:7-alpine
    container_name: nexus-redis
    volumes:
      - redis_data:/data
    restart: unless-stopped

  monitoring:
    image: prom/prometheus
    container_name: nexus-monitoring
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
    restart: unless-stopped

volumes:
  redis_data:
```

### Run with Docker

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f trading-bot

# Stop
docker-compose down
```

---

## Part 4: Security Best Practices

### API Key Security

```bash
# 1. Use IP whitelisting on exchanges
# 2. Enable withdrawal whitelist
# 3. Use trading-only API keys (no withdrawal permissions)
# 4. Rotate keys monthly

# Store keys securely (never in git)
export BINANCE_API_KEY="your_key"
export BINANCE_SECRET="your_secret"

# Or use a secrets manager
# - macOS: Keychain
# - Server: HashiCorp Vault, AWS Secrets Manager
```

### Server Security Checklist

```bash
# Disable password auth, use keys only
sudo nano /etc/ssh/sshd_config
# PasswordAuthentication no
# PubkeyAuthentication yes

# Set up automatic security updates
sudo apt install unattended-upgrades
sudo dpkg-reconfigure unattended-upgrades

# Install and configure UFW firewall
sudo ufw allow OpenSSH
sudo ufw enable

# Set up log monitoring
sudo apt install logwatch
```

---

## Part 5: Monitoring & Alerts

### Set Up Alerts

```bash
# Using NEXUS skills
crypto-trader alert price --symbol=BTC/USDT --condition=above --price=70000
crypto-trader alert price --symbol=BTC/USDT --condition=below --price=60000

# Portfolio alerts
crypto-trader alert portfolio --loss-percent=5
crypto-trader alert portfolio --gain-percent=10

# System alerts (server)
# - Use UptimeRobot or Pingdom for server monitoring
# - Set up Telegram/Discord webhooks for trade notifications
```

### Health Checks

```bash
# Create health check script
cat > ~/trading-health.sh << 'EOF'
#!/bin/bash
# Check if trading bot is running
if ! pgrep -f "crypto-trader"; then
  echo "Trading bot is down!" | mail -s "ALERT: Trading Bot Down" your-email@example.com
  sudo systemctl restart nexus-trader
fi

# Check API connectivity
crypto-trader balance > /dev/null 2>&1 || echo "API connection failed!"
EOF

chmod +x ~/trading-health.sh

# Add to crontab (every 5 minutes)
*/5 * * * * ~/trading-health.sh
```

---

## Quick Start Commands

### Mac
```bash
# Start trading
crypto-trader trade --strategy=macd --symbol=BTC/USDT --paper

# View portfolio
crypto-trader portfolio

# Check logs
tail -f ~/.trading/logs/trading.log
```

### Server
```bash
# Start service
sudo systemctl start nexus-trader

# View status
sudo systemctl status nexus-trader

# View logs
sudo journalctl -u nexus-trader -f

# Restart
sudo systemctl restart nexus-trader
```

---

## Next Steps

1. **Paper trade first** - Test strategies with fake money
2. **Start small** - Use minimal amounts when going live
3. **Monitor closely** - Watch the first few days carefully
4. **Scale gradually** - Increase position sizes as you gain confidence
5. **Keep backups** - Regular backups of config and trade history

---

**Need help?** Check the individual skill docs:
- `openclaw skills docs crypto-trader`
- `openclaw skills docs portfolio-tracker`
- `openclaw skills docs defi-analyzer`
