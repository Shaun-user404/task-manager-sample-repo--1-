"""Five data-driven UI checks for the catalogue search page."""
import json
import os
import threading
from pathlib import Path

import pytest
from http.server import ThreadingHTTPServer
from selenium import webdriver

from page_objects.catalog_page import CatalogPage
from web_app import make_handler

PROJECT_ROOT = Path(__file__).resolve().parents[1]
with (PROJECT_ROOT / "test_data" / "search_cases.json").open(encoding="utf-8") as data_file:
    SEARCH_CASES = json.load(data_file)


@pytest.fixture(scope="session")
def base_url():
    ui_drift = os.getenv("UI_DRIFT", "0") == "1"
    remote_browser = os.getenv("HEALENIUM", "0") == "1"
    bind_host = "0.0.0.0" if remote_browser else "127.0.0.1"
    server = ThreadingHTTPServer((bind_host, 0), make_handler(ui_drift))
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    _, port = server.server_address
    advertised_host = os.getenv("REMOTE_APP_HOST", "host.docker.internal") if remote_browser else "127.0.0.1"
    yield f"http://{advertised_host}:{port}"
    server.shutdown()
    server.server_close()
    server_thread.join(timeout=2)


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    healenium_enabled = os.getenv("HEALENIUM", "0") == "1"
    if not healenium_enabled:
        options.binary_location = os.getenv(
            "CHROME_BINARY", r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        )
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    if healenium_enabled:
        proxy_url = os.getenv("HEALENIUM_URL", "http://127.0.0.1:8085")
        browser = webdriver.Remote(command_executor=proxy_url, options=options)
    else:
        browser = webdriver.Chrome(options=options)

    browser.set_window_size(1280, 900)
    yield browser
    browser.quit()


@pytest.mark.parametrize(
    "case", SEARCH_CASES, ids=[case["case_id"] for case in SEARCH_CASES]
)
def test_catalog_search(case, driver, base_url):
    page = CatalogPage(driver, base_url).open().search(case["query"])
    results = page.result_texts()
    actual_titles = [result.split(" | ", maxsplit=1)[0] for result in results]

    assert actual_titles == case["expected_titles"]
    assert page.status_text() == case["expected_status"]
