# Lab 8: Visual Regression and Accessibility

## Test target and setup

The repository contains a Python CLI, not a browser application. To provide a real browser target without changing the CLI, this lab includes a small, self-contained task-manager demo in this folder. Playwright captures the desktop screenshots and axe-core performs the WCAG scan.

The checks use Chromium at **1365 x 900**. Install dependencies with `npm install`, install the browser with `npx playwright install chromium`, and run the demo interaction test with `npm test`.

## Visual regression

The reference was captured before the deliberate layout adjustment. The change increased the app shell's top margin from **24px to 40px**. The resulting comparison reports:

| Page | Viewport | Changed pixels | Total pixels | Difference |
|---|---:|---:|---:|---:|
| Taskflow / My tasks | 1365 x 900 | 13,463 | 1,228,500 | **1.096%** |

- Baseline: [visual-baseline.png](./artifacts/visual-baseline.png)
- After deliberate change: [visual-after-change.png](./artifacts/visual-after-change.png)
- Pixel diff: [visual-diff.png](./artifacts/visual-diff.png)
- Machine-readable report: [visual-diff-report.json](./artifacts/visual-diff-report.json)

The detected change is the planned vertical offset; the screenshot dimensions and viewport are identical. No unexpected visual change was identified.

## Accessibility audit and triage

The initial scan was run before fixes. Axe reported two violations:

| Rule | WCAG level / criterion | Impact | Initial finding | Resolution |
|---|---|---|---|---|
| `image-alt` | A / 1.1.1 Non-text Content | Critical | Brand mark image had no `alt` attribute. | Marked the logo image decorative with `alt=""`; its link already has the accessible name “Taskflow home.” |
| `color-contrast` | AA / 1.4.3 Contrast (Minimum) | Serious | Muted text contrast was 2.11:1 on the page and 2.27:1 on the card, below the 4.5:1 requirement. | Changed muted text from `#a6acb8` to `#626b7a`, which provides at least 4.98:1 against the tested surfaces. |

Reports:

- Before fixes: [accessibility-before.json](./artifacts/accessibility-before.json)
- After fixes: [accessibility-after.json](./artifacts/accessibility-after.json)
- After-fix screenshot: [accessibility-after.png](./artifacts/accessibility-after.png)

The after-fix scan reports **0 violations** for the selected WCAG 2.0/2.1 A/AA ruleset. Both findings are resolved.

## Reproduce

Run these commands from this folder:

```bash
npm install
npx playwright install chromium
npm test
npm run visual:baseline
npm run a11y:before
```

To recreate the captured initial state, temporarily restore the app-shell top margin to `24px`, muted text to `#a6acb8`, and remove the logo image's `alt` attribute. Then run the baseline and before-audit commands above. Restore the final values (`40px`, `#626b7a`, and `alt=""`) and run:

```bash
npm run visual:compare
npm run a11y:after
```

`npm run a11y:before` allows the expected initial violations and writes the full axe result JSON. `npm run a11y:after` exits unsuccessfully if any violations remain.
