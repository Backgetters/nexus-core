# NEXUS Job Application System

## Overview
Automated job search and application system with AI-generated responses.

## Components

### 1. Job Scraper (`scrapers.py`)
- **RemoteOK** — Remote tech jobs
- **We Work Remotely** — Curated remote jobs
- **LinkedIn** — Professional network (requires auth)
- **Indeed** — General job board

### 2. Application Bot (`job_application_bot.py`)
- Filters jobs by preferences
- Generates AI cover letters
- Answers application questions
- Tracks applications

### 3. Form Filler
- Auto-fills common fields
- Handles file uploads (resume)
- Answers dynamic questions

## Setup

```bash
# Install dependencies
pip install playwright beautifulsoup4
playwright install

# Configure your profile
cp config.example.json config.json
# Edit config.json with your details
```

## Usage

```bash
# Scrape jobs
python3 scrapers.py

# Run full pipeline
python3 job_application_bot.py
```

## JupiterHR Job Boards

From https://jupiterhr.ca/remote-job-board:

### Top Job Boards to Scrape:
1. **Wellfound (AngelList)** — Startup tech jobs
2. **RemoteOK** — Remote developer jobs
3. **We Work Remotely** — Curated remote jobs
4. **Remotive** — Remote tech jobs
5. **FlexJobs** — Vetted remote jobs (paid)
6. **LinkedIn** — Professional network
7. **Indeed** — General job search
8. **Authentic Jobs** — Creative + tech
9. **Cybersecurity Jobs** — Security roles
10. **Black Tech Pipeline** — Black tech talent

## Automation Capabilities

✅ **Can Automate:**
- Job scraping from public boards
- Filtering by keywords/location
- Generating cover letters
- Filling standard forms
- Answering common questions
- Tracking applications

⚠️ **Requires Manual:**
- CAPTCHA solving
- Complex multi-step applications
- Video interviews
- Technical assessments
- Phone screens

🚫 **Cannot/Should Not:**
- Violate Terms of Service
- Fake identity information
- Automated interviews
- Automated technical tests

## Safety & Ethics

- Respect rate limits (delay between requests)
- Review applications before submitting
- Don't spam applications
- Follow each site's ToS
- Be honest in AI-generated content

## Next Steps

1. Set up your profile in `config.json`
2. Test scraping on one job board
3. Review generated cover letters
4. Start with "Easy Apply" jobs
5. Track application success rates
