import * as d3 from "d3";

const monthlyWindows = new Map();
const timeseriesWindows = new Map();
const chartRenderers = new Map();
const MONTHLY_CHARTS = [
  { id: "chart-bar", key: "disruption", type: "bar", color: "teal", label: "Overall monthly disruption score" },
  { id: "chart-typhoon", key: "typhoon", type: "line", color: "red", label: "Typhoon seasonality" },
  { id: "chart-flood", key: "flood", type: "line", color: "teal", label: "Heavy rain and flood risk" },
  { id: "chart-landslide", key: "landslide", type: "line", color: "purple", label: "Landslide and mudslide risk" },
  { id: "chart-snow", key: "snow", type: "line", color: "blue", label: "Heavy snow risk" },
];
const TIMESERIES_CHARTS = [
  { id: "chart-bar", value: (point) => point.temperature_mean, label: "Temperature" },
  { id: "chart-typhoon", value: (point) => point.wind_speed_max, label: "Wind speed" },
  { id: "chart-flood", value: (point) => point.rain_sum, label: "Rainfall" },
  { id: "chart-landslide", value: (point) => point.rain_sum, label: "Rainfall" },
  { id: "chart-snow", value: (point) => point.snowfall_sum, label: "Snowfall" },
];

export function getChartDimensions(width, height) {
  return {
    width: Math.max(1, Number(width) || 520),
    height: Math.max(190, Number(height) || 220),
  };
}

export function getNextVisibleWindow(current, total, action, minimum = 3) {
  if (!total) return { start: 0, count: 0 };
  const count = Math.max(1, Math.min(total, current?.count || total));
  const start = Math.max(0, Math.min(total - count, current?.start || 0));
  if (action === "reset") return { start: 0, count: total };
  const nextCount =
    action === "in"
      ? Math.max(Math.min(minimum, total), count - 2)
      : Math.min(total, count + 2);
  const center = start + count / 2;
  return {
    start: Math.max(0, Math.min(total - nextCount, Math.round(center - nextCount / 2))),
    count: nextCount,
  };
}

function readColors() {
  const styles = getComputedStyle(document.documentElement);
  const read = (name, fallback) => styles.getPropertyValue(name).trim() || fallback;
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
  return getChartDimensions(container.clientWidth, container.clientHeight);
}

function getTickStep(count, plotWidth, minSpacing = 44) {
  return Math.max(1, Math.ceil(count / Math.max(2, Math.floor(plotWidth / minSpacing))));
}

function currentWindow(windows, id, total) {
  const saved = windows.get(id);
  const count = Math.max(1, Math.min(total, saved?.count || total));
  return {
    start: Math.max(0, Math.min(total - count, saved?.start || 0)),
    count,
  };
}

function updateZoomButtons(id, window, total) {
  document.querySelectorAll(`[data-chart-id="${id}"]`).forEach((button) => {
    button.disabled =
      button.dataset.chartAction === "in"
        ? window.count <= Math.min(3, total)
        : button.dataset.chartAction === "out"
          ? window.count >= total
          : false;
  });
}

function zoomToWindow(id, windows, total, transform) {
  const current = currentWindow(windows, id, total);
  const count = Math.max(1, Math.min(total, Math.round(current.count / transform.k)));
  const shift = Math.round((-transform.x / Math.max(1, transform.width)) * current.count);
  const center = current.start + current.count / 2 + shift;
  windows.set(id, {
    start: Math.max(0, Math.min(total - count, Math.round(center - count / 2))),
    count,
  });
}

function attachD3Zoom(svg, id, windows, total, innerWidth, render) {
  const zoom = d3
    .zoom()
    .scaleExtent([1, 6])
    .on("end", (event) => {
      if (!event.sourceEvent) return;
      zoomToWindow(id, windows, total, {
        k: event.transform.k,
        x: event.transform.x,
        width: innerWidth,
      });
      render();
    });
  svg.call(zoom);
}

function styleAxes(group, colors) {
  group.selectAll(".axis text").attr("fill", colors.text);
  group.selectAll(".axis path,.axis line").attr("stroke", colors.axis);
  group.selectAll(".grid path").attr("display", "none");
}

function drawMonthlyChart(config) {
  const { id, data, months, type, color, label, regionName } = config;
  const container = document.getElementById(id);
  if (!container) return;
  container.dataset.zoomMode = "monthly";
  container.dataset.zoomTotal = String(months.length);
  container.replaceChildren();
  if (!months.length) return;

  const { width, height } = dimensionsFor(container);
  const colors = readColors();
  const margin = { top: 14, right: 12, bottom: 36, left: 44 };
  const innerWidth = Math.max(1, width - margin.left - margin.right);
  const innerHeight = Math.max(1, height - margin.top - margin.bottom);
  const view = currentWindow(monthlyWindows, id, months.length);
  const visibleMonths = months.slice(view.start, view.start + view.count);
  const visibleData = visibleMonths.map((month) => data[month.index]);
  const x = d3
    .scaleBand()
    .domain(visibleMonths.map((month) => month.label))
    .range([0, innerWidth])
    .padding(type === "bar" ? 0.2 : 0.05);
  const y = d3.scaleLinear().domain([0, 100]).range([innerHeight, 0]);
  const tickStep = getTickStep(visibleMonths.length, innerWidth);
  const svg = d3
    .select(container)
    .append("svg")
    .attr("viewBox", `0 0 ${width} ${height}`)
    .attr("preserveAspectRatio", "xMidYMid meet")
    .attr("role", "img")
    .attr("aria-label", `${label}. Monthly illustrative scores from 0 to 100.`);
  svg.append("title").text(`${label} — ${regionName}`);
  const group = svg.append("g").attr("transform", `translate(${margin.left},${margin.top})`);
  group
    .append("g")
    .attr("class", "grid")
    .call(d3.axisLeft(y).ticks(5).tickSize(-innerWidth).tickFormat(() => ""));
  group.selectAll(".grid line").attr("stroke", colors.grid);
  group
    .append("g")
    .attr("class", "axis")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(
      d3
        .axisBottom(x)
        .tickValues(visibleMonths.filter((_, index) => index % tickStep === 0).map((month) => month.label))
        .tickSizeOuter(0),
    );
  group.append("g").attr("class", "axis").call(d3.axisLeft(y).ticks(5).tickSizeOuter(0).tickPadding(7));

  if (type === "bar") {
    group
      .selectAll("rect.bar")
      .data(visibleData)
      .join("rect")
      .attr("class", "bar")
      .attr("x", (_, index) => x(visibleMonths[index].label))
      .attr("y", (value) => y(value))
      .attr("width", x.bandwidth())
      .attr("height", (value) => innerHeight - y(value))
      .attr("rx", 3)
      .attr("fill", (value) => (value >= 45 ? colors.orange : color))
      .append("title")
      .text((value, index) => `${visibleMonths[index].label}: ${value}/100 (illustrative score)`);
  } else {
    const line = d3
      .line()
      .x((_, index) => x(visibleMonths[index].label) + x.bandwidth() / 2)
      .y((value) => y(value))
      .curve(d3.curveMonotoneX);
    const area = d3
      .area()
      .x((_, index) => x(visibleMonths[index].label) + x.bandwidth() / 2)
      .y0(innerHeight)
      .y1((value) => y(value))
      .curve(d3.curveMonotoneX);
    group.append("path").datum(visibleData).attr("d", area).attr("fill", color).attr("opacity", 0.12);
    group.append("path").datum(visibleData).attr("d", line).attr("fill", "none").attr("stroke", color).attr("stroke-width", 2.5);
    group
      .selectAll("circle.point")
      .data(visibleData)
      .join("circle")
      .attr("class", "point")
      .attr("cx", (_, index) => x(visibleMonths[index].label) + x.bandwidth() / 2)
      .attr("cy", (value) => y(value))
      .attr("r", 3.3)
      .attr("fill", color)
      .attr("stroke", colors.surface)
      .attr("stroke-width", 1.2)
      .append("title")
      .text((value, index) => `${visibleMonths[index].label}: ${value}/100 (illustrative score)`);
  }

  styleAxes(group, colors);
  updateZoomButtons(id, view, months.length);
  attachD3Zoom(svg, id, monthlyWindows, months.length, innerWidth, config.render);
}

export function renderMonthlyCharts({ monthly, months, regionName, showSnow }) {
  const snowCard = document.getElementById("chart-snow")?.closest(".chart-card");
  if (snowCard) snowCard.hidden = !showSnow;
  if (!monthly) return;
  const renderers = [];
  MONTHLY_CHARTS.forEach(({ id, key, type, color, label }) => {
    const render = () =>
      drawMonthlyChart({
        id,
        data: monthly[key],
        months,
        type,
        color: readColors()[color],
        label,
        regionName,
        render,
      });
    chartRenderers.set(id, render);
    renderers.push(render);
  });
  renderers.forEach((render) => render());
}

export function resetMonthlyChartZoom() {
  monthlyWindows.clear();
}

function drawTimeseriesChart({ id, data, label, render }) {
  const container = document.getElementById(id);
  if (!container) return;
  container.dataset.zoomMode = "timeseries";
  container.dataset.zoomTotal = String(data.length);
  container.replaceChildren();
  if (!data.length) return;

  const { width, height } = dimensionsFor(container);
  const colors = readColors();
  const margin = { top: 14, right: 12, bottom: 40, left: 44 };
  const innerWidth = Math.max(1, width - margin.left - margin.right);
  const innerHeight = Math.max(1, height - margin.top - margin.bottom);
  const view = currentWindow(timeseriesWindows, id, data.length);
  const visibleData = data.slice(view.start, view.start + view.count);
  const dates = visibleData.map((point) => point.date);
  const x = d3.scalePoint().domain(dates).range([margin.left, width - margin.right]);
  const y = d3
    .scaleLinear()
    .domain([0, d3.max(data, (point) => point.value) || 1])
    .nice()
    .range([height - margin.bottom, margin.top]);
  const tickStep = getTickStep(dates.length, innerWidth, 64);
  const svg = d3
    .select(container)
    .append("svg")
    .attr("viewBox", `0 0 ${width} ${height}`)
    .attr("preserveAspectRatio", "xMidYMid meet")
    .attr("role", "img")
    .attr("aria-label", `Live backend weather ${label.toLowerCase()} time series.`);
  svg.append("title").text(`Live backend ${label.toLowerCase()} time series`);
  const group = svg.append("g");
  group
    .append("path")
    .datum(visibleData)
    .attr("fill", "none")
    .attr("stroke", colors.blue)
    .attr("stroke-width", 2.5)
    .attr(
      "d",
      d3
        .line()
        .x((point) => x(point.date))
        .y((point) => y(point.value)),
    );
  group
    .append("g")
    .attr("class", "axis")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x).tickValues(dates.filter((_, index) => index % tickStep === 0)));
  group.append("g").attr("class", "axis").attr("transform", `translate(${margin.left},0)`).call(d3.axisLeft(y).ticks(5));
  styleAxes(group, colors);
  updateZoomButtons(id, view, data.length);
  attachD3Zoom(svg, id, timeseriesWindows, data.length, innerWidth, render);
}

export function renderTimeseriesCharts(series = []) {
  TIMESERIES_CHARTS.forEach(({ id, value, label }) => {
    const data = series.map((point) => ({
      date: point.date,
      value: Number(value(point) || 0),
    }));
    const render = () => drawTimeseriesChart({ id, data, label, render });
    chartRenderers.set(id, render);
    render();
  });
}

function applyZoomAction(id, action) {
  const chart = document.getElementById(id);
  if (!chart) return;
  const renderer = chartRenderers.get(id);
  if (!renderer) return;
  const windows = chart.dataset.zoomMode === "timeseries" ? timeseriesWindows : monthlyWindows;
  const total = Number(chart.dataset.zoomTotal);
  if (!total) return;
  windows.set(id, getNextVisibleWindow(currentWindow(windows, id, total), total, action));
  renderer();
}

if (typeof document !== "undefined") {
  document.addEventListener("click", (event) => {
    const button = event.target.closest("[data-chart-action][data-chart-id]");
    if (button) applyZoomAction(button.dataset.chartId, button.dataset.chartAction);
  });
}

if (typeof window !== "undefined") {
  window.addEventListener("resize", () => {
    chartRenderers.forEach((render) => render());
  });
}
