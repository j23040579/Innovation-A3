import assert from "node:assert/strict";
import test from "node:test";
import {
  FORECAST_LOADING_SELECTOR,
  setForecastLoading,
} from "./forecastLoading.js";

function createElement() {
  const attributes = new Map();
  return {
    attributes,
    setAttribute(name, value) {
      attributes.set(name, value);
    },
    removeAttribute(name) {
      attributes.delete(name);
    },
  };
}

test("forecast updates mark every refreshed component busy", () => {
  const selectors = [
    "#hazard-grid",
    "#stat-temp",
    "#mon-loc",
    "#map-risk-summary",
    "#chart-bar",
    "#chart-typhoon",
    "#chart-flood",
    "#chart-snow",
    ".map-shell",
  ];
  const elements = Array.from({ length: selectors.length }, createElement);

  setForecastLoading(elements, true);

  for (const element of elements) {
    assert.equal(element.attributes.get("aria-busy"), "true");
    assert.equal(element.attributes.get("data-forecast-loading"), "true");
  }
  assert.deepEqual(FORECAST_LOADING_SELECTOR.split(", "), selectors);
});

test("forecast updates clear loading attributes after completion", () => {
  const elements = Array.from({ length: 2 }, createElement);
  setForecastLoading(elements, true);

  setForecastLoading(elements, false);

  for (const element of elements) {
    assert.equal(element.attributes.has("aria-busy"), false);
    assert.equal(element.attributes.has("data-forecast-loading"), false);
  }
});

test("refresh feedback is a pulse animation and respects reduced motion", async () => {
  const { readFile } = await import("node:fs/promises");
  const stylesheet = await readFile(
    new URL("./legacy/kikan.css", import.meta.url),
    "utf8",
  );

  assert.match(stylesheet, /@keyframes forecast-refresh-pulse/);
  assert.match(stylesheet, /animation:forecast-refresh-pulse 1\.4s ease-in-out infinite/);
  assert.match(stylesheet, /@media\(prefers-reduced-motion:reduce\)/);
  assert.doesNotMatch(stylesheet, /content:\s*["'](?:Loading|Updating)/i);
});
