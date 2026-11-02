import { useEffect, useRef } from "react";
import * as d3 from "d3";
import { kikanMarkup } from "./legacy/kikanMarkup";
import { kikanLegacy } from "./legacy/kikanLegacy";
import { api } from "./api";
import "./legacy/kikan.css";

const riskColors = {
  low: { className: "risk-low", color: "#FED7AA" },
  mild: { className: "risk-low", color: "#FED7AA" },
  moderate: { className: "risk-medium", color: "#F59E0B" },
  medium: { className: "risk-medium", color: "#F59E0B" },
  cold: { className: "risk-medium", color: "#38BDF8" },
  "light freeze": { className: "risk-medium", color: "#7DD3FC" },
  "hard freeze": { className: "risk-high", color: "#0284C7" },
  "severe cold": { className: "risk-high", color: "#0369A1" },
  frozen: { className: "risk-high", color: "#0C4A6E" },
  warm: { className: "risk-medium", color: "#F59E0B" },
  high: { className: "risk-high", color: "#C2410C" },
  critical: { className: "risk-high", color: "#9A3412" },
};

function classifyTemperature(tempC) {
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

function formatTemperature(tempC, status) {
  const value = Number(tempC);
  if (!Number.isFinite(value)) return "—";
  const label = status && status !== "Unknown" ? status : classifyTemperature(value);
  return `${value.toFixed(2)}°C (${label})`;
}

function riskStyle(level) {
  return riskColors[String(level || "unknown").toLowerCase()] || {
    className: "risk-medium",
    color: "#FFFFFF",
  };
}

function setStatus(message, isError = false) {
  const status = document.getElementById("monitor-risk-summary");
  if (!status) return;
  status.textContent = message;
  status.dataset.state = isError ? "error" : "ready";
}

function renderRisks(risks = []) {
  const grid = document.getElementById("hazard-grid");
  if (!grid) return;
  grid.replaceChildren();
  risks.forEach((risk) => {
    const style = riskStyle(risk.risk_level);
    const percentage = Math.max(0, Math.min(100, Number(risk.probability || 0) * 100));
    const card = document.createElement("div");
    card.className = "card hazard";
    const top = document.createElement("div");
    top.className = "hazard-top";
    const name = document.createElement("span");
    name.className = "hazard-name";
    name.textContent = risk.hazard || "Unknown hazard";
    const level = document.createElement("span");
    level.className = `hazard-level ${style.className}`;
    level.textContent =
      risk.hazard === "temperature" && risk.predicted_value != null
        ? formatTemperature(risk.predicted_value, risk.risk_level)
        : risk.risk_level || "Unknown";
    top.append(name, level);
    const track = document.createElement("div");
    track.className = "bar-track";
    const fill = document.createElement("div");
    fill.className = "bar-fill";
    fill.style.width = `${percentage}%`;
    fill.style.background = style.color;
    track.appendChild(fill);
    const message = document.createElement("small");
    message.textContent = risk.alert_message || "Live backend prediction";
    card.append(top, track, message);
    grid.appendChild(card);
  });
}

function renderTimeseries(series = []) {
  const containers = ["chart-bar", "chart-typhoon", "chart-flood", "chart-landslide", "chart-snow"];
  const values = {
    "chart-bar": (point) => point.temperature_mean,
    "chart-typhoon": (point) => point.wind_speed_max,
    "chart-flood": (point) => point.rain_sum,
    "chart-landslide": (point) => point.rain_sum,
    "chart-snow": (point) => point.snowfall_sum,
  };
  containers.forEach((id) => {
    const container = document.getElementById(id);
    if (!container) return;
    const data = series.map((point) => ({ date: point.date, value: Number(values[id](point) || 0) }));
    container.replaceChildren();
    if (!data.length) return;
    const width = Math.max(280, container.clientWidth || 520);
    const height = Math.max(190, container.clientHeight || 220);
    const margin = { top: 14, right: 14, bottom: 36, left: 44 };
    const x = d3
      .scalePoint()
      .domain(data.map((point) => point.date))
      .range([margin.left, width - margin.right]);
    const y = d3
      .scaleLinear()
      .domain([0, d3.max(data, (point) => point.value) || 1])
      .nice()
      .range([height - margin.bottom, margin.top]);
    const svg = d3
      .select(container)
      .append("svg")
      .attr("viewBox", `0 0 ${width} ${height}`)
      .attr("role", "img")
      .attr("aria-label", "Live backend weather time series");
    svg
      .append("path")
      .datum(data)
      .attr("fill", "none")
      .attr("stroke", "#2563EB")
      .attr("stroke-width", 2.5)
      .attr("d", d3.line().x((point) => x(point.date)).y((point) => y(point.value)));
    svg
      .append("g")
      .attr("transform", `translate(0,${height - margin.bottom})`)
      .call(d3.axisBottom(x).ticks(Math.min(6, data.length)));
    svg.append("g").attr("transform", `translate(${margin.left},0)`).call(d3.axisLeft(y).ticks(5));
  });
}

function applyMapOverview(items = []) {
  const normalize = (value) => String(value || "").toLowerCase().replace(/[^a-z0-9]/g, "");
  const byPrefecture = new Map(items.map((item) => [normalize(item.prefecture), item]));
  document.querySelectorAll(".pref").forEach((path) => {
    const item =
      byPrefecture.get(normalize(path.getAttribute("aria-label"))) ||
      byPrefecture.get(normalize(path.dataset.id));
    if (!item) return;
    const style = riskStyle(item.primary_risk_level);
    path.style.fill = style.color;
    path.style.opacity = "0.85";
    path.style.stroke = "#FFFFFF";
  });
}

async function initializeApiIntegration() {
  const checkButton = document.getElementById("check-risk-btn");
  checkButton?.addEventListener(
    "click",
    async (event) => {
      event.preventDefault();
      event.stopImmediatePropagation();
      const prefecture = document.getElementById("loc-input")?.value.trim();
      const startDate = document.getElementById("from-date")?.value;
      const endDate = document.getElementById("to-date")?.value;
      if (!prefecture || !startDate || !endDate || startDate > endDate) {
        setStatus("Choose a prefecture and a valid date range.", true);
        return;
      }
      checkButton.disabled = true;
      setStatus("Loading live weather and risk data…");
      try {
        const [prediction, daily, timeseries] = await Promise.all([
          api.predict({ prefecture, date: endDate }),
          api.getDaily({ prefecture, date: endDate }),
          api.getTimeseries({ prefecture, startDate, endDate }),
        ]);
        renderRisks(prediction.risks);
        renderTimeseries(timeseries.series);
        const tempRisk = prediction.risks?.find((risk) => risk.hazard === "temperature");
        const temperature =
          tempRisk?.predicted_value ?? daily.metrics?.temperature_2m_max ?? daily.metrics?.temperature_mean;
        const tempEl = document.getElementById("stat-temp");
        if (temperature !== undefined && tempEl) {
          tempEl.textContent = formatTemperature(temperature, tempRisk?.risk_level);
        }
        const locationSummary = document.getElementById("mon-loc");
        if (locationSummary) {
          locationSummary.replaceChildren("Monitoring live weather for ", Object.assign(document.createElement("strong"), { textContent: prefecture }));
        }
        document.getElementById("map-summary-name").textContent = prefecture;
        document.getElementById("map-summary-hazard").textContent = prediction.overall_risk_level || "Unknown";
        setStatus(`Live backend data loaded for ${prefecture} (${prediction.execution_mode || "backend"} mode).`);
        const map = await api.getMapOverview(endDate);
        applyMapOverview(map.items);
      } catch (error) {
        setStatus(`Unable to load backend data: ${error.message}`, true);
      } finally {
        checkButton.disabled = false;
      }
    },
    true,
  );

  try {
    const [metadata, dateRange] = await Promise.all([api.getPrefectures(), api.getDateRange()]);
    const prefNames = metadata.prefectures.map((item) => item.prefecture);
    ["pref-list", "home-pref-list"].forEach((id) => {
      const list = document.getElementById(id);
      if (!list) return;
      prefNames.forEach((name) => {
        if (!Array.from(list.options).some((option) => option.value === name)) {
          const option = document.createElement("option");
          option.value = name;
          list.appendChild(option);
        }
      });
    });
    ["from-date", "to-date"].forEach((id) => {
      const input = document.getElementById(id);
      if (!input) return;
      input.min = dateRange.min_date;
      input.max = dateRange.max_date;
      if (!input.value) input.value = dateRange.min_date;
    });
  } catch (error) {
    setStatus(`Backend metadata unavailable: ${error.message}`, true);
  }
}

export default function App() {
  const rootRef = useRef(null);

  useEffect(() => {
    if (!rootRef.current) return;
    rootRef.current.innerHTML = kikanMarkup;
    window.d3 = d3;
    new Function(kikanLegacy)();
    initializeApiIntegration().catch((error) => {
      setStatus(`Backend connection unavailable: ${error.message}`, true);
    });
  }, []);

  return <div ref={rootRef} />;
}
