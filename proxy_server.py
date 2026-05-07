import http.server
import socketserver
import urllib.parse
import urllib.request

UPSTREAM_BASE = "https://add.piotrkojalowicz.dev/api"
HOST = "localhost"
PORT = 8765


class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if not self.path.startswith("/proxy/"):
            self.send_error(404, "Not Found")
            return

        upstream_path = "/" + self.path[len("/proxy/"):]
        upstream_url = UPSTREAM_BASE + upstream_path

        parsed = urllib.parse.urlsplit(upstream_url)
        query = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
        api_key = query.pop("api_key", [None])[0]
        cleaned_query = urllib.parse.urlencode(query, doseq=True)
        upstream_url = urllib.parse.urlunsplit(
            (parsed.scheme, parsed.netloc, parsed.path, cleaned_query, parsed.fragment)
        )

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/event-stream",
            "Connection": "keep-alive",
        }
        if api_key:
            headers["X-API-Key"] = api_key

        try:
            req = urllib.request.Request(upstream_url, headers=headers, method="GET")
            with urllib.request.urlopen(req, timeout=60) as resp:
                self.send_response(resp.status)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Headers", "*")
                self.send_header("Cache-Control", "no-cache")
                content_type = resp.headers.get("Content-Type")
                if content_type:
                    self.send_header("Content-Type", content_type)
                self.end_headers()

                # Stream response for SSE endpoints.
                while True:
                    chunk = resp.read(1024)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    self.wfile.flush()
        except Exception as exc:
            self.send_response(502)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Headers", "*")
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"Upstream error: {exc}".encode("utf-8"))

    def log_message(self, format, *args):
        return


def main():
    with socketserver.ThreadingTCPServer((HOST, PORT), ProxyHandler) as httpd:
        print(f"Proxy running on http://{HOST}:{PORT}")
        print("Proxying /proxy/* -> https://add.piotrkojalowicz.dev/api/*")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
