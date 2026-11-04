export const riskColors = {
  low: { className: "risk-low", color: "#FED7AA" },
  "no/minimal rain": { className: "risk-low", color: "#FED7AA" },
  "no rain": { className: "risk-low", color: "#FED7AA" },
  none: { className: "risk-low", color: "#FED7AA" },
  mild: { className: "risk-low", color: "#FED7AA" },
  moderate: { className: "risk-medium", color: "#F59E0B" },
  medium: { className: "risk-medium", color: "#F59E0B" },
  cold: { className: "risk-cold", color: "#38BDF8" },
  "light freeze": { className: "risk-cold", color: "#7DD3FC" },
  "hard freeze": { className: "risk-cold", color: "#0284C7" },
  "severe cold": { className: "risk-cold", color: "#0369A1" },
  frozen: { className: "risk-cold", color: "#0C4A6E" },
  warm: { className: "risk-warm", color: "#F59E0B" },
  high: { className: "risk-high", color: "#C2410C" },
  critical: { className: "risk-high", color: "#9A3412" },
  unassessed: { className: "risk-unassessed", color: "var(--ink-soft)" },
};

export function classifyTemperature(tempC) {
  const value = Number(tempC);
  if (!Number.isFinite(value)) return "Unknown";
  if (value <= -18) return "Frozen";
  if (value <= -5) return "Severe Cold";
  if (value < -2.2) return "Hard Freeze";
  if (value <= 0) return "Light Freeze";
  if (value <= 16) return "Cold";
  if (value < 27) return "Mild";
  return "Warm";
}

export function formatTemperature(tempC, status) {
  const value = Number(tempC);
  if (!Number.isFinite(value)) return "—";
  const label = status && status !== "Unknown" ? status : classifyTemperature(value);
  return `${value.toFixed(2)}°C (${label})`;
}

export function riskStyle(level) {
  return riskColors[String(level || "unknown").toLowerCase()] || {
    className: "risk-medium",
    color: "#FFFFFF",
  };
}

export function temperatureStatusStyle(level) {
  const normalized = String(level || "unknown").trim().toLowerCase();

  if (normalized.includes("cold") || normalized.includes("freeze")) {
    return { className: "risk-cold", color: "#2563EB" };
  }
  if (normalized.includes("warm") || normalized.includes("mild")) {
    return { className: "risk-warm", color: "#F97316" };
  }

  const style = riskColors[normalized];
  if (style) return style;

  return riskStyle(level);
}

export function temperatureBackgroundTone(level) {
  const normalized = String(level || "unknown").trim().toLowerCase();
  if (
    normalized.includes("cold") ||
    normalized.includes("freez") ||
    normalized === "frozen"
  ) {
    return "cold";
  }
  if (normalized.includes("warm") || normalized.includes("mild")) return "warm";
  return "neutral";
}

export function applyTemperatureBackground(level, body = document.body) {
  const tone = temperatureBackgroundTone(level);
  body.dataset.temperatureStatus = tone;
  const page = body.ownerDocument?.documentElement;
  if (page) page.dataset.temperatureStatus = tone;
}

export function applyForecastTemperature(prediction, daily, body = document.body) {
  const tempRisk = prediction.risks?.find((risk) => risk.hazard === "temperature");
  const temperature =
    tempRisk?.predicted_value ?? daily.metrics?.temperature_2m_max ?? daily.metrics?.temperature_mean;
  const temperatureStatus = tempRisk?.risk_level || classifyTemperature(temperature);
  applyTemperatureBackground(temperatureStatus, body);
  return { temperature, temperatureStatus };
}
