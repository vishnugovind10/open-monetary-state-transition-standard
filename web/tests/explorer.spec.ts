import { expect, test } from "@playwright/test";

test("loads the Explorer dashboard and primary panels", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "OMST Explorer" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Settlement Compatibility" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Money Graph" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Conformance Status" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Profiles" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Settlement Exchange" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Adapters" })).toBeVisible();
  await expect(page.getByText("COMPATIBLE").first()).toBeVisible();
  await expect(page.getByText("All examples are synthetic.")).toBeVisible();
});

test("updates settlement verdict when stressed liquidity is selected", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel("Source instrument").selectOption("EUR-Y");
  await expect(page.getByText("CONDITIONALLY_COMPATIBLE")).toBeVisible();
  await expect(page.getByText("LIQUIDITY_EVIDENCE_STALE")).toBeVisible();
  await page.getByLabel("Source instrument").selectOption("EUR-Z");
  await expect(page.getByText("INCOMPATIBLE").first()).toBeVisible();
  await expect(page.getByText("FINALITY_MISMATCH")).toBeVisible();
});

test("supports equivalence, graph and conformance navigation", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Compare" }).click();
  await expect(page.locator("[aria-label='Compare workspace']")).toBeVisible();
  await page.getByRole("button", { name: "Graph" }).click();
  await page.locator(".graph-canvas").getByRole("button", { name: "EUR-Z", exact: true }).click();
  await expect(page.getByLabel("Source instrument")).toHaveValue("EUR-Z");
  await page.getByRole("button", { name: "Conformance" }).click();
  await expect(page.getByRole("cell", { name: "Partial" }).first()).toBeVisible();
  await page.getByRole("button", { name: "Profiles" }).click();
  await expect(page.locator("[aria-label='Profiles workspace']")).toBeVisible();
  await page.getByRole("button", { name: "Adapters" }).click();
  await expect(page.getByRole("cell", { name: "ISO 20022" })).toBeVisible();
});
