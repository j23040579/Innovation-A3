import { useEffect, useRef } from "react";
import * as d3 from "d3";
import * as d3Charts from "./charts/d3Charts";
import { kikanMarkup } from "./legacy/kikanMarkup";
import { kikanLegacy } from "./legacy/kikanLegacy";
import { api } from "./api";
import { getTomorrowISODate, resolveForecastPeriod } from "./forecastPeriod";
import {
  FORECAST_LOADING_SELECTOR,
  MAP_LOADING_SELECTOR,
  setForecastLoading,
} from "./forecastLoading";
import {
  applyForecastTemperature,
  applyTemperatureBackground,
  formatTemperature,
  riskStyle,
  temperatureStatusStyle,
} from "./temperatureStatus";
import "./legacy/kikan.css";

const normalizePrefecture = (value) => String(value || "").toLowerCase().replace(/[^a-z0-9]/g, "");

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
  risks
    .filter((risk) => !["wind", "rain"].includes(String(risk.hazard || "").trim().toLowerCase()))
    .forEach((risk) => {
      const style =
        risk.hazard === "temperature"
          ? temperatureStatusStyle(risk.risk_level)
          : riskStyle(risk.risk_level);
      const profileProbabilities = risk.profile_match_probabilities;
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
      const message = document.createElement("small");
      message.textContent = risk.alert_message || "Live backend prediction";
      if (profileProbabilities) {
        const profileLabel = document.createElement("small");
        profileLabel.textContent = "Landfall profile match (not typhoon occurrence probability)";
        card.append(top, profileLabel, message);
      } else {
        card.append(top, message);
      }
      grid.appendChild(card);
    });
}

function renderTimeseries(series = []) {
  d3Charts.renderTimeseriesCharts(series);
}

function applyMapOverview(items = []) {
  window.updateKikanSnowMapData?.(items);
  if (document.getElementById("map-hazard-select")?.value === "snow") return;
  const byPrefecture = new Map(items.map((item) => [normalizePrefecture(item.prefecture), item]));
  document.querySelectorAll(".pref").forEach((path) => {
    const item =
      byPrefecture.get(normalizePrefecture(path.getAttribute("aria-label"))) ||
      byPrefecture.get(normalizePrefecture(path.dataset.id));
    if (!item) return;
    const style = riskStyle(item.primary_risk_level);
    path.style.fill = style.color;
    path.style.opacity = "0.85";
    path.style.stroke = "#FFFFFF";
  });
}

async function loadMapOverview(date, isCurrent = () => true) {
  const [map, snowCoverage] = await Promise.all([api.getMapOverview(date), api.getSnowCoverage()]);
  if (!isCurrent()) return;
  const coverage = new Set(snowCoverage.map(normalizePrefecture));
  const supportedSnowPrefectures = map.items
    .map((item) => item.prefecture)
    .filter((prefecture) => coverage.has(normalizePrefecture(prefecture)));
  const [snowPredictions, rainPredictions] = await Promise.all([
    Promise.all(
      supportedSnowPrefectures.map(async (prefecture) => {
        try {
          const prediction = await api.predict({ prefecture, date, hazards: ["snow"] });
          const snowRisk = prediction.risks?.find((risk) => risk.hazard === "snow");
          return [
            normalizePrefecture(prefecture),
            {
              execution_mode: prediction.execution_mode,
              risk_level: snowRisk?.risk_level,
            },
          ];
        } catch (error) {
          if (error.status === 404) return [normalizePrefecture(prefecture), null];
          throw error;
        }
      }),
    ),
    Promise.all(
      map.items.map(async ({ prefecture }) => {
        try {
          const prediction = await api.predict({ prefecture, date, hazards: ["rain"] });
          const rainRisk = prediction.risks?.find((risk) => risk.hazard === "rain");
          return [
            normalizePrefecture(prefecture),
            {
              execution_mode: prediction.execution_mode,
              risk_level: rainRisk?.risk_level,
              predicted_value: rainRisk?.predicted_value,
              unit: rainRisk?.unit,
            },
          ];
        } catch (error) {
          if (error.status === 404) return [normalizePrefecture(prefecture), null];
          throw error;
        }
      }),
    ),
  ]);
  const snowByPrefecture = new Map(snowPredictions);
  const rainByPrefecture = new Map(rainPredictions);
  if (!isCurrent()) return;
  const items = map.items.map((item) => ({
    ...item,
    snow_prediction: snowByPrefecture.get(normalizePrefecture(item.prefecture)) || null,
    rain_prediction: rainByPrefecture.get(normalizePrefecture(item.prefecture)) || null,
  }));
  applyMapOverview(items);
  window.updateKikanMapOverviewData?.(items);
  window.updateKikanRainMapData?.(items);
}

async function initializeApiIntegration(root) {
  const checkButton = document.getElementById("check-risk-btn");
  let appliedPeriod = null;
  let selectionRevision = 0;
  const initializationRevision = selectionRevision;
  const isCurrentSelection = (revision) => revision === selectionRevision;
  const setSelectionLoading = (isLoading) =>
    setForecastLoading(root.querySelectorAll(FORECAST_LOADING_SELECTOR), isLoading);
  const setMapLoading = (isLoading) =>
    setForecastLoading(root.querySelectorAll(MAP_LOADING_SELECTOR), isLoading);

  async function loadSelectionData(prefecture, period, revision) {
    const { startDate, endDate } = period;
    const [prediction, daily, timeseries] = await Promise.all([
      api.predict({ prefecture, date: endDate }),
      api.getDaily({ prefecture, date: endDate }),
      api.getTimeseries({ prefecture, startDate, endDate }),
    ]);
    if (!isCurrentSelection(revision)) return;

    renderRisks(prediction.risks);
    renderTimeseries(timeseries.series);
    const { temperature, temperatureStatus } = applyForecastTemperature(prediction, daily);
    const tempEl = document.getElementById("stat-temp");
    if (temperature !== undefined && tempEl) {
      tempEl.textContent = formatTemperature(temperature, temperatureStatus);
    }
    const locationSummary = document.getElementById("mon-loc");
    if (locationSummary) {
      locationSummary.replaceChildren("Monitoring live weather for ", Object.assign(document.createElement("strong"), { textContent: prefecture }));
    }
    document.getElementById("map-summary-name").textContent = prefecture;
    document.getElementById("map-summary-hazard").textContent = prediction.overall_risk_level || "Unknown";
    setStatus(
      `Live backend data loaded for ${prefecture} (${prediction.execution_mode || "backend"} mode).`,
    );
    const selectedPrefecture = prediction.prefecture || prefecture;
    await loadMapOverview(endDate, () => isCurrentSelection(revision));
    if (!isCurrentSelection(revision)) return;
    window.updateKikanRiskMapSelection?.({
      prefecture: selectedPrefecture,
      riskLevel: prediction.overall_risk_level,
    });
  }

  window.onKikanMapPrefectureSelect = (prefecture) => {
    const revision = ++selectionRevision;
    const period = resolveForecastPeriod(appliedPeriod, getTomorrowISODate());
    applyTemperatureBackground("Unknown");
    setSelectionLoading(true);
    setStatus(`Loading live weather and risk data for ${prefecture}…`);
    loadSelectionData(prefecture, period, revision).catch((error) => {
      if (isCurrentSelection(revision)) {
        applyTemperatureBackground("Unknown");
        setStatus(`Unable to load backend data: ${error.message}`, true);
      }
    }).finally(() => {
      if (isCurrentSelection(revision)) setSelectionLoading(false);
    });
  };

  checkButton?.addEventListener(
    "click",
    async (event) => {
      event.preventDefault();
      event.stopImmediatePropagation();
      const prefecture = document.getElementById("loc-input")?.value.trim();
      if (!prefecture) {
        setStatus("Choose a prefecture and a valid date range.", true);
        return;
      }
      const validatedPeriod = window.readKikanValidatedPeriod?.();
      if (!validatedPeriod) return;
      const period = { from: validatedPeriod.from, to: validatedPeriod.to };
      appliedPeriod = period;
      const revision = ++selectionRevision;
      checkButton.disabled = true;
      applyTemperatureBackground("Unknown");
      setSelectionLoading(true);
      window.applyKikanRiskContext?.(prefecture, validatedPeriod);
      window.updateKikanRiskMapSelection?.({ prefecture });
      setStatus(`Loading live weather and risk data for ${prefecture}…`);
      try {
        await loadSelectionData(
          prefecture,
          { startDate: period.from, endDate: period.to },
          revision,
        );
      } catch (error) {
        if (isCurrentSelection(revision)) {
          applyTemperatureBackground("Unknown");
          setStatus(`Unable to load backend data: ${error.message}`, true);
        }
      } finally {
        checkButton.disabled = false;
        if (isCurrentSelection(revision)) setSelectionLoading(false);
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
    setMapLoading(true);
    try {
      await loadMapOverview(
        document.getElementById("to-date")?.value || dateRange.min_date,
        () => isCurrentSelection(initializationRevision),
      );
    } finally {
      if (isCurrentSelection(initializationRevision)) setMapLoading(false);
    }
  } catch (error) {
    if (isCurrentSelection(initializationRevision)) {
      setStatus(`Backend metadata or map data unavailable: ${error.message}`, true);
    }
  }
}

export default function App() {
  const rootRef = useRef(null);

  useEffect(() => {
    if (!rootRef.current) return;
    rootRef.current.innerHTML = kikanMarkup;
    window.d3 = d3;
    window.KikanCharts = d3Charts;
    new Function(kikanLegacy)();
    initializeApiIntegration(rootRef.current).catch((error) => {
      setStatus(`Backend connection unavailable: ${error.message}`, true);
    });
  }, []);

  return <div ref={rootRef} />;
}
