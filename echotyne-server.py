#!/usr/bin/env python3
"""
Echotyne Command Center - Local Server
Serves the Amazo AI interface and handles basic interactions
"""

import http.server
import socketserver
import json
import datetime
from urllib.parse import urlparse, parse_qs
import os

PORT = 8081

class EchotyneHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.serve_main_page()
        elif self.path == '/api/status':
            self.serve_api_status()
        elif self.path == '/api/metrics':
            self.serve_metrics()
        elif self.path == '/api/memory':
            self.serve_memory()
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/command':
            self.handle_command()
        else:
            self.send_error(404)
    
    def serve_main_page(self):
        try:
            with open('echotyne-command-center.html', 'r') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(content.encode())
        except FileNotFoundError:
            self.serve_simple_interface()
    
    def serve_simple_interface(self):
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Echotyne Command Center</title>
            <style>
                body {{ font-family: Arial, sans-serif; background: #1a1a2e; color: white; padding: 20px; }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .status {{ background: rgba(0,212,255,0.2); padding: 20px; border-radius: 10px; margin: 20px 0; }}
                .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }}
                .metric {{ background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; text-align: center; }}
                .btn {{ background: #00d4ff; color: black; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }}
                .command-area {{ background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 20px 0; }}
                input {{ background: rgba(0,0,0,0.3); color: white; border: 1px solid rgba(255,255,255,0.3); padding: 10px; border-radius: 5px; width: 70%; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🤖 ECHOTYNE COMMAND CENTER</h1>
                <h2>Amazo AI - Local Interface</h2>
                <p>Local backup interface for enterprise automation</p>
            </div>
            
            <div class="status">
                <h3>System Status</h3>
                <p>✅ Amazo AI Backup: ACTIVE</p>
                <p>✅ Enterprise Architecture: LOADED</p>
                <p>✅ Bot Army: CONFIGURED</p>
                <p>⚠️ Docker Infrastructure: PENDING DEPLOYMENT</p>
                <p>⚠️ Moltbook Connection: PENDING CLAIM</p>
            </div>
            
            <div class="metrics">
                <div class="metric">
                    <h4>Revenue</h4>
                    <p>$0 / $100K</p>
                </div>
                <div class="metric">
                    <h4>Bots Online</h4>
                    <p>0 / 5</p>
                </div>
                <div class="metric">
                    <h4>Content Today</h4>
                    <p>0 posts</p>
                </div>
                <div class="metric">
                    <h4>Leads</h4>
                    <p>0 active</p>
                </div>
            </div>
            
            <div class="command-area">
                <h3>Quick Actions</h3>
                <button class="btn" onclick="alert('Deploy Docker Infrastructure')">Deploy Infrastructure</button>
                <button class="btn" onclick="alert('Claim Moltbook Agent')">Claim Moltbook</button>
                <button class="btn" onclick="alert('Generate First Content')">Create Content</button>
                <button class="btn" onclick="alert('Check Lead Pipeline')">View Pipeline</button>
            </div>
            
            <div class="command-area">
                <h3>Direct Command</h3>
                <form onsubmit="handleCommand(event)">
                    <input type="text" id="command" placeholder="Enter command..." style="width: 70%;">
                    <button type="submit" class="btn">Execute</button>
                </form>
                <div id="response" style="margin-top: 15px; background: rgba(0,0,0,0.3); padding: 10px; border-radius: 5px; min-height: 50px;">
                    Ready for commands...
                </div>
            </div>
            
            <script>
                function handleCommand(event) {{
                    event.preventDefault();
                    const command = document.getElementById('command').value;
                    const response = document.getElementById('response');
                    
                    response.innerHTML = `Processing: ${command}<br>Status: Command received by local backup system`;
                    
                    // In real implementation, this would call backend API
                    setTimeout(() => {{
                        response.innerHTML += '<br>Result: Command logged for execution when full system is online';
                    }}, 1000);
                    
                    document.getElementById('command').value = '';
                }}
            </script>
        </body>
        </html>
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_api_status(self):
        status = {
            "success": True,
            "timestamp": datetime.datetime.now().isoformat(),
            "system": {
                "amazo_backup": "active",
                "enterprise_architecture": "loaded",
                "bot_army": "configured",
                "docker_status": "pending_deployment",
                "moltbook_status": "pending_claim"
            },
            "metrics": {
                "current_revenue": 0,
                "target_revenue": 100000,
                "active_bots": 0,
                "total_bots": 5,
                "content_today": 0,
                "active_leads": 0
            }
        }
        self.send_json_response(status)
    
    def serve_metrics(self):
        metrics = {
            "revenue": {"current": 0, "target": 100000, "progress": 0},
            "bots": {"online": 0, "total": 5, "uptime": "0%"},
            "content": {"today": 0, "scheduled": 0, "engagement": 0},
            "leads": {"active": 0, "proposals_sent": 0, "conversion_rate": 0}
        }
        self.send_json_response(metrics)
    
    def serve_memory(self):
        try:
            with open('memory/persistent-memory.json', 'r') as f:
                memory = json.load(f)
            self.send_json_response(memory)
        except FileNotFoundError:
            self.send_json_response({"error": "Memory file not found"}, 404)
    
    def handle_command(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            command = data.get('command', '')
            
            response = {
                "success": True,
                "command": command,
                "timestamp": datetime.datetime.now().isoformat(),
                "result": f"Command '{command}' received by local backup system",
                "status": "logged_for_execution"
            }
            
            # Log command to file
            self.log_command(command, response)
            
            self.send_json_response(response)
        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)
    
    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def log_command(self, command, response):
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "command": command,
            "response": response,
            "source": "local_interface"
        }
        
        try:
            with open('memory/command-log.json', 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            print(f"Failed to log command: {e}")

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), EchotyneHandler) as httpd:
        print(f"🚀 Echotyne Command Center running at http://localhost:{PORT}")
        print(f"💾 Local backup interface serving enterprise automation")
        print(f"🤖 Amazo AI ready for commands")
        print(f"📊 API endpoints available at /api/status, /api/metrics, /api/memory")
        print(f"💬 Command interface at root URL")
        print(f"Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
            httpd.shutdown()