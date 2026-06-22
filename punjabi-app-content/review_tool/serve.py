"""Single-command launcher for the Sikho Punjabi review tool."""

import http.server
import json
import pathlib
import subprocess
import sys
import webbrowser
import os
import urllib.parse


Path = pathlib.Path

ROOT_DIR = Path(__file__).resolve().parent.parent
REVIEW_TOOL_DIR = ROOT_DIR / "review_tool"
FEEDBACK_FILE = REVIEW_TOOL_DIR / "feedback.json"
STREAMS_DIR = ROOT_DIR / "session_work" / "2026-06-10_pipeline_plan"
VOCAB_DIR = ROOT_DIR / "processed_data" / "vocab"
TOP_PROVERBS_FILE = REVIEW_TOOL_DIR / "top_100_proverbs.json"
REVIEW_HTML = REVIEW_TOOL_DIR / "review.html"

PORT = 8765


class ReviewToolHandler(http.server.BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def log_message(self, format, *args):
        sys.stderr.write("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format % args))

    def do_GET(self):
        try:
            path = urllib.parse.urlparse(self.path).path
            if path == "/":
                self._serve_review_html()
            elif path == "/api/feedback":
                self._serve_feedback()
            elif path == "/api/data/streams":
                self._serve_streams()
            elif path == "/api/data/vocab":
                self._serve_vocab()
            elif path == "/api/data/proverbs":
                self._serve_proverbs()
            else:
                self._send_json({"error": "not found"}, status=404)
        except Exception as e:
            self._handle_exception(e)

    def do_POST(self):
        try:
            path = urllib.parse.urlparse(self.path).path
            if path == "/api/feedback":
                self._save_feedback()
            else:
                self._send_json({"error": "not found"}, status=404)
        except Exception as e:
            self._handle_exception(e)

    def _handle_exception(self, e):
        print(f"Error handling {self.command} {self.path}: {e}", file=sys.stderr)
        self._send_json({"error": str(e)}, status=500)

    def _send_bytes(self, content, status=200, content_type="application/octet-stream"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _send_json(self, data, status=200):
        content = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self._send_bytes(content, status=status, content_type="application/json; charset=utf-8")

    def _serve_review_html(self):
        content = REVIEW_HTML.read_bytes()
        self._send_bytes(content, content_type="text/html; charset=utf-8")

    def _serve_feedback(self):
        if FEEDBACK_FILE.exists():
            content = FEEDBACK_FILE.read_bytes()
            self._send_bytes(content, content_type="application/json; charset=utf-8")
        else:
            self._send_json({})

    def _save_feedback(self):
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)
        try:
            data = json.loads(body.decode("utf-8"))
            if not isinstance(data, dict):
                raise ValueError("feedback must be a JSON object")
        except Exception:
            self._send_json({"error": "invalid json"}, status=400)
            return

        REVIEW_TOOL_DIR.mkdir(parents=True, exist_ok=True)
        FEEDBACK_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        self._send_json({"status": "ok"})

    def _serve_streams(self):
        streams = {}
        for path in sorted(STREAMS_DIR.glob("s*_enriched.json")):
            stream_key = path.name.split("_", 1)[0]
            with open(path, encoding="utf-8") as f:
                streams[stream_key] = json.load(f)
        self._send_json(streams)

    def _serve_vocab(self):
        vocab_items = []
        for path in sorted(VOCAB_DIR.glob("[a-z]*_*.json")):
            if path.name == ".checkpoint.json":
                continue
            with open(path, encoding="utf-8") as f:
                item = json.load(f)
            if item.get("needs_enrichment"):
                continue

            tags = item.get("tags") or []
            source = ""
            for tag in tags:
                if tag != "conversational":
                    source = tag
                    break

            roman = item.get("roman") or {}
            vocab_items.append(
                {
                    "id": item.get("id"),
                    "gurmukhi": item.get("gurmukhi"),
                    "roman_readable": roman.get("readable", ""),
                    "english": item.get("english"),
                    "part_of_speech": item.get("part_of_speech"),
                    "tags": tags,
                    "source": source,
                }
            )
        self._send_json(vocab_items)

    def _serve_proverbs(self):
        if not TOP_PROVERBS_FILE.exists():
            self._send_json(
                {"error": "top_100_proverbs.json not found — run select_top_proverbs.py first"},
                status=503,
            )
            return

        with open(TOP_PROVERBS_FILE, encoding="utf-8") as f:
            self._send_json(json.load(f))


def open_browser_after_delay(url):
    pid = os.fork()
    if pid == 0:
        try:
            subprocess.run(["/bin/sleep", "1"])
            webbrowser.open(url)
        finally:
            os._exit(0)


def main():
    print("Running test suite...")
    result = subprocess.run(
        [sys.executable, "-m", "review_tool.test_suite"],
        capture_output=True,
        text=True,
    )
    print(result.stdout, end="")
    if result.returncode != 0:
        print(result.stderr, end="", file=sys.stderr)
        print("Test suite failed. Fix issues before reviewing.", file=sys.stderr)
        sys.exit(1)

    url = f"http://localhost:{PORT}"
    print(f"Starting review server at {url}")
    server = http.server.HTTPServer(("localhost", PORT), ReviewToolHandler)
    open_browser_after_delay(url)
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping review server.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
