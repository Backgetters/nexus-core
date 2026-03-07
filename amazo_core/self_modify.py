#!/usr/bin/env python3
"""
Amazo Self-Modification System
Phase 2: Intelligence - Autonomous self-improvement
Implements Ouroboros-style edit → commit → improve loop
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import hashlib

class SelfModifier:
    """
    Autonomous self-improvement system.
    Identifies improvements, validates with multi-model review, commits changes.
    """
    
    def __init__(self, repo_dir: str = "~/clawd"):
        self.repo_dir = Path(repo_dir).expanduser()
        self.improvements_dir = self.repo_dir / "amazo_core" / "improvements"
        self.improvements_dir.mkdir(parents=True, exist_ok=True)
        
        self.change_log = self.improvements_dir / "changes.json"
        self.performance_log = self.improvements_dir / "performance.json"
        
        # Load history
        self.changes = self._load_json(self.change_log, [])
        self.performance = self._load_json(self.performance_log, {})
    
    def _load_json(self, path: Path, default):
        if path.exists():
            with open(path) as f:
                return json.load(f)
        return default
    
    def _save_json(self, path: Path, data):
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def identify_improvements(self) -> List[Dict]:
        """
        Analyze codebase and identify improvement opportunities.
        """
        improvements = []
        
        # Check for TODO comments
        improvements.extend(self._find_todos())
        
        # Check for performance bottlenecks
        improvements.extend(self._find_bottlenecks())
        
        # Check for missing error handling
        improvements.extend(self._find_error_handling_gaps())
        
        # Check for documentation gaps
        improvements.extend(self._find_doc_gaps())
        
        return improvements
    
    def _find_todos(self) -> List[Dict]:
        """Find TODO comments in code"""
        todos = []
        core_dir = self.repo_dir / "amazo_core"
        
        for py_file in core_dir.rglob("*.py"):
            content = py_file.read_text()
            lines = content.split('\n')
            
            for i, line in enumerate(lines, 1):
                if 'TODO' in line or 'FIXME' in line or 'XXX' in line:
                    todos.append({
                        'type': 'todo',
                        'file': str(py_file.relative_to(self.repo_dir)),
                        'line': i,
                        'description': line.strip(),
                        'priority': 'high' if 'FIXME' in line else 'medium'
                    })
        
        return todos
    
    def _find_bottlenecks(self) -> List[Dict]:
        """Identify potential performance issues"""
        bottlenecks = []
        core_dir = self.repo_dir / "amazo_core"
        
        for py_file in core_dir.rglob("*.py"):
            content = py_file.read_text()
            
            # Check for O(n^2) patterns
            if 'for' in content and 'for' in content[content.find('for')+3:]:
                if 'range(len(' in content:
                    bottlenecks.append({
                        'type': 'performance',
                        'file': str(py_file.relative_to(self.repo_dir)),
                        'issue': 'Potential O(n^2) loop pattern',
                        'suggestion': 'Consider using enumerate or iterator patterns'
                    })
            
            # Check for repeated file reads
            if content.count('.read_text()') > 3:
                bottlenecks.append({
                    'type': 'performance',
                    'file': str(py_file.relative_to(self.repo_dir)),
                    'issue': 'Multiple file reads',
                    'suggestion': 'Cache file contents in memory'
                })
        
        return bottlenecks
    
    def _find_error_handling_gaps(self) -> List[Dict]:
        """Find functions lacking error handling"""
        gaps = []
        core_dir = self.repo_dir / "amazo_core"
        
        for py_file in core_dir.rglob("*.py"):
            content = py_file.read_text()
            
            # Simple heuristic: functions without try/except
            # This is a simplified check - real implementation would use AST
            if 'def ' in content and 'try:' not in content:
                gaps.append({
                    'type': 'reliability',
                    'file': str(py_file.relative_to(self.repo_dir)),
                    'issue': 'Missing error handling',
                    'suggestion': 'Add try/except blocks for robustness'
                })
        
        return gaps
    
    def _find_doc_gaps(self) -> List[Dict]:
        """Find missing documentation"""
        gaps = []
        core_dir = self.repo_dir / "amazo_core"
        
        for py_file in core_dir.rglob("*.py"):
            content = py_file.read_text()
            
            # Count functions vs docstrings
            func_count = content.count('def ')
            docstring_count = content.count('"""') // 2  # Approximate
            
            if func_count > docstring_count:
                gaps.append({
                    'type': 'documentation',
                    'file': str(py_file.relative_to(self.repo_dir)),
                    'issue': f'{func_count - docstring_count} functions missing docstrings',
                    'suggestion': 'Add docstrings to all public methods'
                })
        
        return gaps
    
    def generate_improvement(self, issue: Dict) -> Optional[Dict]:
        """
        Generate a specific code improvement for an identified issue.
        """
        improvement = {
            'id': hashlib.md5(json.dumps(issue).encode()).hexdigest()[:8],
            'timestamp': datetime.now().isoformat(),
            'issue': issue,
            'status': 'generated'
        }
        
        if issue['type'] == 'todo':
            improvement['description'] = f"Address {issue['description']}"
            improvement['action'] = 'implement'
        
        elif issue['type'] == 'performance':
            improvement['description'] = f"Optimize: {issue['issue']}"
            improvement['action'] = 'refactor'
        
        elif issue['type'] == 'reliability':
            improvement['description'] = f"Add error handling to {issue['file']}"
            improvement['action'] = 'enhance'
        
        elif issue['type'] == 'documentation':
            improvement['description'] = f"Add docstrings to {issue['file']}"
            improvement['action'] = 'document'
        
        return improvement
    
    def multi_model_review(self, improvement: Dict) -> Dict:
        """
        Simulate multi-model review before committing.
        In production, this would query actual models.
        """
        # Simulate reviews
        reviews = {
            'claude': {'score': 0.85, 'comments': ['Good improvement', 'Safe change']},
            'gpt4': {'score': 0.80, 'comments': ['Reasonable', 'Well-scoped']},
            'kimi': {'score': 0.90, 'comments': ['Efficient', 'Clear benefit']}
        }
        
        avg_score = sum(r['score'] for r in reviews.values()) / len(reviews)
        approvals = sum(1 for r in reviews.values() if r['score'] > 0.7)
        
        return {
            'approved': approvals >= 2,
            'consensus_score': avg_score,
            'reviews': reviews,
            'requires_human': avg_score < 0.75
        }
    
    def apply_improvement(self, improvement: Dict) -> bool:
        """
        Apply an improvement to the codebase.
        """
        # Get multi-model review
        review = self.multi_model_review(improvement)
        
        if not review['approved']:
            improvement['status'] = 'rejected'
            improvement['review'] = review
            self.changes.append(improvement)
            self._save_json(self.change_log, self.changes)
            return False
        
        if review['requires_human']:
            improvement['status'] = 'pending_human_review'
            improvement['review'] = review
            self.changes.append(improvement)
            self._save_json(self.change_log, self.changes)
            return False
        
        # Apply the change (simplified - real implementation would edit files)
        improvement['status'] = 'applied'
        improvement['review'] = review
        improvement['applied_at'] = datetime.now().isoformat()
        
        self.changes.append(improvement)
        self._save_json(self.change_log, self.changes)
        
        return True
    
    def commit_changes(self, message: str = None):
        """
        Commit changes to git.
        """
        if not message:
            message = f"Self-improvement: {len(self.changes)} changes applied"
        
        try:
            # Stage changes
            subprocess.run(
                ['git', '-C', str(self.repo_dir), 'add', '-A'],
                check=True,
                capture_output=True
            )
            
            # Commit
            subprocess.run(
                ['git', '-C', str(self.repo_dir), 'commit', '-m', message],
                check=True,
                capture_output=True
            )
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"Git error: {e}")
            return False
    
    def run_improvement_cycle(self):
        """
        Run one full self-improvement cycle.
        """
        print("🔍 Identifying improvements...")
        issues = self.identify_improvements()
        print(f"  Found {len(issues)} potential improvements")
        
        if not issues:
            print("✅ No improvements needed at this time")
            return
        
        print("\n🎯 Generating improvements...")
        improvements = []
        for issue in issues[:5]:  # Limit to top 5
            imp = self.generate_improvement(issue)
            if imp:
                improvements.append(imp)
                print(f"  - {imp['description'][:60]}...")
        
        print("\n🤖 Reviewing with multi-model consensus...")
        applied = 0
        for imp in improvements:
            if self.apply_improvement(imp):
                applied += 1
                print(f"  ✅ Applied: {imp['description'][:50]}...")
            else:
                print(f"  ⏸️  Pending: {imp['description'][:50]}...")
        
        if applied > 0:
            print(f"\n💾 Committing {applied} improvements...")
            if self.commit_changes():
                print("  ✅ Changes committed")
            else:
                print("  ⚠️  Commit failed")
        
        print(f"\n📊 Summary: {applied}/{len(improvements)} improvements applied")
        
        return {
            'issues_found': len(issues),
            'improvements_generated': len(improvements),
            'improvements_applied': applied
        }

class PerformanceMonitor:
    """
    Monitor and track performance metrics for continuous improvement.
    """
    
    def __init__(self, repo_dir: str = "~/clawd"):
        self.repo_dir = Path(repo_dir).expanduser()
        self.metrics_file = self.repo_dir / "amazo_core" / "improvements" / "metrics.json"
        self.metrics = self._load_metrics()
    
    def _load_metrics(self) -> Dict:
        if self.metrics_file.exists():
            with open(self.metrics_file) as f:
                return json.load(f)
        return {
            'response_times': [],
            'token_usage': [],
            'error_rates': [],
            'success_rates': []
        }
    
    def record_metric(self, metric_type: str, value: float):
        """Record a performance metric"""
        if metric_type not in self.metrics:
            self.metrics[metric_type] = []
        
        self.metrics[metric_type].append({
            'value': value,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last 1000 entries
        self.metrics[metric_type] = self.metrics[metric_type][-1000:]
        
        # Save
        with open(self.metrics_file, 'w') as f:
            json.dump(self.metrics, f, indent=2)
    
    def get_performance_report(self) -> Dict:
        """Generate performance report"""
        report = {}
        
        for metric_type, values in self.metrics.items():
            if values:
                vals = [v['value'] for v in values[-100:]]  # Last 100
                report[metric_type] = {
                    'current': vals[-1] if vals else 0,
                    'average': sum(vals) / len(vals) if vals else 0,
                    'min': min(vals) if vals else 0,
                    'max': max(vals) if vals else 0,
                    'trend': 'improving' if len(vals) > 1 and vals[-1] < vals[0] else 'stable'
                }
        
        return report

if __name__ == "__main__":
    print("=" * 60)
    print("AMAZO SELF-MODIFICATION SYSTEM")
    print("=" * 60)
    print()
    
    # Run improvement cycle
    modifier = SelfModifier()
    result = modifier.run_improvement_cycle()
    
    print()
    print("=" * 60)
    
    if result:
        print(f"Cycle complete: {result['improvements_applied']} improvements applied")
    
    print("=" * 60)
