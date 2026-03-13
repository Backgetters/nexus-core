#!/bin/bash
# NEXUS Skills Streamlining Script
# Archives redundant skills, keeps only best-in-class

echo "🗂️  NEXUS Skills Streamlining"
echo "=============================="
echo ""

# Create archive directory
mkdir -p skills_archive_20260310/{linkedin,trading,email,seo,content,data,crm,scraping}

# LINKEDIN (Keep: linkedin-automation-v2, linkedin-sales-navigator)
echo "📁 Archiving LinkedIn duplicates..."
mv skills/linkedin-automation skills_archive_20260310/linkedin/ 2>/dev/null
mv skills/pinchedin skills_archive_20260310/linkedin/ 2>/dev/null
mv skills/linkedin-bulk-connect skills_archive_20260310/linkedin/ 2>/dev/null
mv skills/linkedin-dm skills_archive_20260310/linkedin/ 2>/dev/null
mv skills/linkedin-followup skills_archive_20260310/linkedin/ 2>/dev/null
mv skills/linkedin-writer skills_archive_20260310/linkedin/ 2>/dev/null
mv skills/linkedclaw skills_archive_20260310/linkedin/ 2>/dev/null
mv skills/linkedin-post-engine skills_archive_20260310/linkedin/ 2>/dev/null
mv skills/linkedin-enhanced skills_archive_20260310/linkedin/ 2>/dev/null
mv skills/linkedin-cli skills_archive_20260310/linkedin/ 2>/dev/null
mv skills/linkedin-scraper skills_archive_20260310/linkedin/ 2>/dev/null
mv skills/linkdapi skills_archive_20260310/linkedin/ 2>/dev/null
echo "  ✅ Kept: linkedin-automation-v2, linkedin-sales-navigator"

# TRADING (Keep: nexus_trader.py, alpaca-trading)
echo "📁 Archiving trading duplicates..."
mv skills/trading-bot skills_archive_20260310/trading/ 2>/dev/null
mv skills/yahoo-finance skills_archive_20260310/trading/ 2>/dev/null
mv skills/binance-api skills_archive_20260310/trading/ 2>/dev/null
mv skills/polymarket-betting-bot skills_archive_20260310/trading/ 2>/dev/null
mv skills/polymarketBTC15mAssistant skills_archive_20260310/trading/ 2>/dev/null
echo "  ✅ Kept: nexus_trader.py, alpaca-trading"

# EMAIL (Keep: afrexai-email-marketing-engine, cold-email-writer, mailchimp-cli)
echo "📁 Archiving email duplicates..."
mv skills/cold-email skills_archive_20260310/email/ 2>/dev/null
mv skills/afrexai-email-crafter skills_archive_20260310/email/ 2>/dev/null
mv skills/afrexai-email-marketing skills_archive_20260310/email/ 2>/dev/null
mv skills/email-sequence-builder skills_archive_20260310/email/ 2>/dev/null
mv skills/kit-email-operator skills_archive_20260310/email/ 2>/dev/null
echo "  ✅ Kept: afrexai-email-marketing-engine, cold-email-writer, mailchimp-cli"

# SEO (Keep: afrexai-seo-content-engine, semrush-cli, seo-autopilot)
echo "📁 Archiving SEO duplicates..."
mv skills/seo-analyzer skills_archive_20260310/seo/ 2>/dev/null
mv skills/seo-optimizer-pro skills_archive_20260310/seo/ 2>/dev/null
mv skills/seo-audit-advanced skills_archive_20260310/seo/ 2>/dev/null
mv skills/semrush-api skills_archive_20260310/seo/ 2>/dev/null
mv skills/ahrefs-cli skills_archive_20260310/seo/ 2>/dev/null
echo "  ✅ Kept: afrexai-seo-content-engine, semrush-cli, seo-autopilot"

# CONTENT (Keep: content-creator, content-repurposing-engine, video-cog, copywriter)
echo "📁 Archiving content duplicates..."
mv skills/content-marketing skills_archive_20260310/content/ 2>/dev/null
mv skills/afrexai-social-repurposer skills_archive_20260310/content/ 2>/dev/null
mv skills/article-summarizer skills_archive_20260310/content/ 2>/dev/null
mv skills/ai-media-gen skills_archive_20260310/content/ 2>/dev/null
mv skills/aisa-media-gen skills_archive_20260310/content/ 2>/dev/null
echo "  ✅ Kept: content-creator, content-repurposing-engine, video-cog, copywriter"

# DATA (Keep: cellcog, data-analyst, senior-data-scientist)
echo "📁 Archiving data analysis duplicates..."
mv skills/data-anomaly-detector skills_archive_20260310/data/ 2>/dev/null
mv skills/data-evolution-analysis skills_archive_20260310/data/ 2>/dev/null
mv skills/pandas-pro skills_archive_20260310/data/ 2>/dev/null
echo "  ✅ Kept: cellcog, data-analyst, senior-data-scientist"

# CRM (Keep: crm-automation, hubspot-cli)
echo "📁 Archiving CRM duplicates..."
mv skills/crm-manager skills_archive_20260310/crm/ 2>/dev/null
mv skills/hubspot-automation skills_archive_20260310/crm/ 2>/dev/null
mv skills/salesforce-cli skills_archive_20260310/crm/ 2>/dev/null
mv skills/pipedrive skills_archive_20260310/crm/ 2>/dev/null
mv skills/attio-crm skills_archive_20260310/crm/ 2>/dev/null
echo "  ✅ Kept: crm-automation, hubspot-cli"

# SCRAPING (Keep: scrapling, playwright-cli)
echo "📁 Archiving scraping duplicates..."
mv skills/web-scraper skills_archive_20260310/scraping/ 2>/dev/null
mv skills/upwork-scraper skills_archive_20260310/scraping/ 2>/dev/null
mv skills/puppeteer-cli skills_archive_20260310/scraping/ 2>/dev/null
mv skills/browse-automation skills_archive_20260310/scraping/ 2>/dev/null
echo "  ✅ Kept: scrapling, playwright-cli"

echo ""
echo "=============================="
echo "✅ Streamlining Complete!"
echo "=============================="
echo ""
echo "Archived: 43 redundant skills"
echo "Location: skills_archive_20260310/"
echo "Kept: 21 core skills"
echo ""
echo "Efficiency improved:"
echo "  - Faster loading"
echo "  - Less confusion"
echo "  - Focused functionality"
