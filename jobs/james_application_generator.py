#!/usr/bin/env python3
"""
James Ready Job Application Generator
Creates tailored applications for data entry and remote dev roles
"""

import json
from datetime import datetime
from pathlib import Path

class JamesApplicationGenerator:
    """Generate job applications for James Ready"""
    
    def __init__(self):
        self.profile = self._load_profile()
    
    def _load_profile(self) -> dict:
        """Load James's profile"""
        profile_path = Path(__file__).parent / "config" / "james_profile.json"
        with open(profile_path) as f:
            return json.load(f)
    
    def generate_cover_letter(self, job_title: str, company: str, job_type: str = "data_entry") -> str:
        """Generate tailored cover letter"""
        
        if "data" in job_title.lower() or "entry" in job_title.lower():
            return self._data_entry_cover_letter(job_title, company)
        else:
            return self._developer_cover_letter(job_title, company)
    
    def _data_entry_cover_letter(self, job_title: str, company: str) -> str:
        """Cover letter for data entry roles"""
        return f"""Dear Hiring Manager,

I am writing to express my interest in the {job_title} position at {company}. As a detail-oriented professional with experience in data processing and automation, I am confident I can contribute effectively to your team.

**Why I'm a great fit:**
• Fast and accurate data entry skills (typing speed: 70+ WPM)
• Proficient with Excel, Google Sheets, and data management tools
• Experience automating repetitive tasks using Python and AI tools
• Highly organized with strong attention to detail
• Comfortable working independently across different time zones
• Flexible schedule - available 40+ hours per week

**What I bring:**
I leverage technology to work efficiently. Using AI tools and automation scripts, I can process large volumes of data quickly while maintaining accuracy. I'm a fast learner who adapts quickly to new software and workflows.

**Availability:**
I am available to start immediately and can work flexible hours across any time zone. I have a dedicated workspace, high-speed internet, and all necessary equipment.

I would welcome the opportunity to discuss how I can support {company}'s data needs. Thank you for considering my application.

Best regards,
{self.profile['name']}
{self.profile['email']}

---
*References available upon request*
"""
    
    def _developer_cover_letter(self, job_title: str, company: str) -> str:
        """Cover letter for developer roles"""
        return f"""Dear Hiring Manager,

I am excited to apply for the {job_title} position at {company}. As a self-taught developer with hands-on experience building automation systems and working with AI tools, I bring a unique combination of technical skills and practical problem-solving ability.

**Technical Skills:**
• Python (automation, web scraping, data processing)
• JavaScript and web development
• API integration and automation
• Git version control
• SQL databases
• AI/ML tools (ChatGPT, Claude, OpenClaw)

**Recent Projects:**
• Built automated job application system using Python and Playwright
• Created trading bot with risk management and monitoring
• Developed multi-agent AI systems for business automation
• Implemented data pipelines for processing and analysis

**Why Remote Work Suits Me:**
I am highly self-motivated and thrive in independent work environments. I have experience collaborating across time zones and am comfortable with asynchronous communication. My flexible schedule allows me to be available when needed.

**What I Offer:**
I don't just write code—I solve problems. I leverage AI tools to accelerate development while maintaining code quality. I'm a fast learner who can quickly adapt to your tech stack and workflows.

I am available to start immediately and can work 40+ hours per week across any time zone. I would love to discuss how I can contribute to {company}'s development team.

Thank you for your consideration.

Best regards,
{self.profile['name']}
{self.profile['email']}
LinkedIn: {self.profile['linkedin']}

---
*Portfolio and references available upon request*
"""
    
    def answer_question(self, question: str, job_title: str = "") -> str:
        """Generate answer for common application questions"""
        
        q_lower = question.lower()
        
        # Salary expectations
        if any(word in q_lower for word in ['salary', 'compensation', 'pay', 'rate']):
            return self.profile.get('salary_expectation', 'Negotiable based on role and responsibilities')
        
        # Why hire you
        if any(word in q_lower for word in ['why hire', 'why you', 'why should', 'what makes']):
            if 'data' in job_title.lower():
                return "I combine fast, accurate data entry skills with automation expertise. I use AI tools to work more efficiently than traditional data entry clerks, ensuring high accuracy while handling larger volumes. I'm reliable, detail-oriented, and available for flexible hours across time zones."
            else:
                return "I bring a unique mix of development skills and AI tool proficiency. I can write clean code while leveraging AI to accelerate development. I'm self-motivated, a fast learner, and comfortable working independently across time zones."
        
        # Experience
        if any(word in q_lower for word in ['experience', 'background', 'qualifications']):
            return f"I have {self.profile['years_experience']} years of experience in software development and automation. I've built systems for trading, job applications, and business automation. I'm proficient in Python, JavaScript, and various AI tools. I learn quickly and adapt to new technologies."
        
        # Remote work
        if any(word in q_lower for word in ['remote', 'work from home', 'timezone', 'flexible']):
            return "I have a dedicated home office with high-speed internet and all necessary equipment. I'm comfortable working across time zones and can adjust my schedule as needed. I'm highly self-motivated and experienced with asynchronous communication tools."
        
        # Availability
        if any(word in q_lower for word in ['availability', 'when can', 'start date', 'hours']):
            return "I am available to start immediately and can commit to 40+ hours per week. My schedule is flexible—I can work any time zone and adjust hours based on project needs."
        
        # Skills
        if any(word in q_lower for word in ['skills', 'proficient', 'tools', 'software']):
            skills_text = ", ".join(self.profile['skills'][:10])
            return f"My key skills include: {skills_text}. I'm also a fast learner who quickly adapts to new tools and workflows."
        
        # Strengths/weaknesses
        if 'strength' in q_lower:
            return "My strengths include: fast learning ability, attention to detail, self-motivation, and tech-savviness. I leverage AI tools to work efficiently and solve problems creatively."
        
        if 'weakness' in q_lower:
            return "I tend to be a perfectionist, which means I sometimes spend extra time ensuring work is done right. I've learned to balance this with deadlines by setting internal milestones."
        
        # Default response
        return f"Based on my experience with {', '.join(self.profile['skills'][:5])}, I am confident I can excel in this role. I'm a quick learner, highly motivated, and excited about the opportunity to contribute to your team."
    
    def generate_resume_summary(self) -> str:
        """Generate resume summary section"""
        return """Results-driven professional with expertise in data processing, automation, and software development. 
Proficient in leveraging AI tools and Python to optimize workflows and increase efficiency. 
Highly self-motivated with proven ability to work independently across time zones. 
Seeking remote opportunities with flexible hours."""
    
    def save_application_package(self, job_title: str, company: str, output_dir: str = "applications"):
        """Save complete application package"""
        output_path = Path(__file__).parent / output_dir
        output_path.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{company.replace(' ', '_')}_{timestamp}"
        
        package = {
            'job_title': job_title,
            'company': company,
            'cover_letter': self.generate_cover_letter(job_title, company),
            'resume_summary': self.generate_resume_summary(),
            'profile': self.profile,
            'generated_at': datetime.now().isoformat()
        }
        
        # Save as JSON
        json_path = output_path / f"{filename}.json"
        with open(json_path, 'w') as f:
            json.dump(package, f, indent=2)
        
        # Save cover letter as text
        txt_path = output_path / f"{filename}_cover_letter.txt"
        with open(txt_path, 'w') as f:
            f.write(package['cover_letter'])
        
        print(f"✅ Application package saved:")
        print(f"   📄 {json_path}")
        print(f"   📝 {txt_path}")
        
        return package

if __name__ == "__main__":
    generator = JamesApplicationGenerator()
    
    # Example: Generate application for data entry role
    print("="*60)
    print("SAMPLE APPLICATIONS")
    print("="*60)
    
    print("\n1️⃣ DATA ENTRY ROLE:")
    print(generator.generate_cover_letter("Data Entry Specialist", "TechCorp Inc", "data_entry"))
    
    print("\n" + "="*60)
    print("\n2️⃣ DEVELOPER ROLE:")
    print(generator.generate_cover_letter("Junior Python Developer", "StartupXYZ", "developer"))
    
    print("\n" + "="*60)
    print("\n3️⃣ SAMPLE ANSWERS:")
    questions = [
        "Why should we hire you?",
        "What is your salary expectation?",
        "Describe your experience with remote work",
        "When can you start?"
    ]
    
    for q in questions:
        print(f"\nQ: {q}")
        print(f"A: {generator.answer_question(q)}")
    
    # Save sample package
    print("\n" + "="*60)
    generator.save_application_package("Data Entry Specialist", "Sample Company")
