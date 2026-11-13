import assert from "node:assert/strict";
import test from "node:test";
import {
  classifyTemperature,
  applyForecastTemperature,
  applyTemperatureCardStatus,
  formatTemperature,
  riskStyle,
  temperatureBackgroundTone,
  temperatureStatusStyle,
} from "./temperatureStatus.js";
import { kikanMarkup } from "./legacy/kikanMarkup.js";

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

test("temperature status colors the complete monitor card and resets it to neutral", () => {
  const body = { dataset: { temperatureStatus: "cold" } };
  const page = { dataset: { temperatureStatus: "cold" } };
  const card = { dataset: {}, ownerDocument: { body, documentElement: page } };

  applyTemperatureCardStatus("Severe Cold", card);
  assert.equal(card.dataset.temperatureStatus, "cold");
  assert.equal(body.dataset.temperatureStatus, undefined);
  assert.equal(page.dataset.temperatureStatus, undefined);

  applyTemperatureCardStatus("Warm", card);
  assert.equal(card.dataset.temperatureStatus, "warm");

  applyTemperatureCardStatus("Unknown", card);
  assert.equal(card.dataset.temperatureStatus, "neutral");
});

test("forecast cold and warm risk results set the monitor card status", () => {
  const body = { dataset: {} };
  const page = { dataset: {} };
  const card = { dataset: {}, ownerDocument: { body, documentElement: page } };
  const cold = applyForecastTemperature(
    { risks: [{ hazard: "temperature", predicted_value: 11.72, risk_level: "Cold" }] },
    {},
    card,
  );
  assert.deepEqual(cold, { temperature: 11.72, temperatureStatus: "Cold" });
  assert.equal(card.dataset.temperatureStatus, "cold");

  const warm = applyForecastTemperature(
    { risks: [{ hazard: "temperature", predicted_value: 29, risk_level: "Warm" }] },
    {},
    card,
  );
  assert.deepEqual(warm, { temperature: 29, temperatureStatus: "Warm" });
  assert.equal(card.dataset.temperatureStatus, "warm");
});

test("the temperature status target contains the full Weather monitoring card", () => {
  const cardMarkup = kikanMarkup.match(
    /<div class="card monitor" id="monitor-card">([\s\S]*?)<\/div>\s*<\/div>\s*<div class="section-head">/,
  );
  assert.ok(cardMarkup);
  assert.match(cardMarkup[1], /Weather monitoring mode/);
  assert.match(cardMarkup[1], /class="[^"]*\btemperature-only\b/);
  assert.doesNotMatch(kikanMarkup, /monitor-risk-summary|Safety tips|tips-panel/);
  assert.match(kikanMarkup, /id="forecast-status" role="status"/);
});

test("monitor card backgrounds follow temperature status and respect theme and contrast", async () => {
  const { readFile } = await import("node:fs/promises");
  const stylesheet = await readFile(
    new URL("./legacy/kikan.css", import.meta.url),
    "utf8",
  );

  assert.match(stylesheet, /\.monitor\[data-temperature-status="cold"\]\{background:#DCEEFF!important;border-color:#93C5FD;\}/);
  assert.match(stylesheet, /\.monitor\[data-temperature-status="warm"\]\{background:#FFE5CC!important;border-color:#FDBA74;\}/);
  assert.match(stylesheet, /:root\[data-theme="dark"\] \.monitor\[data-temperature-status="cold"\]/);
  assert.match(stylesheet, /:root\[data-theme="dark"\] \.monitor\[data-temperature-status="warm"\]/);
  assert.match(stylesheet, /body\.access-contrast \.monitor\[data-temperature-status\]\{background:var\(--surface\)!important;border-color:#526071;\}/);
  assert.match(stylesheet, /html\{background:var\(--paper\);/);
  assert.match(stylesheet, /body\{background:var\(--paper\)!important;color:var\(--ink\)!important;/);
  assert.doesNotMatch(stylesheet, /(?:html|body)\[data-temperature-status/);
  assert.match(stylesheet, /\.risk-cold,[^{]+\{color:#2563EB!important;\}/);
  assert.match(stylesheet, /\.risk-warm,[^{]+\{color:#C2410C!important;\}/);
  assert.doesNotMatch(stylesheet, /\.risk-(?:cold|warm),[^{]+\{[^}]*background:/);
  assert.doesNotMatch(stylesheet, /\.risk-(?:cold|warm),[^{]+\{[^}]*border:/);
});
