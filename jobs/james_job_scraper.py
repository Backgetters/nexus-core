#!/usr/bin/env python3
"""
Specialized Job Scraper for James Ready
Focus: Data Entry, Remote Software Dev, Flexible Hours, Multi-Timezone
"""

import asyncio
import json
from datetime import datetime
from typing import List, Dict
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

class DataEntryJobScraper:
    """Scrape data entry and remote jobs"""
    
    TARGET_BOARDS = {
        "remoteok_dev": "https://remoteok.io/remote-dev-jobs",
        "remoteok_data": "https://remoteok.io/remote-data-jobs",
        "weworkremotely": "https://weworkremotely.com",
        "remotive": "https://remotive.io/remote-jobs",
        "flexjobs_data": "https://www.flexjobs.com/search?search=data+entry",
        "indeed_remote": "https://www.indeed.com/jobs?q=data+entry+remote",
    }
    
    KEYWORDS = [
        "data entry",
        "data processing",
        "remote developer",
        "software developer",
        "python developer",
        "automation",
        "AI developer",
        "flexible",
        "work from home",
        "virtual assistant",
        "entry level developer",
        "junior developer"
    ]
    
    async def scrape_remoteok(self) -> List[Dict]:
        """Scrape RemoteOK for dev and data jobs"""
        jobs = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                # Try developer jobs first
                await page.goto(self.TARGET_BOARDS["remoteok_dev"], wait_until="networkidle")
                await asyncio.sleep(2)
                
                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
                job_rows = soup.find_all('tr', class_='job')
                
                for row in job_rows:
                    try:
                        title_elem = row.find('h2', itemprop='title')
                        company_elem = row.find('h3', itemprop='name')
                        tags = row.find_all('div', class_='tag')
                        
                        if title_elem and company_elem:
                            title = title_elem.text.strip()
                            company = company_elem.text.strip()
                            
                            # Check if it's a match
                            if self._is_match(title):
                                job_tags = [tag.text.strip() for tag in tags]
                                
                                jobs.append({
                                    'title': title,
                                    'company': company,
                                    'location': 'Remote',
                                    'tags': job_tags,
                                    'url': 'https://remoteok.io' + row.find('a')['href'] if row.find('a') else '',
                                    'source': 'RemoteOK',
                                    'job_type': 'remote',
                                    'flexible': 'flexible' in ' '.join(job_tags).lower() or True,
                                    'scraped_at': datetime.now().isoformat()
                                })
                    except:
                        continue
                        
            finally:
                await browser.close()
        
        return jobs
    
    async def scrape_weworkremotely(self) -> List[Dict]:
        """Scrape We Work Remotely"""
        jobs = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                await page.goto(self.TARGET_BOARDS["weworkremotely"], wait_until="networkidle")
                await asyncio.sleep(2)
                
                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
                # Find all job sections
                sections = soup.find_all('section', class_='jobs')
                
                for section in sections:
                    category = section.find('h2')
                    category_name = category.text.strip() if category else "General"
                    
                    # Focus on programming and data categories
                    if any(keyword in category_name.lower() for keyword in ['programming', 'dev', 'data', 'tech']):
                        job_listings = section.find_all('li', class_='feature')
                        
                        for listing in job_listings:
                            try:
                                title_elem = listing.find('span', class_='title')
                                company_elem = listing.find('span', class_='company')
                                
                                if title_elem and company_elem:
                                    title = title_elem.text.strip()
                                    
                                    if self._is_match(title):
                                        link = listing.find('a')
                                        jobs.append({
                                            'title': title,
                                            'company': company_elem.text.strip(),
                                            'location': 'Remote',
                                            'category': category_name,
                                            'url': 'https://weworkremotely.com' + link['href'] if link else '',
                                            'source': 'WeWorkRemotely',
                                            'job_type': 'remote',
                                            'flexible': True,
                                            'scraped_at': datetime.now().isoformat()
                                        })
                            except:
                                continue
                        
            finally:
                await browser.close()
        
        return jobs
    
    async def scrape_remotive(self) -> List[Dict]:
        """Scrape Remotive job board"""
        jobs = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                await page.goto(self.TARGET_BOARDS["remotive"], wait_until="networkidle")
                await asyncio.sleep(2)
                
                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
                # Remotive uses specific class structure
                job_cards = soup.find_all('div', class_='job-list-item')
                
                for card in job_cards:
                    try:
                        title_elem = card.find('h3')
                        company_elem = card.find('span', class_='company')
                        
                        if title_elem and company_elem:
                            title = title_elem.text.strip()
                            
                            if self._is_match(title):
                                jobs.append({
                                    'title': title,
                                    'company': company_elem.text.strip(),
                                    'location': 'Remote',
                                    'url': card.find('a')['href'] if card.find('a') else '',
                                    'source': 'Remotive',
                                    'job_type': 'remote',
                                    'flexible': True,
                                    'scraped_at': datetime.now().isoformat()
                                })
                    except:
                        continue
                        
            finally:
                await browser.close()
        
        return jobs
    
    def _is_match(self, title: str) -> bool:
        """Check if job title matches desired roles"""
        title_lower = title.lower()
        
        # Must-have keywords (at least one)
        must_have = [
            'data entry', 'data processing', 'data analyst',
            'software', 'developer', 'programmer', 'engineer',
            'python', 'automation', 'AI', 'virtual assistant',
            'entry level', 'junior', 'beginner'
        ]
        
        # Check for must-have
        has_match = any(keyword in title_lower for keyword in must_have)
        
        # Exclude these
        exclude = [
            'senior', 'lead', 'principal', 'architect',
            'manager', 'director', 'head of', '5+ years',
            '10+ years', 'staff engineer'
        ]
        
        has_exclude = any(exc in title_lower for exc in exclude)
        
        return has_match and not has_exclude
    
    async def scrape_all(self) -> Dict[str, List[Dict]]:
        """Scrape all target job boards"""
        print("🔍 Starting job search for James Ready...")
        print("   Target: Data Entry, Remote Dev, Flexible Hours\n")
        
        results = {}
        
        # Scrape each board
        print("1️⃣ Scraping RemoteOK...")
        results['remoteok'] = await self.scrape_remoteok()
        print(f"   ✅ Found {len(results['remoteok'])} matching jobs")
        
        print("\n2️⃣ Scraping We Work Remotely...")
        results['weworkremotely'] = await self.scrape_weworkremotely()
        print(f"   ✅ Found {len(results['weworkremotely'])} matching jobs")
        
        print("\n3️⃣ Scraping Remotive...")
        results['remotive'] = await self.scrape_remotive()
        print(f"   ✅ Found {len(results['remotive'])} matching jobs")
        
        # Save results
        output_file = '/Users/tomegathericon/clawd/jobs/data/james_job_matches.json'
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        # Summary
        total = sum(len(jobs) for jobs in results.values())
        print(f"\n{'='*50}")
        print(f"✅ TOTAL MATCHING JOBS: {total}")
        print(f"💾 Saved to: {output_file}")
        print(f"{'='*50}\n")
        
        # Show sample
        if total > 0:
            print("📋 SAMPLE JOBS:")
            for source, jobs in results.items():
                if jobs:
                    print(f"\n{source.upper()}:")
                    for job in jobs[:3]:
                        print(f"   • {job['title']} @ {job['company']}")
        
        return results

if __name__ == "__main__":
    scraper = DataEntryJobScraper()
    results = asyncio.run(scraper.scrape_all())
