#!/usr/bin/env python3
"""
JONES NET GROUP MEGA-AGENT v3.0
Unified Intelligence for Mr. J

Single entry point for all 806+ skills, CLIs, and repos.
"""

import os
import sys
import json
import re
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Any, Callable
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib

# Add amazo_core to path
sys.path.insert(0, str(Path(__file__).parent.parent / "amazo_core"))

from context_manager import get_context_manager
from memory_system import get_memory
from ensemble import get_ensemble

@dataclass
class Skill:
    name: str
    path: Path
    category: str
    capabilities: List[str]
    has_cli: bool
    cli_commands: List[str]
    description: str
    effectiveness: float = 0.5
    usage_count: int = 0

@dataclass
class ExecutionPlan:
    approach: str  # 'skill_chain', 'cli', 'direct', 'ensemble'
    steps: List[Dict]
    estimated_time: str
    confidence: float
    reasoning: str

class SkillAbsorber:
    """Absorbs all skills into unified cognitive architecture"""
    
    def __init__(self):
        self.skills: Dict[str, Skill] = {}
        self.capability_matrix: Dict[str, List[Skill]] = {}
        self.skills_dir = Path("~/.openclaw/skills").expanduser()
        
    def absorb_all(self):
        """Absorb all available skills"""
        print("🧠 Absorbing all skills...")
        
        if not self.skills_dir.exists():
            print(f"❌ Skills directory not found: {self.skills_dir}")
            return
        
        count = 0
        for skill_path in self.skills_dir.iterdir():
            if skill_path.is_dir() and not skill_path.name.startswith('.'):
                try:
                    self._absorb_skill(skill_path)
                    count += 1
                except Exception as e:
                    print(f"  ⚠️  {skill_path.name}: {e}")
        
        print(f"✅ Absorbed {count} skills")
        print(f"📊 {len(self.capability_matrix)} unique capabilities identified")
    
    def _absorb_skill(self, skill_path: Path):
        """Deep absorption of single skill"""
        name = skill_path.name
        
        # Parse metadata
        description = self._extract_description(skill_path)
        category = self._categorize(name, description)
        capabilities = self._extract_capabilities(name, description)
        has_cli, cli_commands = self._discover_cli(skill_path)
        
        skill = Skill(
            name=name,
            path=skill_path,
            category=category,
            capabilities=capabilities,
            has_cli=has_cli,
            cli_commands=cli_commands,
            description=description
        )
        
        self.skills[name] = skill
        
        # Add to capability matrix
        for cap in capabilities:
            if cap not in self.capability_matrix:
                self.capability_matrix[cap] = []
            self.capability_matrix[cap].append(skill)
    
    def _extract_description(self, skill_path: Path) -> str:
        """Extract description from SKILL.md or README.md"""
        for filename in ['SKILL.md', 'README.md']:
            doc_path = skill_path / filename
            if doc_path.exists():
                try:
                    content = doc_path.read_text(errors='ignore')
                    lines = content.split('\n')
                    for line in lines[:5]:
                        line = line.strip()
                        if line and not line.startswith('#') and len(line) > 10:
                            return line[:200]
                        if line.startswith('#') and len(line) > 10:
                            return line.replace('#', '').strip()[:200]
                except:
                    pass
        return f"{skill_path.name} skill"
    
    def _categorize(self, name: str, description: str) -> str:
        """Categorize skill by domain"""
        text = (name + " " + description).lower()
        
        categories = {
            'trading': ['trade', 'market', 'crypto', 'bitcoin', 'polygon', 'alpaca', 'binance', 'polymarket', 'finance'],
            'sales': ['sales', 'lead', 'crm', 'apollo', 'hubspot', 'linkedin', 'zoho'],
            'marketing': ['market', 'content', 'social', 'email', 'ad', 'brand', 'youtube', 'twitter', 'seo'],
            'devops': ['devops', 'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'deploy'],
            'security': ['security', 'compliance', 'audit', 'privacy', 'hipaa', 'cyber', 'scan'],
            'data': ['data', 'analy', 'scrap', 'csv', 'excel', 'ga4', 'report', 'database'],
            'hr': ['hiring', 'employee', 'onboard', 'hr', 'people', 'compensation'],
            'operations': ['ops', 'workflow', 'project', 'meeting', 'calendar', 'task'],
            'legal': ['contract', 'legal', 'compliance', 'agreement'],
            'e-commerce': ['shopify', 'woocommerce', 'stripe', 'paypal', 'ecommerce'],
            'productivity': ['notes', 'calendar', 'reminder', 'notion', 'obsidian', 'bear'],
            'core': ['agent', 'flow', 'orchestr', 'harness'],
            'mcp': ['mcp', 'apitap', 'graphthulhu'],
        }
        
        for category, keywords in categories.items():
            if any(kw in text for kw in keywords):
                return category
        
        return 'misc'
    
    def _extract_capabilities(self, name: str, description: str) -> List[str]:
        """Extract capabilities from skill metadata"""
        text = (name + " " + description).lower()
        capabilities = []
        
        # Action verbs
        actions = ['generate', 'create', 'manage', 'analyze', 'automate', 
                   'deploy', 'monitor', 'scrape', 'track', 'optimize',
                   'schedule', 'send', 'receive', 'process', 'transform']
        for action in actions:
            if action in text:
                capabilities.append(action)
        
        # Domain nouns
        domains = ['email', 'calendar', 'data', 'report', 'code', 'api',
                   'database', 'server', 'container', 'workflow']
        for domain in domains:
            if domain in text:
                capabilities.append(domain)
        
        return capabilities if capabilities else ['general']
    
    def _discover_cli(self, skill_path: Path) -> tuple:
        """Discover CLI commands for skill"""
        bin_dir = skill_path / "bin"
        if not bin_dir.exists():
            return False, []
        
        commands = []
        for cmd_file in bin_dir.iterdir():
            if cmd_file.is_file():
                commands.append(cmd_file.name)
        
        return len(commands) > 0, commands
    
    def find_for_objective(self, objective: str) -> List[Skill]:
        """Find skills matching objective"""
        objective_lower = objective.lower()
        words = set(objective_lower.split())
        
        scored = []
        for skill in self.skills.values():
            score = 0
            
            # Name match
            if any(word in skill.name.lower() for word in words):
                score += 3
            
            # Capability match
            for cap in skill.capabilities:
                if any(word in cap for word in words):
                    score += 2
            
            # Description match
            if any(word in skill.description.lower() for word in words):
                score += 1
            
            if score > 0:
                scored.append((score, skill))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        return [s for _, s in scored[:10]]

class CLIUnifier:
    """Unifies all CLIs into single interface"""
    
    def __init__(self, absorber: SkillAbsorber):
        self.absorber = absorber
        self.command_map: Dict[str, Callable] = {}
        
    def execute(self, command: str, *args, **kwargs) -> Dict:
        """Execute CLI command through unified interface"""
        
        # Find matching skill
        matching = self.absorber.find_for_objective(command)
        
        if not matching:
            return {'error': f'No skill found for: {command}'}
        
        # Use best match
        skill = matching[0]
        
        if skill.has_cli:
            return self._execute_cli(skill, command, args, kwargs)
        else:
            return self._execute_skill(skill, command)
    
    def _execute_cli(self, skill: Skill, command: str, args: tuple, kwargs: dict) -> Dict:
        """Execute skill's CLI"""
        # Find appropriate CLI command
        cli_cmd = skill.cli_commands[0] if skill.cli_commands else skill.name
        
        # Build command
        cmd_parts = [str(skill.path / "bin" / cli_cmd)]
        cmd_parts.extend(args)
        
        for key, value in kwargs.items():
            cmd_parts.append(f"--{key}={value}")
        
        try:
            result = subprocess.run(
                cmd_parts,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            return {
                'skill': skill.name,
                'command': ' '.join(cmd_parts),
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode,
                'success': result.returncode == 0
            }
        except Exception as e:
            return {
                'skill': skill.name,
                'error': str(e),
                'success': False
            }
    
    def _execute_skill(self, skill: Skill, objective: str) -> Dict:
        """Execute skill through its Python interface"""
        # Look for main Python file
        for py_file in skill.path.rglob("*.py"):
            if py_file.name in ['__init__.py', 'main.py', f"{skill.name.replace('-', '_')}.py"]:
                return {
                    'skill': skill.name,
                    'path': str(py_file),
                    'note': 'Python skill found - use direct import',
                    'success': True
                }
        
        return {
            'skill': skill.name,
            'note': 'Skill documentation available',
            'description': skill.description,
            'success': True
        }

class JonesNetMegaAgent:
    """
    The One Interface for Jones Net Group.
    Unified mega-agent absorbing all capabilities.
    """
    
    def __init__(self):
        print("🚀 Initializing Jones Net Group Mega-Agent v3.0...")
        
        # Core systems
        self.absorber = SkillAbsorber()
        self.cli = CLIUnifier(self.absorber)
        self.context = get_context_manager()
        self.memory = get_memory()
        self.ensemble = get_ensemble()
        
        # Absorb all capabilities
        self.absorber.absorb_all()
        
        print(f"✅ Mega-Agent ready with {len(self.absorber.skills)} skills")
    
    def think(self, objective: str) -> ExecutionPlan:
        """
        Analyze objective and create execution plan.
        """
        # Find relevant skills
        skills = self.absorber.find_for_objective(objective)
        
        # Check memory for similar objectives
        similar = self.memory.recall_similar(objective)
        
        # Determine approach
        if skills and skills[0].has_cli:
            approach = 'cli'
            confidence = 0.8
        elif skills:
            approach = 'skill_chain'
            confidence = 0.7
        else:
            approach = 'ensemble'
            confidence = 0.6
        
        # Build steps
        steps = []
        for skill in skills[:3]:
            steps.append({
                'skill': skill.name,
                'action': 'execute' if skill.has_cli else 'reference',
                'description': skill.description
            })
        
        return ExecutionPlan(
            approach=approach,
            steps=steps,
            estimated_time=f"{len(steps) * 2}s",
            confidence=confidence,
            reasoning=f"Found {len(skills)} relevant skills for objective"
        )
    
    def execute(self, command: str, **kwargs) -> Dict:
        """
        Execute command through unified interface.
        
        Examples:
        - "deploy trading bot"
        - "check BTC price"
        - "generate proposal"
        """
        print(f"🎯 Executing: {command}")
        
        # Get execution plan
        plan = self.think(command)
        print(f"📋 Plan: {plan.approach} (confidence: {plan.confidence:.0%})")
        
        # Execute based on approach
        if plan.approach == 'cli':
            result = self.cli.execute(command, **kwargs)
        else:
            # Use skill chain
            result = self._execute_skill_chain(plan.steps, kwargs)
        
        # Store in memory
        self.memory.store_episodic(
            f"Command: {command}\nResult: {json.dumps(result)[:200]}",
            importance=0.7 if result.get('success') else 0.9
        )
        
        return result
    
    def _execute_skill_chain(self, steps: List[Dict], kwargs: dict) -> Dict:
        """Execute chain of skills"""
        results = []
        
        for step in steps:
            skill_name = step['skill']
            if skill_name in self.absorber.skills:
                skill = self.absorber.skills[skill_name]
                result = self.cli._execute_skill(skill, "chain execution")
                results.append(result)
        
        return {
            'chain_results': results,
            'success': all(r.get('success', False) for r in results)
        }
    
    def query(self, question: str) -> List[Dict]:
        """
        Query unified knowledge base.
        """
        # Search skills
        matching_skills = self.absorber.find_for_objective(question)
        
        # Search memory
        memories = self.memory.recall_similar(question, k=3)
        
        return {
            'skills': [
                {
                    'name': s.name,
                    'description': s.description,
                    'category': s.category
                }
                for s in matching_skills[:5]
            ],
            'memories': [
                {
                    'content': m.content[:100],
                    'relevance': 'high'
                }
                for m in memories
            ]
        }
    
    def status(self) -> Dict:
        """Report mega-agent status"""
        return {
            'version': '3.0.0',
            'skills_absorbed': len(self.absorber.skills),
            'capabilities': len(self.absorber.capability_matrix),
            'categories': len(set(s.category for s in self.absorber.skills.values())),
            'memory_entries': self.memory.get_insights(),
            'top_capabilities': list(self.absorber.capability_matrix.keys())[:10]
        }
    
    def interactive(self):
        """Run interactive session"""
        print("\n" + "="*60)
        print("JONES NET GROUP MEGA-AGENT v3.0")
        print("Type 'exit' to quit, 'status' for stats")
        print("="*60 + "\n")
        
        while True:
            try:
                command = input("🤖 mega-agent> ").strip()
                
                if command.lower() in ['exit', 'quit']:
                    print("👋 Goodbye!")
                    break
                
                if command.lower() == 'status':
                    status = self.status()
                    print(f"\n📊 Mega-Agent Status:")
                    print(f"  Version: {status['version']}")
                    print(f"  Skills Absorbed: {status['skills_absorbed']}")
                    print(f"  Capabilities: {status['capabilities']}")
                    print(f"  Categories: {status['categories']}")
                    print(f"  Memory Entries: {status['memory_entries'].get('total_memories', 0)}")
                    print(f"  Top capabilities: {', '.join(status['top_capabilities'][:5])}")
                    continue
                
                if not command:
                    continue
                
                # Execute
                result = self.execute(command)
                
                # Display result
                if result.get('success'):
                    print(f"✅ Success!")
                    if 'stdout' in result:
                        print(result['stdout'][:500])
                else:
                    print(f"❌ Error: {result.get('error', 'Unknown error')}")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    """Main entry point"""
    mega = JonesNetMegaAgent()
    
    if len(sys.argv) > 1:
        # Command line mode
        command = ' '.join(sys.argv[1:])
        result = mega.execute(command)
        print(json.dumps(result, indent=2))
    else:
        # Interactive mode
        mega.interactive()

if __name__ == "__main__":
    main()
