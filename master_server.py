from http.server import HTTPServer, BaseHTTPRequestHandler
import json, time

servers = {}

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args): pass

    def do_GET(self):
        now = time.time()
        active = {k: v for k, v in servers.items() if now - v["time"] < 15}
        servers.clear()
        servers.update(active)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(list(servers.values())).encode())

    def do_POST(self):
        length = int(self.headers["Content-Length"])
        data = json.loads(self.rfile.read(length))
        key = f"{data['ip']}:{data['port']}"
        servers[key] = {
            "name": data.get("name", "My Server"),
            "ip": data["ip"],
            "port": data["port"],
            "players": data.get("players", 0),
            "time": time.time()
        }
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

port = int(__import__('os').environ.get('PORT', 8000))
print(f"Master server running on port {port}")
HTTPServer(('0.0.0.0', port), Handler).serve_forever()
