const fs = require("node:fs");
const path = require("node:path");
const { pathToFileURL } = require("node:url");
const { chromium } = require("@playwright/test");
const pixelmatch = require("pixelmatch").default;
const { PNG } = require("pngjs");

const root = path.resolve(__dirname, "..");
const artifacts = path.join(root, "artifacts");
const baselinePath = path.join(artifacts, "visual-baseline.png");
const currentPath = path.join(artifacts, "visual-after-change.png");
const diffPath = path.join(artifacts, "visual-diff.png");
const reportPath = path.join(artifacts, "visual-diff-report.json");
const isBaseline = process.argv.includes("--baseline");

async function main() {
  fs.mkdirSync(artifacts, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage({
      viewport: { width: 1365, height: 900 },
      deviceScaleFactor: 1,
    });
    await page.goto(pathToFileURL(path.join(root, "index.html")).href);
    await page.screenshot({ path: isBaseline ? baselinePath : currentPath });

    if (isBaseline) {
      console.log(`Baseline captured: ${baselinePath}`);
      return;
    }

    if (!fs.existsSync(baselinePath)) {
      throw new Error("Missing baseline. Run npm run visual:baseline first.");
    }

    const baseline = PNG.sync.read(fs.readFileSync(baselinePath));
    const current = PNG.sync.read(fs.readFileSync(currentPath));
    if (baseline.width !== current.width || baseline.height !== current.height) {
      throw new Error("Screenshot dimensions differ; use the same viewport for both captures.");
    }

    const diff = new PNG({ width: baseline.width, height: baseline.height });
    const differentPixels = pixelmatch(
      baseline.data,
      current.data,
      diff.data,
      baseline.width,
      baseline.height,
      { threshold: 0.1 }
    );
    fs.writeFileSync(diffPath, PNG.sync.write(diff));
    const report = {
      baseline: path.basename(baselinePath),
      comparison: path.basename(currentPath),
      diffImage: path.basename(diffPath),
      viewport: { width: baseline.width, height: baseline.height },
      differentPixels,
      totalPixels: baseline.width * baseline.height,
      differencePercent: Number(
        ((differentPixels / (baseline.width * baseline.height)) * 100).toFixed(3)
      ),
      deliberateChange: "Increased the top margin of the app shell from 24px to 40px.",
    };
    fs.writeFileSync(reportPath, `${JSON.stringify(report, null, 2)}\n`);
    console.log(JSON.stringify(report, null, 2));
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
