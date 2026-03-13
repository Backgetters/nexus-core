#!/usr/bin/env python3
"""
NEXUS Auto-Apply System for James Ready
Automates job applications with AI-generated responses
"""

import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from james_application_generator import JamesApplicationGenerator

class AutoApplyBot:
    """Automate job applications"""
    
    def __init__(self):
        self.generator = JamesApplicationGenerator()
        self.applied_jobs: List[Dict] = []
        self.application_log = Path(__file__).parent / "data" / "applications_log.jsonl"
    
    def load_jobs(self, jobs_file: str = "data/quick_scrape.json") -> List[Dict]:
        """Load scraped jobs"""
        jobs_path = Path(__file__).parent / jobs_file
        if jobs_path.exists():
            with open(jobs_path) as f:
                data = json.load(f)
                return data.get('jobs', [])
        return []
    
    def filter_easy_apply(self, jobs: List[Dict]) -> List[Dict]:
        """Filter jobs that support easy apply"""
        # For now, assume all scraped jobs need manual application
        # In production, this would check for "Easy Apply" buttons
        easy_apply_sources = ['LinkedIn', 'Wellfound', 'Indeed']
        return [job for job in jobs if job.get('source') in easy_apply_sources]
    
    def prepare_application(self, job: Dict) -> Dict:
        """Prepare application package for a job"""
        print(f"\n📄 Preparing application for:")
        print(f"   {job['title']} @ {job['company']}")
        
        # Generate cover letter
        cover_letter = self.generator.generate_cover_letter(
            job['title'], 
            job['company']
        )
        
        # Generate common answers
        answers = {
            'why_hire': self.generator.answer_question('Why should we hire you?', job['title']),
            'experience': self.generator.answer_question('Describe your experience', job['title']),
            'salary': self.generator.answer_question('What are your salary expectations?', job['title']),
            'remote': self.generator.answer_question('Describe your remote work experience', job['title']),
        }
        
        application = {
            'job': job,
            'cover_letter': cover_letter,
            'answers': answers,
            'prepared_at': datetime.now().isoformat(),
            'status': 'ready_to_apply'
        }
        
        return application
    
    def save_application(self, application: Dict):
        """Save application to file"""
        # Create applications directory
        apps_dir = Path(__file__).parent / "applications" / "pending"
        apps_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        company = application['job']['company'].replace(' ', '_')
        title = application['job']['title'].replace(' ', '_')[:30]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{company}_{title}_{timestamp}"
        
        # Save full application
        app_file = apps_dir / f"{filename}.json"
        with open(app_file, 'w') as f:
            json.dump(application, f, indent=2)
        
        # Save cover letter separately
        cl_file = apps_dir / f"{filename}_cover_letter.txt"
        with open(cl_file, 'w') as f:
            f.write(application['cover_letter'])
        
        # Save answers
        ans_file = apps_dir / f"{filename}_answers.txt"
        with open(ans_file, 'w') as f:
            for question, answer in application['answers'].items():
                f.write(f"Q: {question}\n")
                f.write(f"A: {answer}\n\n")
        
        print(f"   ✅ Saved to: applications/pending/{filename}")
        
        # Log application
        self._log_application(application)
        
        return app_file
    
    def _log_application(self, application: Dict):
        """Log application to tracking file"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'company': application['job']['company'],
            'title': application['job']['title'],
            'source': application['job']['source'],
            'status': 'prepared'
        }
        
        with open(self.application_log, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def run_auto_apply(self, max_jobs: int = 5):
        """Run auto-apply process"""
        print("🚀 NEXUS Auto-Apply System")
        print("="*60)
        print(f"User: James Ready")
        print(f"Target: Data Entry, Remote Dev, Flexible Hours")
        print(f"Max Jobs: {max_jobs}")
        print("="*60)
        
        # 1. Load jobs
        print("\n📂 Loading scraped jobs...")
        jobs = self.load_jobs()
        print(f"   Found {len(jobs)} jobs")
        
        if not jobs:
            print("\n⚠️  No jobs found. Run scraper first:")
            print("   python3 quick_scrape.py")
            return
        
        # 2. Filter for easy apply (if applicable)
        easy_apply_jobs = self.filter_easy_apply(jobs)
        print(f"   {len(easy_apply_jobs)} support Easy Apply")
        
        # 3. Prepare applications
        print(f"\n📝 Preparing up to {max_jobs} applications...")
        prepared = []
        
        for i, job in enumerate(jobs[:max_jobs], 1):
            print(f"\n{i}. {job['title']} @ {job['company']}")
            
            # Check if already applied
            if self._already_applied(job):
                print(f"   ⏭️  Already applied - skipping")
                continue
            
            # Prepare application
            application = self.prepare_application(job)
            app_file = self.save_application(application)
            prepared.append(application)
            
            print(f"   ✅ Ready to apply")
        
        # 4. Summary
        print(f"\n{'='*60}")
        print(f"✅ PREPARED {len(prepared)} APPLICATIONS")
        print(f"{'='*60}")
        print(f"\n📁 Applications saved in:")
        print(f"   jobs/applications/pending/")
        print(f"\n📊 Next steps:")
        print(f"   1. Review applications in pending folder")
        print(f"   2. Customize if needed")
        print(f"   3. Submit manually or run auto-submit")
        print(f"\n📈 Application log:")
        print(f"   {self.application_log}")
        
        return prepared
    
    def _already_applied(self, job: Dict) -> bool:
        """Check if already applied to this job"""
        if not self.application_log.exists():
            return False
        
        job_key = f"{job['title']}-{job['company']}"
        
        with open(self.application_log) as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    entry_key = f"{entry['title']}-{entry['company']}"
                    if entry_key == job_key:
                        return True
                except:
                    continue
        
        return False
    
    def show_stats(self):
        """Show application statistics"""
        if not self.application_log.exists():
            print("No applications yet.")
            return
        
        stats = {'prepared': 0, 'submitted': 0, 'rejected': 0, 'interview': 0}
        companies = set()
        
        with open(self.application_log) as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    stats[entry.get('status', 'prepared')] += 1
                    companies.add(entry['company'])
                except:
                    continue
        
        print("📊 Application Statistics")
        print("="*40)
        print(f"Total Applications: {sum(stats.values())}")
        print(f"Prepared: {stats['prepared']}")
        print(f"Submitted: {stats['submitted']}")
        print(f"Interviews: {stats['interview']}")
        print(f"Companies: {len(companies)}")

if __name__ == "__main__":
    bot = AutoApplyBot()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'stats':
            bot.show_stats()
        elif sys.argv[1] == 'apply':
            max_jobs = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            bot.run_auto_apply(max_jobs)
    else:
        # Default: prepare 5 applications
        bot.run_auto_apply(5)
