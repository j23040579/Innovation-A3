import assert from "node:assert/strict";
import test from "node:test";
import {
  classifyTemperature,
  applyForecastTemperature,
  applyTemperatureBackground,
  formatTemperature,
  riskStyle,
  temperatureBackgroundTone,
  temperatureStatusStyle,
} from "./temperatureStatus.js";

test("temperature labels keep cold statuses blue and warm statuses orange", () => {
  assert.equal(classifyTemperature(-10), "Severe Cold");
  assert.equal(classifyTemperature(4), "Cold");
  assert.equal(classifyTemperature(23), "Mild");
  assert.equal(classifyTemperature(30), "Warm");

  assert.equal(temperatureStatusStyle("Severe Cold").className, "risk-cold");
  assert.equal(temperatureStatusStyle("Cold").className, "risk-cold");
  assert.equal(temperatureStatusStyle("Mild").className, "risk-warm");
  assert.equal(temperatureStatusStyle("Warm").className, "risk-warm");
  assert.equal(temperatureStatusStyle("Unknown").className, "risk-medium");
  assert.equal(temperatureBackgroundTone("Frozen"), "cold");
  assert.equal(temperatureBackgroundTone("Light Freeze"), "cold");
  assert.equal(temperatureBackgroundTone("Mild"), "warm");
  assert.equal(temperatureBackgroundTone("Warm"), "warm");
  assert.equal(temperatureBackgroundTone("Unknown"), "neutral");
  assert.equal(temperatureBackgroundTone("Unassessed"), "neutral");
  assert.equal(riskStyle("High").className, "risk-high");
  assert.equal(formatTemperature(9.5, "Cold"), "9.50°C (Cold)");
});

test("temperature background application updates the visible page canvas and resets to neutral", () => {
  const page = { dataset: {} };
  const body = { dataset: {}, ownerDocument: { documentElement: page } };

  applyTemperatureBackground("Severe Cold", body);
  assert.equal(body.dataset.temperatureStatus, "cold");
  assert.equal(page.dataset.temperatureStatus, "cold");

  applyTemperatureBackground("Warm", body);
  assert.equal(body.dataset.temperatureStatus, "warm");
  assert.equal(page.dataset.temperatureStatus, "warm");

  applyTemperatureBackground("Unknown", body);
  assert.equal(body.dataset.temperatureStatus, "neutral");
  assert.equal(page.dataset.temperatureStatus, "neutral");
});

test("forecast cold and warm risk results set the visible page canvas status", () => {
  const page = { dataset: {} };
  const body = { dataset: {}, ownerDocument: { documentElement: page } };
  const cold = applyForecastTemperature(
    { risks: [{ hazard: "temperature", predicted_value: 11.72, risk_level: "Cold" }] },
    {},
    body,
  );
  assert.deepEqual(cold, { temperature: 11.72, temperatureStatus: "Cold" });
  assert.equal(page.dataset.temperatureStatus, "cold");

  const warm = applyForecastTemperature(
    { risks: [{ hazard: "temperature", predicted_value: 29, risk_level: "Warm" }] },
    {},
    body,
  );
  assert.deepEqual(warm, { temperature: 29, temperatureStatus: "Warm" });
  assert.equal(page.dataset.temperatureStatus, "warm");
});

test("page background uses theme-aware cold and warm colors and respects contrast settings", async () => {
  const { readFile } = await import("node:fs/promises");
  const stylesheet = await readFile(
    new URL("./legacy/kikan.css", import.meta.url),
    "utf8",
  );

  assert.match(stylesheet, /html\[data-temperature-status="cold"\]\{--temperature-page-background:#DCEEFF;\}/);
  assert.match(stylesheet, /html\[data-temperature-status="warm"\]\{--temperature-page-background:#FFE5CC;\}/);
  assert.match(stylesheet, /html\{background:var\(--temperature-page-background,var\(--paper\)\);/);
  assert.match(stylesheet, /:root\[data-theme="dark"\]\[data-temperature-status="cold"\]/);
  assert.match(stylesheet, /:root\[data-theme="dark"\]\[data-temperature-status="warm"\]/);
  assert.match(stylesheet, /html\[data-access-contrast="true"\]\[data-temperature-status\]\{--temperature-page-background:#fff;\}/);
  assert.match(stylesheet, /body\.access-contrast\[data-temperature-status\]\{--temperature-page-background:var\(--paper\);\}/);
  assert.match(stylesheet, /body\{background:var\(--temperature-page-background,var\(--paper\)\)!important;color:var\(--ink\)!important;/);
  assert.match(stylesheet, /\.risk-cold,[^{]+\{color:#2563EB!important;\}/);
  assert.match(stylesheet, /\.risk-warm,[^{]+\{color:#C2410C!important;\}/);
  assert.doesNotMatch(stylesheet, /\.risk-(?:cold|warm),[^{]+\{[^}]*background:/);
  assert.doesNotMatch(stylesheet, /\.risk-(?:cold|warm),[^{]+\{[^}]*border:/);
});
