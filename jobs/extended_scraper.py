#!/usr/bin/env python3
"""
Extended Job Board Scraper for James Ready
Adds: Indeed, LinkedIn, FlexJobs, AngelList/Wellfound
"""

import asyncio
import json
import time
from datetime import datetime
from typing import List, Dict, Optional
from playwright.async_api import async_playwright, Page
from bs4 import BeautifulSoup

class ExtendedJobScraper:
    """Extended scraper with more job boards"""
    
    def __init__(self):
        self.jobs: List[Dict] = []
        self.seen_jobs = set()  # Deduplication
    
    async def scrape_indeed(self, query: str = "data entry remote", location: str = "Remote") -> List[Dict]:
        """Scrape Indeed for remote jobs"""
        jobs = []
        url = f"https://www.indeed.com/jobs?q={query.replace(' ', '+')}&l={location}&remotejob=032b3046-06a5-11ea-8e8f-3f75aa459a0c"
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                await page.goto(url, wait_until="networkidle")
                await asyncio.sleep(3)
                
                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
                # Indeed job cards
                job_cards = soup.find_all('div', {'data-testid': 'job-title'})
                
                for card in job_cards[:20]:  # Limit to 20
                    try:
                        # Navigate up to find the full job container
                        container = card.find_parent('div', class_='job_seen_beacon') or card.find_parent('td')
                        if not container:
                            continue
                        
                        title = card.get_text(strip=True)
                        
                        company_elem = container.find(['span', 'a'], {'data-testid': 'company-name'})
                        company = company_elem.get_text(strip=True) if company_elem else "Unknown"
                        
                        # Deduplication
                        job_key = f"{title}-{company}"
                        if job_key in self.seen_jobs:
                            continue
                        self.seen_jobs.add(job_key)
                        
                        if self._is_match(title):
                            jobs.append({
                                'title': title,
                                'company': company,
                                'location': location,
                                'source': 'Indeed',
                                'url': f"https://www.indeed.com/viewjob?jk={container.get('data-jk', '')}",
                                'job_type': 'remote',
                                'flexible': True,
                                'scraped_at': datetime.now().isoformat()
                            })
                    except Exception as e:
                        continue
                        
            finally:
                await browser.close()
        
        print(f"   ✅ Indeed: {len(jobs)} jobs")
        return jobs
    
    async def scrape_linkedin(self, keywords: List[str] = None) -> List[Dict]:
        """Scrape LinkedIn jobs (limited without auth)"""
        jobs = []
        
        if keywords is None:
            keywords = ["data entry", "remote developer", "python"]
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                for keyword in keywords[:2]:  # Limit keywords
                    url = f"https://www.linkedin.com/jobs/search?keywords={keyword.replace(' ', '%20')}&location=Remote"
                    
                    await page.goto(url, wait_until="networkidle")
                    await asyncio.sleep(3)
                    
                    content = await page.content()
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # LinkedIn job cards
                    job_cards = soup.find_all('div', class_='base-card')
                    
                    for card in job_cards[:10]:  # Limit per keyword
                        try:
                            title_elem = card.find('h3', class_='base-search-card__title')
                            company_elem = card.find('h4', class_='base-search-card__subtitle')
                            
                            if title_elem and company_elem:
                                title = title_elem.get_text(strip=True)
                                company = company_elem.get_text(strip=True)
                                
                                job_key = f"{title}-{company}"
                                if job_key in self.seen_jobs:
                                    continue
                                self.seen_jobs.add(job_key)
                                
                                if self._is_match(title):
                                    link_elem = card.find('a', class_='base-card__full-link')
                                    jobs.append({
                                        'title': title,
                                        'company': company,
                                        'location': 'Remote',
                                        'source': 'LinkedIn',
                                        'url': link_elem['href'] if link_elem else '',
                                        'job_type': 'remote',
                                        'flexible': True,
                                        'scraped_at': datetime.now().isoformat()
                                    })
                        except:
                            continue
                    
                    # Rate limiting
                    await asyncio.sleep(2)
                    
            finally:
                await browser.close()
        
        print(f"   ✅ LinkedIn: {len(jobs)} jobs")
        return jobs
    
    async def scrape_angellist(self) -> List[Dict]:
        """Scrape Wellfound (AngelList) for startup jobs"""
        jobs = []
        url = "https://wellfound.com/jobs"
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                await page.goto(url, wait_until="networkidle")
                await asyncio.sleep(3)
                
                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
                # Wellfound job cards
                job_cards = soup.find_all('div', class_='job-listing')
                
                for card in job_cards[:15]:
                    try:
                        title_elem = card.find('h2') or card.find('a', class_='title')
                        company_elem = card.find('span', class_='company') or card.find('h3')
                        
                        if title_elem and company_elem:
                            title = title_elem.get_text(strip=True)
                            company = company_elem.get_text(strip=True)
                            
                            job_key = f"{title}-{company}"
                            if job_key in self.seen_jobs:
                                continue
                            self.seen_jobs.add(job_key)
                            
                            if self._is_match(title):
                                jobs.append({
                                    'title': title,
                                    'company': company,
                                    'location': 'Remote',
                                    'source': 'Wellfound (AngelList)',
                                    'url': title_elem['href'] if title_elem.name == 'a' else '',
                                    'job_type': 'remote',
                                    'flexible': True,
                                    'startup': True,
                                    'scraped_at': datetime.now().isoformat()
                                })
                    except:
                        continue
                        
            finally:
                await browser.close()
        
        print(f"   ✅ Wellfound: {len(jobs)} jobs")
        return jobs
    
    async def scrape_flexjobs(self) -> List[Dict]:
        """Scrape FlexJobs (limited without subscription)"""
        jobs = []
        # FlexJobs requires login for full access
        # This is a placeholder for the structure
        print("   ⚠️  FlexJobs: Requires subscription for full access")
        return jobs
    
    async def scrape_remotive(self) -> List[Dict]:
        """Scrape Remotive.io"""
        jobs = []
        url = "https://remotive.io/remote-jobs"
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                await page.goto(url, wait_until="networkidle")
                await asyncio.sleep(3)
                
                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
                job_cards = soup.find_all('li', class_='job-list-item')
                
                for card in job_cards[:15]:
                    try:
                        title_elem = card.find('h3')
                        company_elem = card.find('span', class_='company')
                        
                        if title_elem and company_elem:
                            title = title_elem.get_text(strip=True)
                            company = company_elem.get_text(strip=True)
                            
                            job_key = f"{title}-{company}"
                            if job_key in self.seen_jobs:
                                continue
                            self.seen_jobs.add(job_key)
                            
                            if self._is_match(title):
                                jobs.append({
                                    'title': title,
                                    'company': company,
                                    'location': 'Remote',
                                    'source': 'Remotive',
                                    'url': card.find('a')['href'] if card.find('a') else '',
                                    'job_type': 'remote',
                                    'flexible': True,
                                    'scraped_at': datetime.now().isoformat()
                                })
                    except:
                        continue
                        
            finally:
                await browser.close()
        
        print(f"   ✅ Remotive: {len(jobs)} jobs")
        return jobs
    
    def _is_match(self, title: str) -> bool:
        """Check if job title matches James's criteria"""
        title_lower = title.lower()
        
        # Must-have keywords
        must_have = [
            'data entry', 'data processing', 'data analyst', 'data coordinator',
            'software', 'developer', 'programmer', 'engineer', 'programming',
            'python', 'automation', 'AI', 'virtual assistant', 'administrative',
            'entry level', 'junior', 'beginner', 'associate', 'assistant',
            'remote', 'work from home', 'wfh', 'virtual'
        ]
        
        has_match = any(keyword in title_lower for keyword in must_have)
        
        # Exclude senior roles
        exclude = [
            'senior', 'lead', 'principal', 'architect', 'staff',
            'manager', 'director', 'head of', 'vp', 'chief',
            '5+ years', '7+ years', '10+ years', 'staff engineer'
        ]
        
        has_exclude = any(exc in title_lower for exc in exclude)
        
        return has_match and not has_exclude
    
    async def scrape_all(self) -> Dict[str, List[Dict]]:
        """Scrape all job boards"""
        print("🔍 Extended Job Search for James Ready")
        print("   Target: Data Entry, Remote Dev, Flexible Hours\n")
        print("="*60)
        
        results = {}
        
        # Scrape each board
        print("\n1️⃣ Scraping Indeed...")
        results['indeed'] = await self.scrape_indeed()
        
        print("\n2️⃣ Scraping LinkedIn...")
        results['linkedin'] = await self.scrape_linkedin()
        
        print("\n3️⃣ Scraping Wellfound (AngelList)...")
        results['angellist'] = await self.scrape_angellist()
        
        print("\n4️⃣ Scraping Remotive...")
        results['remotive'] = await self.scrape_remotive()
        
        print("\n5️⃣ Scraping FlexJobs...")
        results['flexjobs'] = await self.scrape_flexjobs()
        
        # Save results
        output_file = '/Users/tomegathericon/clawd/jobs/data/james_all_jobs.json'
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        # Summary
        total = sum(len(jobs) for jobs in results.values())
        print(f"\n{'='*60}")
        print(f"✅ TOTAL JOBS FOUND: {total}")
        print(f"💾 Saved to: {output_file}")
        print(f"{'='*60}\n")
        
        # Show top matches
        if total > 0:
            print("📋 TOP MATCHES BY SOURCE:")
            for source, jobs in results.items():
                if jobs:
                    print(f"\n{source.upper()} ({len(jobs)} jobs):")
                    for job in jobs[:3]:
                        print(f"   • {job['title']}")
                    if len(jobs) > 3:
                        print(f"   ... and {len(jobs)-3} more")
        
        return results

if __name__ == "__main__":
    scraper = ExtendedJobScraper()
    results = asyncio.run(scraper.scrape_all())
