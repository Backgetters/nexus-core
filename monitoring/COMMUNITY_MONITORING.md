# Community Monitoring Framework
**Created:** 2026-03-15 19:40 EDT
**Status:** Active
**Frequency:** Every 4 hours during active hours (8 AM - 10 PM EST)

## Communities to Monitor

### Primary Sources
1. **r/openclaw** - Reddit community for OpenClaw users
2. **GitHub Issues** - openclaw/openclaw repository
3. **Discord** - OpenClaw official server (if accessible)
4. **Twitter/X** - @openclaw mentions and discussions

### Secondary Sources
5. **Hacker News** - Show HN posts about OpenClaw
6. **Lobste.rs** - Programming community discussions
7. **Indie Hackers** - Builder community

## What to Track

### Issues & Problems
- Installation failures
- Configuration errors
- Skill-related bugs
- Performance problems
- Security concerns
- Breaking changes

### Best Practices
- Optimization tips
- Workflow improvements
- Security hardening
- Cost-saving strategies
- Integration patterns

### Feature Requests
- Most requested features
- Workarounds people use
- Plugin/skill ideas

## Tracking Method

### Efficient Review Protocol
- **Scope:** Top 20 posts (Top + New categories combined)
- **Frequency:** Every 3-5 hours during active hours (8 AM - 11 PM)
- **Focus:** Breaking news, actionable issues, best practices
- **Token Budget:** ~2k-3k tokens per check (efficient but thorough)

### Review Schedule
- **8 AM:** Morning check (overnight developments)
- **12 PM:** Midday check
- **5 PM:** Afternoon check
- **10 PM:** Evening check

### Process
1. Browse r/openclaw/top/?t=day (top 10 posts)
2. Browse r/openclaw/new (top 10 posts)
3. Quick scan Twitter/X for #openclaw (5-10 recent tweets)
4. Log to daily intel file if significant findings
5. Alert immediately if breaking news or critical issues

### Prioritization (Skip Low-Value Content)
- ✅ **LOG:** Breaking news, forks, security issues, cost optimizations, architecture discussions
- ✅ **LOG:** High-engagement posts (20+ upvotes or 10+ comments)
- ❌ **SKIP:** "I don't get the hype" posts, basic setup questions, duplicate issues
- ❌ **SKIP:** Ads, off-topic discussions, low-effort showcases

## Output Format

Each daily log includes:
1. **Breaking Developments** - Critical news, forks, launches
2. **Significant Developments** - Important updates, tools, patterns
3. **Pattern Analysis** - Recurring issues, community sentiment
4. **Strategic Recommendations** - Action items with timelines
5. **🔗 Link & Repo Summary** - All repositories, tools, resources with relevance ratings
6. **Metrics** - Community activity stats, NEXUS alignment score

### Link/Repo Summary Format
```markdown
| Repo | Author | Purpose | Activity | Relevance |
|------|--------|---------|----------|-----------|
| [name](url) | author | brief description | stars/upvotes | HIGH/MEDIUM/LOW - why |
```

## Storage
- Location: `~/clawd/monitoring/community_intel/`
- Daily files: `community_intel_YYYYMMDD.md`
- Weekly summaries: `community_weekly_YYYY-W##.md`

## Integration with HEARTBEAT.md

Add to monitoring jobs:
- **Community Intel (Every 4 hours)**
  - Check r/openclaw for new issues
  - Check GitHub for bug reports
  - Summarize findings
  - Action: Log to file, alert on critical issues

---

## First Actions Needed

1. Configure Brave API key for web_search
2. Set up cron job for community monitoring
3. Create initial scan of current issues
4. Establish baseline of common problems

**Next community check:** As soon as web search is configured
