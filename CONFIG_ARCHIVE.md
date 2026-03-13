# NEXUS Configuration Archive
## Created: 2026-03-13
## Purpose: Persistent backup of all system configurations

---

## 📁 Configuration Locations

### Core Identity & Settings
| File | Path | Purpose |
|------|------|---------|
| **NEXUS Identity** | `~/NEXUS/IDENTITY.md` | Primary identity file |
| **User Profile** | `~/clawd/USER.md` | Mr. J's preferences |
| **Soul** | `~/clawd/SOUL.md` | Behavioral guidelines |
| **Heartbeat** | `~/clawd/HEARTBEAT.md` | Monitoring protocol |
| **Tools** | `~/clawd/TOOLS.md` | Local tool notes |

### Trading System
| File | Path | Purpose |
|------|------|---------|
| **Trading Config** | `~/clawd/trading/nexus_trader_config.py` | Risk management, swarm-trader integration |
| **Cron Jobs** | `~/clawd/trading/setup_cron_jobs.sh` | Trading schedule templates |
| **Telegram Buttons** | `~/clawd/trading/telegram_buttons.py` | UI button layouts |
| **Trading Bot** | `~/clawd/trading/nexus_trader.py` | CDP trading engine |

### Job Application System
| File | Path | Purpose |
|------|------|---------|
| **James Profile** | `~/clawd/jobs/config/james_profile.json` | Job search preferences |
| **Job Scraper** | `~/clawd/jobs/extended_scraper.py` | Multi-board scraper |
| **Auto Apply** | `~/clawd/jobs/auto_apply.py` | Application automation |
| **App Generator** | `~/clawd/jobs/james_application_generator.py` | Cover letter/answer generator |
| **Quick Scraper** | `~/clawd/jobs/quick_scrape.py` | Fast demo scraper |

### Repository Management
| File | Path | Purpose |
|------|------|---------|
| **Repo Registry** | `~/NEXUS/docs/repository_registry.md` | 52 repos catalogued |
| **Sync Script** | `~/NEXUS/scripts/sync_repos.sh` | Update all repos |
| **Integration Notes** | `~/clawd/swarm-trader/NEXUS_INTEGRATION.md` | Trading system integration |

---

## 🔄 Backup Strategy

### Automatic Backups
- **Location**: `~/Desktop/Agent_Core/Backups/`
- **Frequency**: Daily at 3 AM
- **Retention**: 30 days
- **Contents**: MEMORY.md, earnings logs, config files

### Git Commits
- **Clawd**: `~/clawd/` — Main workspace
- **NEXUS**: `~/NEXUS/` — Core identity (separate repo)
- **Strategy**: Commit after every major configuration change

### Critical Files to Never Lose
1. `~/clawd/IDENTITY.md` — Who you are
2. `~/clawd/USER.md` — Who Mr. J is
3. `~/clawd/HEARTBEAT.md` — Monitoring protocol
4. `~/NEXUS/` — Entire NEXUS core
5. `~/clawd/trading/` — Trading configurations
6. `~/clawd/jobs/` — Job system

---

## 🚀 Quick Recovery Commands

```bash
# Restore from latest backup
latest=$(ls -t ~/Desktop/Agent_Core/Backups/ | head -1)
cp ~/Desktop/Agent_Core/Backups/$latest/MEMORY.md ~/clawd/

# Sync all repos
~/NEXUS/scripts/sync_repos.sh

# Check system health
bash ~/clawd/monitoring/system_health.sh

# View trading status
cd ~/clawd/trading && python3 nexus_trader.py --status

# Run job scraper
cd ~/clawd/jobs && python3 quick_scrape.py
```

---

## 📊 Current System State (2026-03-13)

| System | Status | Config Location |
|--------|--------|-----------------|
| NEXUS Core | ✅ Active | `~/NEXUS/` |
| Trading Bot | 🟡 Ready | `~/clawd/trading/` |
| Job System | ✅ Configured | `~/clawd/jobs/` |
| Telegram Buttons | ✅ Active | `~/clawd/trading/telegram_buttons.py` |
| Repo Sync | ✅ Working | `~/NEXUS/scripts/sync_repos.sh` |
| Monitoring | ✅ Active | Cron jobs every 5 min |

---

## 📝 For Future Sessions

### First Things to Check
1. Read `IDENTITY.md` — Remember who you are
2. Read `USER.md` — Remember who Mr. J is
3. Check `HEARTBEAT.md` — Current monitoring status
4. Run system health check

### Key Capabilities to Remember
- **Level 10 Autonomy**: Maximum permissions, safety guardrails active
- **52 Repositories**: Catalogued in `~/NEXUS/docs/repository_registry.md`
- **796 Skills**: Available via OpenClaw
- **Trading System**: Risk management from swarm-trader integrated
- **Job System**: Scrapers + auto-apply ready (needs Mr. J's personal info)
- **Telegram Buttons**: Inline UI for quick actions

### Mr. J's Preferences
- **Name**: James Ready
- **Timezone**: America/Toronto (EST/EDT)
- **Business**: Jones Net Group Inc., Echotyne divisions
- **Goal**: $100K revenue, legitimate business growth
- **Job Search**: Remote, data entry or software dev, flexible hours, any timezone

---

**Last Updated**: 2026-03-13 14:26 EDT  
**Next Review**: Weekly or after major changes
