# Healenium Healing Report

## Execution Status

**Not executed in this environment.** Docker/Docker Compose is unavailable, so the Healenium backend, Selenium Grid, and proxy could not be started. No proxy-mode run, healing decision, dashboard entry, or wrong-target observation is claimed.

| Measure | Result |
|---|---|
| Direct baseline | 5/5 passed (`baseline_direct.xml`) |
| Direct run after controlled locator drift | 0/5 passed; 5/5 failed (`drift_direct.xml`) |
| Healenium seed run on unchanged UI | Not run: Docker unavailable |
| Healenium run after drift | Not run: Docker unavailable |
| Healing success rate | N/A; zero proxy-mode test executions |
| Incorrectly healed elements | Not evaluated |

The direct drift failures are expected locator failures: the Page Object looks for `id=catalog-search`, while the drifted page uses `id=catalog-search-v2`. This confirms the test is sensitive to the intentional change; it does not demonstrate self-healing.

## Required Follow-up Execution

From this folder, start the included stack with `docker compose up -d`. Run the suite through the proxy once with `HEALENIUM=1` and `UI_DRIFT=0` to collect baseline selectors. Then rerun with `HEALENIUM=1` and `UI_DRIFT=1`. Save the outputs as `healenium_seed.xml` and `healenium_drift.xml`, inspect `http://localhost:7878/healenium/report/`, and update this report with the observed healed locator and whether it selected the correct search input.

Calculate success rate as:

`number of drift-affected test cases that self-heal to the correct element / number of drift-affected test cases executed through Healenium * 100%`

A test that passes by selecting a different or semantically wrong element must be counted as an incorrect healing, not a success.
