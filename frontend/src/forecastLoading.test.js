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
