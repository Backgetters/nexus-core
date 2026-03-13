#!/usr/bin/env python3
"""
Job Board Scraper Implementations
Uses Playwright for JavaScript-heavy sites
"""

import asyncio
import json
from datetime import datetime
from typing import List, Dict
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

class RemoteOKScraper:
    """Scrape RemoteOK job board"""
    
    URL = "https://remoteok.io/remote-{}-jobs"
    
    async def scrape(self, keyword: str = "dev") -> List[Dict]:
        jobs = []
        url = self.URL.format(keyword)
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                await page.goto(url, wait_until="networkidle")
                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
                # RemoteOK uses specific class names
                job_rows = soup.find_all('tr', class_='job')
                
                for row in job_rows:
                    try:
                        title_elem = row.find('h2', itemprop='title')
                        company_elem = row.find('h3', itemprop='name')
                        
                        if title_elem and company_elem:
                            jobs.append({
                                'title': title_elem.text.strip(),
                                'company': company_elem.text.strip(),
                                'location': 'Remote',
                                'url': 'https://remoteok.io' + row.find('a')['href'] if row.find('a') else '',
                                'source': 'RemoteOK',
                                'scraped_at': datetime.now().isoformat()
                            })
                    except Exception as e:
                        continue
                        
            finally:
                await browser.close()
        
        return jobs

class WeWorkRemotelyScraper:
    """Scrape We Work Remotely job board"""
    
    URL = "https://weworkremotely.com/remote-jobs/search?term={}"
    
    async def scrape(self, keyword: str = "developer") -> List[Dict]:
        jobs = []
        url = self.URL.format(keyword)
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                await page.goto(url, wait_until="networkidle")
                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
                # WWR uses article tags for jobs
                job_listings = soup.find_all('li', class_='feature')
                
                for listing in job_listings:
                    try:
                        title_elem = listing.find('span', class_='title')
                        company_elem = listing.find('span', class_='company')
                        
                        if title_elem and company_elem:
                            link = listing.find('a')
                            jobs.append({
                                'title': title_elem.text.strip(),
                                'company': company_elem.text.strip(),
                                'location': 'Remote',
                                'url': 'https://weworkremotely.com' + link['href'] if link else '',
                                'source': 'WeWorkRemotely',
                                'scraped_at': datetime.now().isoformat()
                            })
                    except Exception as e:
                        continue
                        
            finally:
                await browser.close()
        
        return jobs

class LinkedInJobScraper:
    """Scrape LinkedIn jobs (requires authentication)"""
    
    URL = "https://www.linkedin.com/jobs/search"
    
    async def scrape(self, keywords: List[str], location: str = "Remote") -> List[Dict]:
        """Note: Requires LinkedIn login for full functionality"""
        jobs = []
        
        # LinkedIn scraping is more complex due to auth requirements
        # This is a placeholder for the structure
        
        return jobs

class IndeedScraper:
    """Scrape Indeed job board"""
    
    URL = "https://www.indeed.com/jobs"
    
    async def scrape(self, query: str, location: str = "Remote") -> List[Dict]:
        jobs = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                search_url = f"{self.URL}?q={query}&l={location}&remotejob=032b3046-06a5-11ea-8e8f-3f75aa459a0c"
                await page.goto(search_url, wait_until="networkidle")
                
                # Indeed uses specific data attributes
                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
                job_cards = soup.find_all('div', class_='job_seen_beacon')
                
                for card in job_cards:
                    try:
                        title_elem = card.find('h2', class_='jobTitle')
                        company_elem = card.find('span', {'data-testid': 'company-name'})
                        
                        if title_elem and company_elem:
                            jobs.append({
                                'title': title_elem.text.strip(),
                                'company': company_elem.text.strip(),
                                'location': location,
                                'source': 'Indeed',
                                'scraped_at': datetime.now().isoformat()
                            })
                    except:
                        continue
                        
            finally:
                await browser.close()
        
        return jobs

async def scrape_all_job_boards(keywords: List[str] = None) -> Dict[str, List[Dict]]:
    """Scrape multiple job boards"""
    if keywords is None:
        keywords = ["software engineer", "full stack developer", "AI engineer"]
    
    results = {}
    
    # Scrape RemoteOK
    print("🔍 Scraping RemoteOK...")
    remoteok = RemoteOKScraper()
    results['remoteok'] = await remoteok.scrape("developer")
    print(f"   Found {len(results['remoteok'])} jobs")
    
    # Scrape We Work Remotely
    print("🔍 Scraping We Work Remotely...")
    wwr = WeWorkRemotelyScraper()
    results['weworkremotely'] = await wwr.scrape("developer")
    print(f"   Found {len(results['weworkremotely'])} jobs")
    
    # Save results
    with open('/Users/tomegathericon/clawd/jobs/data/scraped_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    return results

if __name__ == "__main__":
    results = asyncio.run(scrape_all_job_boards())
    
    total = sum(len(jobs) for jobs in results.values())
    print(f"\n✅ Total jobs scraped: {total}")
    print(f"💾 Saved to: /Users/tomegathericon/clawd/jobs/data/scraped_results.json")
