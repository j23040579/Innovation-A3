import assert from "node:assert/strict";
import test from "node:test";
import { getChartDimensions, getNextVisibleWindow } from "./d3Charts.js";

test("chart dimensions fit narrow phone layouts without a desktop-width minimum", () => {
  assert.deepEqual(getChartDimensions(240, 190), { width: 240, height: 190 });
  assert.deepEqual(getChartDimensions(0, 0), { width: 520, height: 220 });
});

test("chart zoom actions move through the data and reset to the full range", () => {
  const zoomedIn = getNextVisibleWindow({ start: 0, count: 12 }, 12, "in");
  assert.deepEqual(zoomedIn, { start: 1, count: 10 });
  assert.deepEqual(getNextVisibleWindow(zoomedIn, 12, "in"), { start: 2, count: 8 });
  assert.deepEqual(getNextVisibleWindow(zoomedIn, 12, "out"), { start: 0, count: 12 });
  assert.deepEqual(getNextVisibleWindow(zoomedIn, 12, "reset"), { start: 0, count: 12 });
});

test("chart zoom stays within short data ranges and allows one-point series", () => {
  assert.deepEqual(getNextVisibleWindow({ start: 0, count: 2 }, 2, "in"), { start: 0, count: 2 });
  assert.deepEqual(getNextVisibleWindow({ start: 0, count: 2 }, 2, "out"), { start: 0, count: 2 });
  assert.deepEqual(getNextVisibleWindow({ start: 0, count: 1 }, 1, "in"), { start: 0, count: 1 });
});
