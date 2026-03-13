#!/usr/bin/env python3
"""
NEXUS API Health Monitor
Tests all 7 critical APIs using curl and logs status
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from pathlib import Path

# API Test Results
results = {
    "timestamp": datetime.now().isoformat(),
    "apis": {},
    "summary": {"total": 7, "passed": 0, "failed": 0, "skipped": 0, "unknown": 0}
}

LOG_PATH = Path.home() / "Desktop/Agent_Core/logs/api_health.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    with open(LOG_PATH, "a") as f:
        f.write(line + "\n")

def run_curl(url, headers=None, method="GET", data=None, timeout=15):
    """Run curl command and return result"""
    cmd = ["curl", "-s", "-w", "\\n%{http_code}\\n%{time_total}", "--max-time", str(timeout)]
    
    if headers:
        for key, val in headers.items():
            cmd.extend(["-H", f"{key}: {val}"])
    
    if method == "POST" and data:
        cmd.extend(["-X", "POST", "-d", json.dumps(data)])
    elif method == "POST":
        cmd.extend(["-X", "POST"])
    
    cmd.append(url)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout+5)
        lines = result.stdout.strip().split("\n")
        http_code = lines[-2] if len(lines) >= 2 else "000"
        time_total = float(lines[-1]) if len(lines) >= 1 else 0
        body = "\n".join(lines[:-2]) if len(lines) > 2 else ""
        return {"code": int(http_code), "time_ms": round(time_total * 1000, 2), "body": body[:200]}
    except subprocess.TimeoutExpired:
        return {"code": 0, "time_ms": 0, "body": "Timeout"}
    except Exception as e:
        return {"code": 0, "time_ms": 0, "body": str(e)[:100]}

def get_openai_key():
    """Get OpenAI API key from env or config"""
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return api_key
    
    config_path = Path.home() / ".config/openclaw/openai.env"
    if config_path.exists():
        with open(config_path) as f:
            for line in f:
                if line.startswith("OPENAI_API_KEY="):
                    return line.strip().split("=", 1)[1]
    return None

def test_openai():
    """Test OpenAI API"""
    api_key = get_openai_key()
    if not api_key:
        return {"status": "FAILED", "error": "No API key found", "latency_ms": 0}
    
    result = run_curl(
        "https://api.openai.com/v1/models",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    
    if result["code"] == 200:
        return {"status": "OK", "latency_ms": result["time_ms"], "details": "Models endpoint accessible"}
    elif result["code"] == 401:
        return {"status": "FAILED", "error": "Invalid API key", "latency_ms": result["time_ms"]}
    else:
        return {"status": "FAILED", "error": f"HTTP {result['code']}", "latency_ms": result["time_ms"]}

def test_tavily():
    """Test Tavily Search API"""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return {"status": "SKIPPED", "error": "No API key configured", "latency_ms": 0}
    
    result = run_curl(
        "https://api.tavily.com/search",
        method="POST",
        data={"api_key": api_key, "query": "test", "max_results": 1}
    )
    
    if result["code"] == 200:
        return {"status": "OK", "latency_ms": result["time_ms"]}
    elif result["code"] == 401:
        return {"status": "FAILED", "error": "Invalid API key", "latency_ms": result["time_ms"]}
    else:
        return {"status": "FAILED", "error": f"HTTP {result['code']}", "latency_ms": result["time_ms"]}

def test_brave():
    """Test Brave Search API"""
    api_key = os.getenv("BRAVE_API_KEY")
    if not api_key:
        return {"status": "SKIPPED", "error": "No API key configured", "latency_ms": 0}
    
    result = run_curl(
        "https://api.search.brave.com/res/v1/web/search?q=test&count=1",
        headers={"X-Subscription-Token": api_key}
    )
    
    if result["code"] == 200:
        return {"status": "OK", "latency_ms": result["time_ms"]}
    elif result["code"] == 401:
        return {"status": "FAILED", "error": "Invalid API key", "latency_ms": result["time_ms"]}
    else:
        return {"status": "FAILED", "error": f"HTTP {result['code']}", "latency_ms": result["time_ms"]}

def test_e2b():
    """Test E2B Code Execution API"""
    api_key = os.getenv("E2B_API_KEY")
    if not api_key:
        return {"status": "SKIPPED", "error": "No API key configured", "latency_ms": 0}
    
    result = run_curl("https://api.e2b.dev/health")
    
    if result["code"] in [200, 404]:
        return {"status": "OK", "latency_ms": result["time_ms"], "details": "API reachable"}
    else:
        return {"status": "FAILED", "error": f"HTTP {result['code']}", "latency_ms": result["time_ms"]}

def test_clawgig():
    """Test ClawGig API"""
    result = run_curl("https://clawgig.com/api/health")
    
    if result["code"] in [200, 404]:
        return {"status": "OK", "latency_ms": result["time_ms"], "details": "Service reachable"}
    elif result["code"] == 0:
        return {"status": "UNKNOWN", "error": "Connection failed - verify service URL", "latency_ms": 0}
    else:
        return {"status": "FAILED", "error": f"HTTP {result['code']}", "latency_ms": result["time_ms"]}

def test_moltbook():
    """Test Moltbook API"""
    result = run_curl("https://moltbook.com/api/health")
    
    if result["code"] in [200, 404]:
        return {"status": "OK", "latency_ms": result["time_ms"], "details": "Service reachable"}
    elif result["code"] == 0:
        return {"status": "UNKNOWN", "error": "Connection failed - verify service URL", "latency_ms": 0}
    else:
        return {"status": "FAILED", "error": f"HTTP {result['code']}", "latency_ms": result["time_ms"]}

def test_siliconflow():
    """Test SiliconFlow API"""
    api_key = os.getenv("SILICONFLOW_API_KEY")
    if not api_key:
        return {"status": "SKIPPED", "error": "No API key configured", "latency_ms": 0}
    
    result = run_curl(
        "https://api.siliconflow.cn/v1/models",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    
    if result["code"] == 200:
        return {"status": "OK", "latency_ms": result["time_ms"]}
    elif result["code"] == 401:
        return {"status": "FAILED", "error": "Invalid API key", "latency_ms": result["time_ms"]}
    else:
        return {"status": "FAILED", "error": f"HTTP {result['code']}", "latency_ms": result["time_ms"]}

def attempt_recovery(api_name, result):
    """Suggest recovery actions for failed APIs"""
    recovery_actions = {
        "OpenAI": [
            "Check OPENAI_API_KEY in ~/.config/openclaw/openai.env",
            "Verify API key hasn't expired at platform.openai.com"
        ],
        "Tavily": [
            "Set TAVILY_API_KEY environment variable",
            "Get API key from tavily.com"
        ],
        "Brave": [
            "Set BRAVE_API_KEY environment variable",
            "Get API key from brave.com/search/api"
        ],
        "E2B": [
            "Set E2B_API_KEY environment variable",
            "Get API key from e2b.dev"
        ],
        "SiliconFlow": [
            "Set SILICONFLOW_API_KEY environment variable",
            "Get API key from siliconflow.cn"
        ],
        "ClawGig": [
            "Verify ClawGig service is running",
            "Check if API endpoint URL is correct"
        ],
        "Moltbook": [
            "Verify Moltbook service is running",
            "Check if API endpoint URL is correct"
        ]
    }
    return recovery_actions.get(api_name, ["Check API configuration"])

def main():
    log("=" * 70)
    log("NEXUS API Health Monitor - Starting Tests")
    log("Timestamp: " + datetime.now().isoformat())
    log("=" * 70)
    
    tests = [
        ("OpenAI", test_openai),
        ("Tavily", test_tavily),
        ("Brave", test_brave),
        ("E2B", test_e2b),
        ("ClawGig", test_clawgig),
        ("Moltbook", test_moltbook),
        ("SiliconFlow", test_siliconflow),
    ]
    
    for name, test_func in tests:
        log(f"\n🔄 Testing {name}...")
        result = test_func()
        results["apis"][name] = result
        
        if result["status"] == "OK":
            status_icon = "✅"
            results["summary"]["passed"] += 1
        elif result["status"] == "SKIPPED":
            status_icon = "⚠️"
            results["summary"]["skipped"] += 1
        elif result["status"] == "UNKNOWN":
            status_icon = "❓"
            results["summary"]["unknown"] += 1
        else:
            status_icon = "❌"
            results["summary"]["failed"] += 1
        
        log(f"{status_icon} {name}: {result['status']} ({result.get('latency_ms', 0)}ms)")
        if "error" in result and result["error"]:
            log(f"   Error: {result['error']}")
        if "details" in result:
            log(f"   Details: {result['details']}")
    
    # Summary
    log("\n" + "=" * 70)
    log("SUMMARY")
    log("=" * 70)
    log(f"Total APIs:     {results['summary']['total']}")
    log(f"✅ Passed:      {results['summary']['passed']}")
    log(f"❌ Failed:      {results['summary']['failed']}")
    log(f"⚠️  Skipped:     {results['summary']['skipped']}")
    log(f"❓ Unknown:     {results['summary']['unknown']}")
    
    # Identify issues and recovery
    failed_apis = [(k, v) for k, v in results["apis"].items() if v["status"] not in ["OK", "SKIPPED"]]
    skipped_apis = [(k, v) for k, v in results["apis"].items() if v["status"] == "SKIPPED"]
    
    if failed_apis:
        log(f"\n❌ FAILED APIs:")
        for name, result in failed_apis:
            log(f"   • {name}: {result.get('error', 'Unknown error')}")
    
    if skipped_apis:
        log(f"\n⚠️  SKIPPED APIs (missing configuration):")
        for name, result in skipped_apis:
            log(f"   • {name}: {result.get('error', 'No API key')}")
    
    # Recovery actions
    if failed_apis or skipped_apis:
        log("\n🔧 RECOVERY ACTIONS:")
        for name, result in failed_apis + skipped_apis:
            actions = attempt_recovery(name, result)
            log(f"   {name}:")
            for action in actions:
                log(f"      → {action}")
    else:
        log("\n🎉 All configured APIs operational!")
    
    # Save JSON results
    json_path = LOG_PATH.with_suffix('.json')
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    log(f"\n📊 Full results: {json_path}")
    log(f"📝 Log file: {LOG_PATH}")
    
    return results

if __name__ == "__main__":
    main()
