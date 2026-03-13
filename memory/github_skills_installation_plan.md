# GitHub/GitLab Skills Inventory & Installation Plan
**Date:** March 7, 2026  
**Status:** Discovered, Not Installed

---

## DISCOVERED REPOSITORY SKILLS

### 1. GitHub Core (`github`)
- **Location:** `~/.npm-global1/lib/node_modules/openclaw/skills/github/`
- **Purpose:** GitHub operations via `gh` CLI
- **Category:** Version Control / Repository Management
- **Status:** ⚠️ Requires `gh` CLI installation
- **Dependencies:** `brew install gh` or `apt install gh`
- **Priority:** HIGH

**Capabilities:**
- List/view PRs and issues
- Check CI/workflow status
- Create/merge PRs
- Comment on issues
- Query GitHub API

---

### 2. GitHub Issues Auto-Fix (`gh-issues`)
- **Location:** `~/.npm-global1/lib/node_modules/openclaw/skills/gh-issues/`
- **Purpose:** Automated issue resolution with sub-agents
- **Category:** Automation / DevOps
- **Status:** ✅ Ready (uses curl + API, no CLI needed)
- **Dependencies:** GitHub API token
- **Priority:** HIGHEST

**Capabilities:**
- Fetch issues from any repo
- Spawn sub-agents to fix issues automatically
- Create PRs with fixes
- Handle PR review comments
- Watch mode for continuous monitoring
- Fork mode for upstream contributions

**Unique Features:**
- 6-phase orchestration pipeline
- Parallel sub-agent execution (up to 8)
- Claim system prevents duplicates
- Cursor tracking for sequential processing
- Cron-safe operation

---

### 3. GitHub Actions CLI (`github-actions-cli`)
- **Location:** `~/.npm-global1/lib/node_modules/openclaw/skills/github-actions-cli/`
- **Purpose:** NEXUS Council enterprise integration
- **Category:** CI/CD / DevOps
- **Status:** ✅ Auto-installed for NEXUS
- **Dependencies:** None
- **Priority:** MEDIUM

**Capabilities:**
- Part of NEXUS Council multi-agent system
- Enterprise agent swarm integration

---

### 4. GitLab API (`gitlab-api`)
- **Location:** `~/.openclaw/skills/archived/gitlab-api` (symlinked)
- **Purpose:** GitLab repository operations
- **Category:** Version Control / Repository Management
- **Status:** ⚠️ Archived, needs token setup
- **Dependencies:** GitLab API token
- **Priority:** LOW (GitHub primary)

**Capabilities:**
- Read/write files in GitLab repos
- List projects and branches
- Create/update/delete files
- Repository archive downloads
- Self-hosted GitLab support

---

## INSTALLATION PLAN

### Phase 1: Core GitHub Setup (Immediate)
1. **Install GitHub CLI:**
   ```bash
   brew install gh
   ```

2. **Authenticate:**
   ```bash
   gh auth login
   ```

3. **Verify:**
   ```bash
   gh auth status
   ```

### Phase 2: API Token Configuration (Immediate)
1. **Generate GitHub Token:**
   - Go to https://github.com/settings/tokens
   - Create fine-grained token with scopes:
     - `repo` (full repository access)
     - `workflow` (GitHub Actions)
     - `read:org` (organization read)

2. **Configure OpenClaw:**
   ```bash
   # Add to ~/.openclaw/openclaw.json
   {
     "skills": {
       "entries": {
         "gh-issues": {
           "apiKey": "ghp_YOUR_TOKEN_HERE"
         }
       }
     }
   }
   ```

### Phase 3: Repository Remote Setup
1. **Create GitHub Repository** (if not exists)
2. **Add Remote:**
   ```bash
   cd ~/clawd
   git remote add origin https://github.com/YOUR_USERNAME/clawd.git
   git branch -M main
   git push -u origin main
   ```

### Phase 4: Automation Deployment (Optional)
1. **Enable Issue Auto-Fix:**
   - Configure cron job for `gh-issues`
   - Set up watch mode for continuous monitoring
   - Configure Telegram notifications

2. **CI/CD Integration:**
   - Add GitHub Actions workflow
   - Integrate with existing monitoring

---

## CATEGORY MAPPING

| Skill | Primary Category | Secondary Categories |
|-------|------------------|---------------------|
| github | DevOps | Version Control, CI/CD |
| gh-issues | Automation | DevOps, AI/ML, Collaboration |
| github-actions-cli | DevOps | CI/CD, Enterprise |
| gitlab-api | DevOps | Version Control, Enterprise |

---

## PRIORITY MATRIX

| Skill | Business Value | Setup Complexity | Priority |
|-------|---------------|------------------|----------|
| gh-issues | ⭐⭐⭐⭐⭐ (Auto-fix saves hours) | Medium | HIGHEST |
| github | ⭐⭐⭐⭐ (Essential operations) | Low | HIGH |
| github-actions-cli | ⭐⭐⭐ (NEXUS integration) | None | MEDIUM |
| gitlab-api | ⭐⭐ (Backup option) | Medium | LOW |

---

## NEXT ACTIONS

1. [ ] Install `gh` CLI via brew
2. [ ] Authenticate with `gh auth login`
3. [ ] Generate GitHub personal access token
4. [ ] Configure token in OpenClaw settings
5. [ ] Create GitHub repo for clawd backup
6. [ ] Push current repository to GitHub
7. [ ] Test `gh-issues` skill with a sample issue

---

**Report Generated:** March 7, 2026  
**By:** Amazo 🤖
