#!/usr/bin/env python3
"""
Quick Job Scraper - Test Version
Scrapes 2-3 jobs from each source quickly
"""

import asyncio
import json
from datetime import datetime
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def quick_scrape():
    """Quick scrape for demo"""
    jobs = []
    
    print("🔍 Quick Job Search for James Ready\n")
    print("="*60)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # 1. RemoteOK
        print("\n1️⃣ Checking RemoteOK...")
        try:
            page = await browser.new_page()
            await page.goto("https://remoteok.io/remote-dev-jobs", timeout=30000)
            await asyncio.sleep(2)
            
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            job_rows = soup.find_all('tr', class_='job')[:3]
            
            for row in job_rows:
                title = row.find('h2', itemprop='title')
                company = row.find('h3', itemprop='name')
                if title and company:
                    jobs.append({
                        'title': title.text.strip(),
                        'company': company.text.strip(),
                        'source': 'RemoteOK',
                        'type': 'remote'
                    })
            print(f"   ✅ Found {len(job_rows)} jobs")
            await page.close()
        except Exception as e:
            print(f"   ⚠️  {e}")
        
        # 2. We Work Remotely
        print("\n2️⃣ Checking We Work Remotely...")
        try:
            page = await browser.new_page()
            await page.goto("https://weworkremotely.com", timeout=30000)
            await asyncio.sleep(2)
            
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            listings = soup.find_all('li', class_='feature')[:3]
            
            for listing in listings:
                title = listing.find('span', class_='title')
                company = listing.find('span', class_='company')
                if title and company:
                    jobs.append({
                        'title': title.text.strip(),
                        'company': company.text.strip(),
                        'source': 'WeWorkRemotely',
                        'type': 'remote'
                    })
            print(f"   ✅ Found {len(listings)} jobs")
            await page.close()
        except Exception as e:
            print(f"   ⚠️  {e}")
        
        # 3. Remotive
        print("\n3️⃣ Checking Remotive...")
        try:
            page = await browser.new_page()
            await page.goto("https://remotive.io/remote-jobs", timeout=30000)
            await asyncio.sleep(2)
            
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            cards = soup.find_all('li', class_='job-list-item')[:3]
            
            for card in cards:
                title = card.find('h3')
                company = card.find('span', class_='company')
                if title and company:
                    jobs.append({
                        'title': title.text.strip(),
                        'company': company.text.strip(),
                        'source': 'Remotive',
                        'type': 'remote'
                    })
            print(f"   ✅ Found {len(cards)} jobs")
            await page.close()
        except Exception as e:
            print(f"   ⚠️  {e}")
        
        await browser.close()
    
    # Save results
    output = {
        'scraped_at': datetime.now().isoformat(),
        'total_jobs': len(jobs),
        'jobs': jobs
    }
    
    with open('/Users/tomegathericon/clawd/jobs/data/quick_scrape.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"✅ TOTAL: {len(jobs)} jobs found")
    print(f"💾 Saved to: jobs/data/quick_scrape.json")
    print(f"{'='*60}\n")
    
    print("📋 SAMPLE JOBS:")
    for i, job in enumerate(jobs[:5], 1):
        print(f"{i}. {job['title']} @ {job['company']} ({job['source']})")
    
    return jobs

if __name__ == "__main__":
    jobs = asyncio.run(quick_scrape())
