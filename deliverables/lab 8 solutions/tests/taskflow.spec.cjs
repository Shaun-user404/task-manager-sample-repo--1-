const { test, expect } = require("@playwright/test");
const { pathToFileURL } = require("node:url");
const path = require("node:path");

const appUrl = pathToFileURL(path.resolve(__dirname, "..", "index.html")).href;

test("adds a task and clears it after completion", async ({ page }) => {
  await page.goto(appUrl);

  await page.getByLabel("Add a task").fill("Prepare release notes");
  await page.getByRole("button", { name: "Add task" }).click();
  await expect(page.getByText("Prepare release notes")).toBeVisible();
  await expect(page.locator("#remaining-count")).toHaveText("3");

  await page.getByLabel("Prepare release notes").check();
  await page.getByRole("button", { name: "Clear completed" }).click();
  await expect(page.getByText("Prepare release notes")).toHaveCount(0);
  await expect(page.locator("#remaining-count")).toHaveText("2");
});
