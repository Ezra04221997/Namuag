from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs  # ✅ Correct import
import os

# 🔒 Secure credentials using environment variables
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "password123")

class MyServer(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/login":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')

            # ✅ Correct form parsing using urllib.parse
            form = parse_qs(post_data)
            username = form.get("username", [""])[0]
            password = form.get("password", [""])[0]

            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                # ✅ Successful login
                self.send_response(302)
                self.send_header("Location", "/dashboard.html")
                self.end_headers()
            else:
                # ❌ Failed login
                self.send_response(302)
                self.send_header("Location", "/login.html")
                self.end_headers()

    def do_GET(self):
        if self.path in ["/dashboard.html", "/login.html"]:
            return SimpleHTTPRequestHandler.do_GET(self)
        else:
            # ✅ Fix: Set Content-Type before writing 404 response
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"404 - Page Not Found")  # ✅ Fixed

# ✅ Improved server setup with error handling
def run_server():
    host = "localhost"
    port = 8080  # ✅ Updated port
    server = HTTPServer((host, port), MyServer)

    print(f"🚀 Server running at http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server shutting down...")
        server.server_close()

if __name__ == "__main__":
    run_server()

