
import * as d3 from "d3";

import { drawAxes, gridLines, tickDates } from "./chartHelpers.js";

import { renderHeavyRainFlood } from "./HeavyRainFlood.js";
import { renderLandslideMudslide } from "./LandslideMudslide.js";
import { renderHeavySnowBlizzard } from "./HeavySnowBlizzard.js";
import { renderTyphoonSeasonality } from "./TyphoonSeasonality.js";

// ============================================================
// CHART STATE
// ============================================================

const monthlyWindows = new Map();
const timeseriesWindows = new Map();
const chartRenderers = new Map();

const MONTHLY_CHARTS = [
  {
    id: "chart-bar",
    key: "disruption",
    type: "bar",
    color: "teal",
    label: "Overall monthly disruption score",
  },
];

const TIMESERIES_CHARTS = [
  {
    id: "chart-typhoon",
    value: (p) => p.wind_speed_max,
    label: "Wind speed",
    draw: renderTyphoonSeasonality,
    limit: 365,
  },
  {
    id: "chart-flood",
    value: (p) => p.rain_sum,
    label: "Rainfall",
    draw: renderHeavyRainFlood,
    limit: 30,
  },
  {
    id: "chart-landslide",
    value: (p) => p.rain_sum,
    label: "Rainfall accumulation",
    draw: renderLandslideMudslide,
    limit: 14,
  },
  {
    id: "chart-snow",
    value: (p) => p.snowfall_sum,
    label: "Snowfall",
    draw: renderHeavySnowBlizzard,
    limit: 365,
    noZoom: true,
  },
];

// ============================================================
// HELPERS
// ============================================================

export function getChartDimensions(width, height) {
  return {
    width: Math.max(1, Number(width) || 520),
    height: Math.max(190, Number(height) || 220),
  };
}

export function getNextVisibleWindow(
  current,
  total,
  action,
  minimum = 3
) {
  if (!total) {
    return { start: 0, count: 0 };
  }

  const count = Math.max(
    1,
    Math.min(total, current?.count || total)
  );

  const start = Math.max(
    0,
    Math.min(total - count, current?.start || 0)
  );

  if (action === "reset") {
    return { start: 0, count: total };
  }

  const nextCount =
    action === "in"
      ? Math.max(Math.min(minimum, total), count - 2)
      : Math.min(total, count + 2);

  const center = start + count / 2;

  return {
    start: Math.max(
      0,
      Math.min(
        total - nextCount,
        Math.round(center - nextCount / 2)
      )
    ),
    count: nextCount,
  };
}

function readColors() {
  const styles = getComputedStyle(document.documentElement);

  const read = (name, fallback) =>
    styles.getPropertyValue(name).trim() || fallback;

  return {
    text: read("--chart-text", "#334155"),
    grid: read("--chart-grid", "#D8E0E8"),
    axis: read("--chart-axis", "#8793A3"),
    blue: read("--chart-blue", "#2563EB"),
    teal: read("--chart-teal", "#0F766E"),
    orange: read("--chart-orange", "#C2410C"),
    purple: read("--chart-purple", "#7C3AED"),
    red: read("--chart-red", "#B91C1C"),
    surface: read("--surface", "#FFFFFF"),
  };
}

function dimensionsFor(container) {
  return getChartDimensions(
    container.clientWidth,
    container.clientHeight
  );
}

function currentWindow(windows, id, total) {
  if (!total) {
    return { start: 0, count: 0 };
  }

  const saved = windows.get(id);

  const count = Math.max(
    1,
    Math.min(total, saved?.count || total)
  );

  return {
    start: Math.max(
      0,
      Math.min(total - count, saved?.start || 0)
    ),
    count,
  };
}

function updateZoomButtons(id, view, total) {
  document
    .querySelectorAll(`[data-chart-id="${id}"]`)
    .forEach((button) => {
      const action = button.dataset.chartAction;

      if (action === "in") {
        button.disabled =
          view.count <= Math.min(3, total);
      } else if (action === "out") {
        button.disabled = view.count >= total;
      } else {
        button.disabled = false;
      }
    });
}

function styleAxes(group, colors) {
  group
    .selectAll(".axis text")
    .attr("fill", colors.text);

  group
    .selectAll(".axis path, .axis line")
    .attr("stroke", colors.axis);

  group
    .selectAll(".grid path")
    .attr("display", "none");
}

function showChartMessage(container, message) {
  container.replaceChildren();

  const label = document.createElement("div");

  label.textContent = message;
  label.style.padding = "24px 12px";
  label.style.textAlign = "center";
  label.style.fontSize = "12px";
  label.style.color = readColors().text;

  container.appendChild(label);
}

// ============================================================
// MAIN BAR CHART
// Overall Disaster Overview
// ============================================================

function drawMonthlyChart(config) {
  const {
    id,
    data,
    months,
    color,
    label,
    regionName,
  } = config;

  const container = document.getElementById(id);

  if (!container) return;

  const values = Array.isArray(data) ? data : [];

  if (!months?.length || !values.length) {
    showChartMessage(container, "No monthly data available.");
    return;
  }

  container.dataset.zoomMode = "monthly";
  container.dataset.zoomTotal = String(months.length);

  container.replaceChildren();

  const { width, height } = dimensionsFor(container);
  const colors = readColors();

  const margin = {
    top: 14,
    right: 12,
    bottom: 36,
    left: 44,
  };

  const innerWidth = Math.max(
    1,
    width - margin.left - margin.right
  );

  const innerHeight = Math.max(
    1,
    height - margin.top - margin.bottom
  );

  const view = currentWindow(
    monthlyWindows,
    id,
    months.length
  );

  const visibleMonths = months.slice(
    view.start,
    view.start + view.count
  );

  const visibleData = visibleMonths.map(
    (month) => Number(values[month.index] ?? 0)
  );

  const x = d3
    .scaleBand()
    .domain(visibleMonths.map((month) => month.label))
    .range([0, innerWidth])
    .padding(0.2);

  const y = d3
    .scaleLinear()
    .domain([0, 100])
    .range([innerHeight, 0]);

  const svg = d3
    .select(container)
    .append("svg")
    .attr("viewBox", `0 0 ${width} ${height}`)
    .attr("preserveAspectRatio", "xMidYMid meet")
    .attr("role", "img")
    .attr(
      "aria-label",
      `${label}. Monthly illustrative scores from 0 to 100.`
    );

  svg
    .append("title")
    .text(`${label} — ${regionName}`);

  const group = svg
    .append("g")
    .attr(
      "transform",
      `translate(${margin.left},${margin.top})`
    );

  group
    .append("g")
    .attr("class", "grid")
    .call(
      d3
        .axisLeft(y)
        .ticks(5)
        .tickSize(-innerWidth)
        .tickFormat(() => "")
    );

  group
    .selectAll(".grid line")
    .attr("stroke", colors.grid);

  const tickStep = Math.max(
    1,
    Math.ceil(visibleMonths.length / 12)
  );

  group
    .append("g")
    .attr("class", "axis")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(
      d3
        .axisBottom(x)
        .tickValues(
          visibleMonths
            .filter((_, i) => i % tickStep === 0)
            .map((month) => month.label)
        )
        .tickSizeOuter(0)
    );

  group
    .append("g")
    .attr("class", "axis")
    .call(
      d3
        .axisLeft(y)
        .ticks(5)
        .tickSizeOuter(0)
        .tickPadding(7)
    );

  group
    .selectAll("rect.bar")
    .data(visibleData)
    .join("rect")
    .attr("class", "bar")
    .attr(
      "x",
      (_, index) => x(visibleMonths[index].label)
    )
    .attr("y", (value) => y(value))
    .attr("width", x.bandwidth())
    .attr(
      "height",
      (value) => innerHeight - y(value)
    )
    .attr("rx", 3)
    .attr(
      "fill",
      (value) =>
        value >= 45 ? colors.orange : color
    )
    .append("title")
    .text(
      (value, index) =>
        `${visibleMonths[index].label}: ${value}/100 (illustrative score)`
    );

  styleAxes(group, colors);

  updateZoomButtons(
    id,
    view,
    months.length
  );
}

// ============================================================
// RENDER MAIN MONTHLY CHART
// ============================================================

export function renderMonthlyCharts({
  monthly,
  months,
  regionName,
  showSnow,
}) {
  const snowCard = document
    .getElementById("chart-snow")
    ?.closest(".chart-card");

  // Keep snow chart visible as the fifth chart.
  if (snowCard) {
    snowCard.hidden = false;
  }

  if (!monthly || !months) return;

  const mainChart = MONTHLY_CHARTS[0];

  const render = () => {
    drawMonthlyChart({
      id: mainChart.id,
      data: monthly[mainChart.key],
      months,
      color: readColors()[mainChart.color],
      label: mainChart.label,
      regionName,
    });
  };

  chartRenderers.set(mainChart.id, render);

  render();
}

export function resetMonthlyChartZoom() {
  monthlyWindows.clear();
}

// ============================================================
// BACKEND TIMESERIES CHART DRAWING
// ============================================================

function drawTimeseriesChart({
  id,
  data,
  label,
  draw,
  noZoom,
}) {
  const container = document.getElementById(id);

  if (!container) return;

  container.dataset.zoomMode = "timeseries";
  container.dataset.zoomTotal = String(data.length);

  container.replaceChildren();

  if (!data.length) {
    showChartMessage(
      container,
      "No weather data available."
    );
    return;
  }

  const { width, height } = dimensionsFor(container);
  const colors = readColors();

  const margin = {
    top: 14,
    right: 12,
    bottom: 40,
    left: 48,
  };

  const innerWidth = Math.max(
    1,
    width - margin.left - margin.right
  );

  const innerHeight = Math.max(
    1,
    height - margin.top - margin.bottom
  );

  const view = currentWindow(
    timeseriesWindows,
    id,
    data.length
  );

  const visibleData = data.slice(
    view.start,
    view.start + view.count
  );

  const svg = d3
    .select(container)
    .append("svg")
    .attr("viewBox", `0 0 ${width} ${height}`)
    .attr("preserveAspectRatio", "xMidYMid meet")
    .attr("role", "img")
    .attr(
      "aria-label",
      `Backend weather ${label.toLowerCase()} chart.`
    );

  svg
    .append("title")
    .text(`Backend weather ${label.toLowerCase()} chart`);

  const group = svg.append("g");

  // The four independent chart files expect this format.
  const ctx = {
    group,
    data: visibleData,
    allData: data,
    width,
    height,
    margin,
    innerWidth,
    innerHeight,
    colors,
  };

  try {
    draw(ctx);
    styleAxes(group, colors);
  } catch (error) {
    console.error(`Failed to draw ${id}:`, error);

    showChartMessage(
      container,
      "Unable to display chart. Check Console."
    );
  }

  updateZoomButtons(
    id,
    view,
    data.length
  );

  // Snow scatter plot uses the full dataset.
  if (noZoom) {
    container.dataset.zoomMode = "none";
  }
}

// ============================================================
// RENDER FOUR WEATHER CHARTS
// ============================================================

export function renderTimeseriesCharts(series = []) {
  if (!Array.isArray(series) || !series.length) {
    console.warn(
      "No weather timeseries data received from backend."
    );
    return;
  }

  const sortedSeries = [...series]
    .filter((point) => point && point.date)
    .sort((a, b) =>
      String(a.date).localeCompare(String(b.date))
    );

  TIMESERIES_CHARTS.forEach(
    ({
      id,
      value,
      label,
      draw,
      limit,
      noZoom,
    }) => {
      const selectedSeries = sortedSeries.slice(-limit);

      const data = selectedSeries
        .map((point) => {
          const rawValue = value(point);

          return {
            date: point.date,
            value:
              rawValue == null || rawValue === ""
                ? NaN
                : Number(rawValue),
            raw: point,
          };
        })
        .filter((point) =>
          Number.isFinite(point.value)
        );

      const render = () => {
        drawTimeseriesChart({
          id,
          data,
          label,
          draw,
          noZoom,
        });
      };

      chartRenderers.set(id, render);

      render();
    }
  );
}

// ============================================================
// ZOOM BUTTONS
// ============================================================

function applyZoomAction(id, action) {
  const chart = document.getElementById(id);

  if (!chart) return;

  if (chart.dataset.zoomMode === "none") {
    return;
  }

  const renderer = chartRenderers.get(id);

  if (!renderer) return;

  const isTimeseries =
    chart.dataset.zoomMode === "timeseries";

  const windows = isTimeseries
    ? timeseriesWindows
    : monthlyWindows;

  const total = Number(chart.dataset.zoomTotal);

  if (!total) return;

  const current = currentWindow(
    windows,
    id,
    total
  );

  windows.set(
    id,
    getNextVisibleWindow(
      current,
      total,
      action
    )
  );

  renderer();
}

// ============================================================
// EVENT LISTENERS
// ============================================================

if (typeof document !== "undefined") {
  document.addEventListener("click", (event) => {
    const button = event.target.closest(
      "[data-chart-action][data-chart-id]"
    );

    if (!button) return;

    applyZoomAction(
      button.dataset.chartId,
      button.dataset.chartAction
    );
  });
}

if (typeof window !== "undefined") {
  window.addEventListener("resize", () => {
    chartRenderers.forEach((render) => {
      render();
    });
  });
}
