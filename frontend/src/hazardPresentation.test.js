import assert from "node:assert/strict";
import test from "node:test";
import {
  hazardCardPresentation,
  hazardMapColor,
  hazardSeverity,
  isSnowMapPrediction,
  mapHazardsForPrefecture,
  mapLegendTitle,
  nextMapHazardForPrefecture,
  shouldShowHazardCard,
} from "./hazardPresentation.js";

test("map colors use each backend hazard class and leave unknown results white", () => {
  assert.equal(hazardMapColor({ risk_level: "No/Minimal Rain" }), "#FED7AA");
  assert.equal(hazardMapColor({ risk_level: "Low" }), "#FED7AA");
  assert.equal(hazardMapColor({ risk_level: "Moderate" }), "#F59E0B");
  assert.equal(hazardMapColor({ risk_level: "High" }), "#C2410C");
  assert.equal(hazardMapColor({ risk_level: "Heavy Rain" }), "#C2410C");
  assert.equal(hazardMapColor({ risk_level: "Unassessed" }), "#FFFFFF");
});

test("typhoon profile matches determine the displayed class and map legend", () => {
  const typhoon = { risk_level: "Unassessed", profile_match_class: "High" };
  assert.equal(hazardSeverity(typhoon), "High");
  assert.equal(hazardMapColor(typhoon), "#C2410C");
  assert.equal(mapLegendTitle("typhoon", typhoon), "Typhoon profile match");
  assert.deepEqual(hazardCardPresentation({ hazard: "typhoon", ...typhoon }), {
    icon: "\u{1F300}",
    name: "Typhoon profile match",
    level: "High",
  });
  assert.equal(mapLegendTitle("typhoon", { risk_level: "High" }), "Typhoon risk");
});

test("snow selection follows Yamagata model coverage and only colors inference results", () => {
  const snowCoverage = new Set(["yamagata", "niigata"]);
  const supportedSnow = { execution_mode: "inference", risk_level: "Medium" };
  assert.equal(isSnowMapPrediction(supportedSnow), true);
  assert.equal(isSnowMapPrediction({ execution_mode: "mock", risk_level: "High" }), false);
  assert.deepEqual(mapHazardsForPrefecture("Yamagata", snowCoverage), ["typhoon", "flood", "rain", "snow"]);
  assert.deepEqual(mapHazardsForPrefecture("Tokyo", snowCoverage), ["typhoon", "flood", "rain"]);
  assert.equal(nextMapHazardForPrefecture("typhoon", "Yamagata", true), "snow");
  assert.equal(nextMapHazardForPrefecture("snow", "Tokyo", false), "typhoon");
  assert.equal(nextMapHazardForPrefecture("rain", "Niigata", true), "rain");
});

test("snow prediction cards are only shown for Yamagata", () => {
  const snowRisk = { hazard: "snow", risk_level: "High" };
  assert.equal(shouldShowHazardCard(snowRisk, "Yamagata"), true);
  assert.equal(shouldShowHazardCard(snowRisk, "Niigata"), false);
  assert.equal(shouldShowHazardCard({ hazard: "flood" }, "Niigata"), true);
});
