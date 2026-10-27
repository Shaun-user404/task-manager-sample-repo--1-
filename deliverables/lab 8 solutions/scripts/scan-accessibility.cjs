const fs = require("node:fs");
const path = require("node:path");
const { pathToFileURL } = require("node:url");
const { chromium } = require("@playwright/test");
const axeSource = require("axe-core").source;

const outputName = process.argv.find((argument) => argument.endsWith(".json"));
const allowViolations = process.argv.includes("--allow-violations");
if (!outputName) {
  throw new Error("Pass the output JSON path as an argument.");
}

async function main() {
  const root = path.resolve(__dirname, "..");
  const outputPath = path.resolve(root, outputName);
  const screenshotPath = outputPath.replace(/\.json$/i, ".png");
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });

  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage({
      viewport: { width: 1365, height: 900 },
      deviceScaleFactor: 1,
    });
    await page.goto(pathToFileURL(path.join(root, "index.html")).href);
    await page.screenshot({ path: screenshotPath });
    await page.addScriptTag({ content: axeSource });
    const results = await page.evaluate(async () =>
      window.axe.run(document, {
        runOnly: {
          type: "tag",
          values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"],
        },
      })
    );
    const report = {
      page: "Taskflow | My tasks",
      viewport: { width: 1365, height: 900 },
      scannedAt: new Date().toISOString(),
      screenshot: path.relative(root, screenshotPath),
      violationCount: results.violations.length,
      violations: results.violations,
      passes: results.passes.length,
      incomplete: results.incomplete,
    };
    fs.writeFileSync(outputPath, `${JSON.stringify(report, null, 2)}\n`);
    console.log(
      JSON.stringify(
        {
          report: path.relative(root, outputPath),
          violationCount: report.violationCount,
          violations: results.violations.map(({ id, impact, tags }) => ({
            id,
            impact,
            wcag: tags.filter((tag) => tag.startsWith("wcag")),
          })),
        },
        null,
        2
      )
    );

    if (report.violationCount && !allowViolations) {
      process.exitCode = 1;
    }
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
