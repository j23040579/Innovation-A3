const RISK_COLORS = {
  Low: "#FED7AA",
  Medium: "#F59E0B",
  High: "#C2410C",
};

const HAZARD_LABELS = {
  flood: "Flood",
  rain: "Heavy rain",
  snow: "Heavy snow",
  temperature: "Temperature",
  typhoon: "Typhoon",
  wind: "Wind",
};

const HAZARD_ICONS = {
  flood: "\u{1F3E2}",
  rain: "\u{1F327}\uFE0F",
  snow: "\u2744\uFE0F",
  temperature: "\u{1F321}\uFE0F",
  typhoon: "\u{1F300}",
  wind: "\u{1F32C}\uFE0F",
};

function normalizeLevel(value) {
  return String(value || "").trim().toLowerCase().replace(/[\s_-]+/g, " ");
}

export function normalizePrefecture(value) {
  return String(value || "").toLowerCase().replace(/[^a-z0-9]/g, "");
}

export function mapHazardsForPrefecture(prefecture, snowCoverage) {
  const hazards = ["typhoon", "flood", "rain"];
  if (snowCoverage.has(normalizePrefecture(prefecture))) hazards.push("snow");
  return hazards;
}

export function hazardSeverity(risk) {
  const level = normalizeLevel(risk?.profile_match_class || risk?.risk_level);
  if (["low", "no/minimal rain", "no rain", "none", "light", "light rain"].includes(level)) {
    return "Low";
  }
  if (["medium", "moderate", "moderate rain"].includes(level)) return "Medium";
  if (
    ["high", "critical", "heavy", "heavy rain", "very heavy rain", "extreme", "extreme rain"].includes(level)
  ) {
    return "High";
  }
  return null;
}

export function hazardMapColor(risk) {
  return RISK_COLORS[hazardSeverity(risk)] || "#FFFFFF";
}

export function mapLegendTitle(hazard, risk) {
  if (hazard === "typhoon" && risk?.profile_match_class) return "Typhoon profile match";
  return `${HAZARD_LABELS[hazard] || "Disaster"} risk`;
}

export function isSnowMapPrediction(prediction) {
  return (
    prediction?.execution_mode === "inference" &&
    ["Low", "Medium", "High"].includes(hazardSeverity(prediction))
  );
}

export function nextMapHazardForPrefecture(currentHazard, prefecture, snowAvailable) {
  if (normalizePrefecture(prefecture) === "yamagata" && snowAvailable) return "snow";
  if (currentHazard === "snow" && !snowAvailable) return "typhoon";
  return currentHazard;
}

export function shouldShowHazardCard(risk, prefecture) {
  return risk?.hazard !== "snow" || normalizePrefecture(prefecture) === "yamagata";
}

export function hazardCardPresentation(risk) {
  const hazard = String(risk?.hazard || "").toLowerCase();
  return {
    icon: HAZARD_ICONS[hazard] || "\u{1F6E1}\uFE0F",
    name:
      hazard === "typhoon" && risk?.profile_match_class
        ? "Typhoon profile match"
        : HAZARD_LABELS[hazard] || risk?.hazard || "Unknown hazard",
    level: risk?.profile_match_class || risk?.risk_level || "Unknown",
  };
}
