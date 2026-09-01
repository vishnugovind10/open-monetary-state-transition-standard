import { expect, test } from "@playwright/test";

test("loads the Explorer dashboard and primary panels", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "OMST Explorer" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Settlement Evaluator" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Money Graph" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Conformance Status" })).toBeVisible();
  await expect(page.getByText("All examples are synthetic.")).toBeVisible();
});

test("updates settlement verdict when stressed liquidity is selected", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel("Settlement amount").fill("95000000");
  await page.getByLabel("Stress context").selectOption("liquidity-shock");
  await expect(page.getByText("CONSTRAINED")).toBeVisible();
  await expect(page.getByText("Required liquidity exceeds stressed available liquidity")).toBeVisible();
});

test("supports equivalence, graph and conformance navigation", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Equivalence" }).click();
  await expect(page.locator("[aria-label='Equivalence workspace']")).toBeVisible();
  await page.getByRole("button", { name: "Money Graph" }).click();
  await page.locator(".graph-canvas").getByRole("button", { name: "EUR-Z", exact: true }).click();
  await expect(page.getByLabel("Source instrument")).toHaveValue("EUR-Z");
  await page.getByRole("button", { name: "Conformance" }).click();
  await expect(page.getByRole("cell", { name: "Partial" }).first()).toBeVisible();
});
