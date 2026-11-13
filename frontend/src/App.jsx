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
  applyTemperatureCardStatus,
  formatTemperature,
  riskStyle,
  temperatureStatusStyle,
} from "./temperatureStatus";
import {
  hazardCardPresentation,
  hazardMapColor,
  isSnowMapPrediction,
  mapHazardsForPrefecture,
  mapLegendTitle,
  nextMapHazardForPrefecture,
  normalizePrefecture,
  shouldShowHazardCard,
} from "./hazardPresentation";
import "./legacy/kikan.css";

function setStatus(message, isError = false) {
  const status = document.getElementById("forecast-status");
  if (!status) return;
  const isTransient = isError || message.startsWith("Loading");
  if (!isTransient) {
    status.textContent = "";
    status.hidden = true;
    delete status.dataset.state;
    return;
  }
  if (isError || message.startsWith("Loading")) {
    applyTemperatureCardStatus("Unknown");
  }
  status.textContent = message;
  status.dataset.state = isError ? "error" : "ready";
  status.hidden = false;
}

function renderRisks(risks = [], prefecture) {
  const grid = document.getElementById("hazard-grid");
  if (!grid) return;
  grid.replaceChildren();
  risks
    .filter((risk) => !["wind", "rain"].includes(String(risk.hazard || "").trim().toLowerCase()))
    .filter((risk) => shouldShowHazardCard(risk, prefecture))
    .forEach((risk) => {
      const presentation = hazardCardPresentation(risk);
      const style =
        risk.hazard === "temperature"
          ? temperatureStatusStyle(presentation.level)
          : riskStyle(presentation.level);
      const card = document.createElement("div");
      card.className = "card hazard";
      const top = document.createElement("div");
      top.className = "hazard-top";
      const name = document.createElement("span");
      name.className = "hazard-name";
      name.textContent = `${presentation.icon} ${presentation.name}`;
      const level = document.createElement("span");
      level.className = `hazard-level ${style.className}`;
      level.textContent =
        risk.hazard === "temperature" && risk.predicted_value != null
          ? formatTemperature(risk.predicted_value, presentation.level)
          : presentation.level;
      top.append(name, level);
      card.append(top);
      grid.appendChild(card);
    });
}

function renderTimeseries(series = []) {
  d3Charts.renderTimeseriesCharts(series);
}

function applyMapOverview(items = []) {
  window.updateKikanMapPredictions?.(items);
}

async function loadMapOverview(date, isCurrent = () => true) {
  const [map, snowCoverage] = await Promise.all([api.getMapOverview(date), api.getSnowCoverage()]);
  if (!isCurrent()) return;
  const coverage = new Set(snowCoverage.map(normalizePrefecture));
  const predictionsByPrefecture = await Promise.all(
    map.items.map(async ({ prefecture }) => {
      const hazards = mapHazardsForPrefecture(prefecture, coverage);
      try {
        const prediction = await api.predict({ prefecture, date, hazards });
        const risks = Object.fromEntries(
          (prediction.risks || []).map((risk) => [
            risk.hazard,
            { ...risk, execution_mode: prediction.execution_mode },
          ]),
        );
        return [normalizePrefecture(prefecture), risks];
      } catch (error) {
        if (error.status === 404) return [normalizePrefecture(prefecture), {}];
        throw error;
      }
    }),
  );
  const predictions = new Map(predictionsByPrefecture);
  if (!isCurrent()) return;
  const items = map.items.map((item) => ({
    ...item,
    hazard_predictions: predictions.get(normalizePrefecture(item.prefecture)) || {},
  }));
  applyMapOverview(items);
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

    renderRisks(prediction.risks, prefecture);
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
    const selectedPrefecture = prediction.prefecture || prefecture;
    await loadMapOverview(endDate, () => isCurrentSelection(revision));
    if (!isCurrentSelection(revision)) return;
    window.updateKikanRiskMapSelection?.({
      prefecture: selectedPrefecture,
      riskLevel: prediction.overall_risk_level,
    });
    setStatus("");
  }


  // Load real weather data for Data Visualization charts
  let datavizRevision = 0;

  window.onKikanDatavizRegion = async (prefecture) => {
  const revision = ++datavizRevision;

  try {
    const result = await api.getTimeseries({
      prefecture,
      startDate: "2026-02-01",
      endDate: "2027-01-31",
    });

    if (revision !== datavizRevision) return;

    d3Charts.renderTimeseriesCharts(result.series || []);
  } catch (error) {
    if (revision !== datavizRevision) return;
    console.error("Data Visualization charts failed:", error);
  }
};

window.onKikanDatavizRegion("Tokyo");

const selectedRegion = root.querySelector("#region-select");
if (selectedRegion?.value) window.onKikanDatavizRegion(selectedRegion.selectedOptions[0]?.textContent?.trim() || "Tokyo");

  window.onKikanMapPrefectureSelect = (prefecture) => {
    const revision = ++selectionRevision;
    const period = resolveForecastPeriod(appliedPeriod, getTomorrowISODate());
    applyTemperatureCardStatus("Unknown");
    setSelectionLoading(true);
    setStatus(`Loading live weather and risk data for ${prefecture}…`);
    loadSelectionData(prefecture, period, revision).catch((error) => {
      if (isCurrentSelection(revision)) {
        applyTemperatureCardStatus("Unknown");
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
      applyTemperatureCardStatus("Unknown");
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
          applyTemperatureCardStatus("Unknown");
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
    window.KikanMapHelpers = {
      hazardMapColor,
      isSnowMapPrediction,
      mapLegendTitle,
      nextMapHazardForPrefecture,
    };
    new Function(kikanLegacy)();
    initializeApiIntegration(rootRef.current).catch((error) => {
      setStatus(`Backend connection unavailable: ${error.message}`, true);
    });
  }, []);

  return <div ref={rootRef} />;
}