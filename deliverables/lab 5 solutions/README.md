# Lab 5: Selenium Page Objects and Healenium

This folder contains a self-contained catalogue-search demo because the supplied task-manager repository has no browser UI. The demo, test code, test data, and controlled DOM drift are isolated here.

## Suite

- `web_app.py` serves a small searchable catalogue for the tests.
- `page_objects/catalog_page.py` owns the page locators and actions.
- `tests/test_catalog_search.py` runs five cases from `test_data/search_cases.json`.
- `UI_DRIFT=1` changes the search field ID from `catalog-search` to `catalog-search-v2`; the Page Object intentionally retains its original locator.
- `HEALENIUM=1` routes Selenium through the Healenium proxy at `http://127.0.0.1:8085`.

## Run the direct baseline and drift experiment

From this folder in PowerShell:

```powershell
python -m pip install -r requirements.txt
$env:UI_DRIFT = '0'
Remove-Item Env:HEALENIUM -ErrorAction SilentlyContinue
python -m pytest -q --junitxml=reports/baseline_direct.xml
$env:UI_DRIFT = '1'
python -m pytest -q --junitxml=reports/drift_direct.xml
```

The checked-in run reports are `reports/baseline_direct.xml` and `reports/drift_direct.xml`, with readable console summaries in the adjacent `.txt` files. Direct baseline: 5 passed. Drift without Healenium: 5 failed at the Page Object's search-field wait because `#catalog-search` no longer exists.

## Run Healenium

Docker Desktop and Docker Compose must be running. The compose definition is adapted from the official Healenium self-hosted Selenium Grid setup. Start it from this folder:

```powershell
docker compose up -d
```

First run the unchanged UI **through the proxy** so Healenium can collect reference selectors, then turn on drift and repeat the same suite:

```powershell
$env:HEALENIUM = '1'
$env:UI_DRIFT = '0'
python -m pytest -q --junitxml=reports/healenium_seed.xml
$env:UI_DRIFT = '1'
python -m pytest -q --junitxml=reports/healenium_drift.xml
```

The app fixture binds to all interfaces in proxy mode and advertises `host.docker.internal` to the Chrome container; override with `REMOTE_APP_HOST` if the Docker host uses a different name. Review the Healenium report at `http://localhost:7878/healenium/report/` and proxy debug logs before marking a test healed. Record the failed locator, healed locator, confidence score, screenshot, and whether the selected element is correct. Do not assume a green test alone proves the healing target was correct.

## Reports and limitations

- `reports/baseline_direct.*`: executed direct-browser baseline.
- `reports/drift_direct.*`: executed direct-browser run after the controlled locator change.
- `reports/healenium_report.md`: healing observations and status. Docker was unavailable in the authoring environment, so no proxy run or healing decision is claimed.

Official references: [Healenium self-hosted proxy install](https://healenium.io/docs/download_and_install/hlm_proxy), [Healenium report](https://healenium.io/docs/report), and [official Python example](https://github.com/healenium/healenium-example-python).
