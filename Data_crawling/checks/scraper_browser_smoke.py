"""Real Firefox capture/redirect smoke check using a local HTTP fixture only.

Run: .venv/bin/python -m checks.scraper_browser_smoke
"""

import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from url_discovery.scraper import browser_fetch, run_pipeline


def main():
    requests = []

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            requests.append(self.path)
            redirects = {
                "/start": "/middle",
                "/middle": "/policy?part=refund-policy",
                "/blocked": "/private",
                "/outside": f"http://localhost:{self.server.server_port}/unwanted",
            }
            if self.path == "/robots.txt":
                body = b"User-agent: *\nDisallow: /private\n"
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
            elif self.path in redirects:
                body = b""
                self.send_response(302)
                self.send_header("Location", redirects[self.path])
            else:
                body = """<!doctype html><html><head><title>Policy fixture</title></head>
                <body><h1>Chính sách</h1><p id="content">Initial content</p>
                <script>document.getElementById('content').textContent = 'Nội dung động';</script>
                </body></html>""".encode()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    origin = f"http://127.0.0.1:{server.server_port}"
    workspace = Path(__file__).resolve().parents[1]
    try:
        with browser_fetch(workspace, [origin + "/start"], render_wait_ms=50) as fetch:
            result = fetch(origin + "/start")
            assert result["http_status"] == 200, result
            assert result["final_url"] == origin + "/policy?part=refund-policy", result
            assert b"Initial content" in result["response_body"], result
            assert "Nội dung động" in result["rendered_html"], result
            assert "Nội dung động" in result["text"] and "Initial content" not in result["text"]
            assert result["redirect_chain"] == [
                origin + "/start",
                origin + "/middle",
                origin + "/policy?part=refund-policy",
            ], result["redirect_chain"]
            with tempfile.TemporaryDirectory() as temporary:
                report = run_pipeline(
                    [origin + "/blocked", origin + "/outside", origin + "/policy"],
                    Path(temporary) / "run",
                    fetch,
                    delay_seconds=0,
                )
                assert (report["succeeded"], report["failed"]) == (1, 2), report
            assert "/private" not in requests, requests
            assert "/unwanted" not in requests, requests
        print(
            "PASS: raw/rendered capture, ordered redirects, robots/scope checks, failure continuation."
        )
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


if __name__ == "__main__":
    main()
