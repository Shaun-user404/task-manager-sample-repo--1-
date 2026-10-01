"""Minimal catalogue search page used by the Lab 5 UI tests."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

BOOKS = [
    {"title": "The Hobbit", "author": "J. R. R. Tolkien", "isbn": "9780547928227"},
    {"title": "The Left Hand of Darkness", "author": "Ursula K. Le Guin", "isbn": "9780441478125"},
    {"title": "A Wizard of Earthsea", "author": "Ursula K. Le Guin", "isbn": "9780547773742"},
    {"title": "Clean Code", "author": "Robert C. Martin", "isbn": "9780132350884"},
]


def page_html(ui_drift=False):
    search_id = "catalog-search-v2" if ui_drift else "catalog-search"
    books_json = json.dumps(BOOKS).replace("</", "<\\/")
    return f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Library catalogue</title></head>
<body>
  <main>
    <h1>Library catalogue</h1>
    <label for="{search_id}">Search title, author, or ISBN</label>
    <input id="{search_id}" type="search" aria-label="Search title, author, or ISBN">
    <button id="search-submit" type="button">Search</button>
    <p id="search-status" aria-live="polite"></p>
    <ul id="search-results" aria-label="Search results"></ul>
  </main>
  <script>
    const books = {books_json};
    const input = document.getElementById("{search_id}");
    const results = document.getElementById("search-results");
    const status = document.getElementById("search-status");
    document.getElementById("search-submit").addEventListener("click", () => {{
      const query = input.value.trim().toLowerCase();
      const matches = query ? books.filter(book =>
        Object.values(book).some(value => value.toLowerCase().includes(query))
      ) : [];
      results.replaceChildren(...matches.map(book => {{
        const item = document.createElement("li");
        item.className = "book-result";
        item.textContent = `${{book.title}} | ${{book.author}} | ${{book.isbn}}`;
        return item;
      }}));
      status.textContent = matches.length ? `${{matches.length}} result(s)` : "No results found";
    }});
  </script>
</body>
</html>"""


def make_handler(ui_drift=False):
    class CatalogHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            body = page_html(ui_drift).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format, *args):
            return

    return CatalogHandler


def serve():
    drift_enabled = os.getenv("UI_DRIFT", "0") == "1"
    server = ThreadingHTTPServer(("127.0.0.1", 8000), make_handler(drift_enabled))
    mode = "drifted" if drift_enabled else "baseline"
    print(f"Serving {mode} catalogue at http://127.0.0.1:8000", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    serve()
