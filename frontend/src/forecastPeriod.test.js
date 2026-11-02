import assert from "node:assert/strict";
import test from "node:test";
import { getTomorrowISODate, resolveForecastPeriod } from "./forecastPeriod.js";

test("map selections reuse the previously applied date interval", () => {
  assert.deepEqual(
    resolveForecastPeriod({ from: "2027-01-31", to: "2027-03-28" }, "2027-04-01"),
    { startDate: "2027-01-31", endDate: "2027-03-28" },
  );
});

test("map selections target tomorrow when no interval has been applied", () => {
  assert.deepEqual(resolveForecastPeriod(null, "2027-04-01"), {
    startDate: "2027-04-01",
    endDate: "2027-04-01",
  });
});

test("tomorrow is calculated in Japan's calendar across month and year boundaries", () => {
  assert.equal(getTomorrowISODate(new Date("2026-12-31T15:00:00.000Z")), "2027-01-02");
});
