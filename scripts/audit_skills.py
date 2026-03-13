#!/usr/bin/env python3
"""
NEXUS Skills Inventory & Optimization Tracker
Audits 1161 skills and identifies high-value additions
"""

import json
import os
from pathlib import Path
from collections import defaultdict

SKILLS_DIR = Path.home() / ".openclaw" / "skills"
INVENTORY_FILE = Path(__file__).parent / "data" / "skills_inventory.json"

def categorize_skill(name: str) -> str:
    """Categorize skill by name patterns"""
    name_lower = name.lower()
    
    categories = {
        "ai-ml": ["ai", "ml", "gpt", "claude", "openai", "anthropic", "llm", "model"],
        "automation": ["auto", "bot", "workflow", "cron", "schedule", "task"],
        "business": ["business", "corp", "enterprise", "company", "org"],
        "communication": ["slack", "discord", "telegram", "email", "message", "chat"],
        "data": ["data", "database", "sql", "analytics", "csv", "excel"],
        "deployment": ["deploy", "docker", "k8s", "kubernetes", "hosting", "server"],
        "devops": ["devops", "ci", "cd", "pipeline", "git", "github"],
        "finance": ["finance", "accounting", "tax", "payroll", "invoice", "money"],
        "hr": ["hr", "hiring", "recruit", "employee", "team", "people"],
        "infrastructure": ["infra", "cloud", "aws", "azure", "gcp", "terraform"],
        "legal": ["legal", "compliance", "contract", "law", "gdpr", "hipaa"],
        "marketing": ["marketing", "seo", "ads", "social", "content"],
        "monitoring": ["monitor", "alert", "log", "track", "health"],
        "productivity": ["productivity", "todo", "task", "calendar", "note"],
        "research": ["research", "scrape", "crawl", "search", "intel"],
        "sales": ["sales", "crm", "lead", "prospect", "deal"],
        "security": ["security", "vault", "password", "encrypt", "auth"],
        "voice": ["voice", "audio", "tts", "speech", "transcribe"],
        "web": ["web", "html", "css", "scraping", "browser"],
    }
    
    for category, keywords in categories.items():
        if any(kw in name_lower for kw in keywords):
            return category
    
    return "other"

def audit_skills():
    """Audit all installed skills"""
    print("🔍 Auditing NEXUS Skills Inventory")
    print("="*50)
    
    if not SKILLS_DIR.exists():
        print(f"❌ Skills directory not found: {SKILLS_DIR}")
        return
    
    skills = [d.name for d in SKILLS_DIR.iterdir() if d.is_dir() and not d.name.startswith('.')]
    
    print(f"\n📊 Total Skills: {len(skills)}")
    
    # Categorize
    categories = defaultdict(list)
    for skill in skills:
        cat = categorize_skill(skill)
        categories[cat].append(skill)
    
    # Print breakdown
    print("\n📁 Categories:")
    for cat in sorted(categories.keys()):
        count = len(categories[cat])
        print(f"  {cat:20s}: {count:4d} skills")
    
    # Top categories
    print("\n🏆 Top 5 Categories:")
    sorted_cats = sorted(categories.items(), key=lambda x: len(x[1]), reverse=True)[:5]
    for cat, skill_list in sorted_cats:
        print(f"  {cat}: {len(skill_list)} skills")
        # Show sample
        samples = skill_list[:3]
        for s in samples:
            print(f"    - {s}")
    
    # Save inventory
    inventory = {
        "total": len(skills),
        "categories": {k: v for k, v in categories.items()},
        "audit_date": str(Path.home() / ".openclaw" / "skills"),
    }
    
    INVENTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(INVENTORY_FILE, 'w') as f:
        json.dump(inventory, f, indent=2)
    
    print(f"\n💾 Inventory saved: {INVENTORY_FILE}")
    
    return categories

def identify_gaps(categories: dict) -> list:
    """Identify skill gaps for aggressive expansion"""
    print("\n🔍 Identifying Skill Gaps")
    print("="*50)
    
    gaps = []
    
    # Check for missing critical categories
    critical = ["hr", "legal", "infrastructure", "security", "monitoring"]
    for cat in critical:
        count = len(categories.get(cat, []))
        if count < 10:
            gaps.append({
                "category": cat,
                "current": count,
                "target": 20,
                "priority": "HIGH"
            })
    
    # Print gaps
    print("\n⚠️  High-Priority Gaps:")
    for gap in gaps:
        print(f"  {gap['category']:15s}: {gap['current']:3d} → {gap['target']:3d} ({gap['priority']})")
    
    return gaps

def recommend_additions():
    """Recommend specific skills to add"""
    print("\n📋 Recommended Skill Additions")
    print("="*50)
    
    recommendations = {
        "hr": ["bamboohr", "gusto", "workday", "adp", "zenefits"],
        "legal": ["ironclad", "docusign", "hellosign", "contractworks", "carta"],
        "infrastructure": ["terraform", "pulumi", "vagrant", "nomad", "consul"],
        "security": ["vault-enterprise", "snyk-enterprise", "crowdstrike", "okta", "auth0"],
        "monitoring": ["datadog", "newrelic", "sentry-enterprise", "pagerduty", "opsgenie"],
    }
    
    for category, skills in recommendations.items():
        print(f"\n{category.upper()}:")
        for skill in skills:
            print(f"  - {skill}")
    
    return recommendations

if __name__ == "__main__":
    categories = audit_skills()
    gaps = identify_gaps(categories)
    recommendations = recommend_additions()
    
    print("\n" + "="*50)
    print("✅ Skills Audit Complete")
    print("="*50)
    print("\nNext: Run expand_repos.sh to add infrastructure repos")
    print("Then: Search for/install recommended skills")
