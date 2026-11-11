import * as d3 from "d3";
import { drawAxes, gridLines, tickDates } from "./chartHelpers.js";

export function renderTyphoonSeasonality(ctx) {
  const { group, data, allData, width, height, margin, colors } = ctx;
  const monthKeys = new Set(allData.map((d) => String(d.date).slice(0, 7)));
  const byMonth = monthKeys.size >= 2;
  const points = byMonth
    ? d3
        .rollups(
          data,
          (v) => d3.max(v, (d) => d.value),
          (d) => String(d.date).slice(0, 7),
        )
        .map(([label, value]) => ({ label, value }))
    : data.map((d) => ({ label: d.date, value: d.value }));

  const labels = points.map((p) => p.label);
  const x = d3.scalePoint().domain(labels).range([margin.left + 12, width - margin.right - 12]);
  const y = d3
    .scaleLinear()
    .domain([0, d3.max(points, (p) => p.value) || 1])
    .nice()
    .range([height - margin.bottom, margin.top]);

  gridLines(ctx, y);
  group
    .append("path")
    .datum(points)
    .attr("fill", "none")
    .attr("stroke", colors.purple)
    .attr("stroke-width", 2.5)
    .attr("d", d3.line().x((p) => x(p.label)).y((p) => y(p.value)).curve(d3.curveMonotoneX));

  const peak = d3.greatest(points, (p) => p.value);
  group
    .selectAll("circle.point")
    .data(points)
    .join("circle")
    .attr("class", "point")
    .attr("cx", (p) => x(p.label))
    .attr("cy", (p) => y(p.value))
    .attr("r", (p) => (p === peak ? 5 : 3.2))
    .attr("fill", (p) => (p === peak ? colors.red : colors.purple))
    .attr("stroke", colors.surface)
    .attr("stroke-width", 1.2)
    .append("title")
    .text((p) => `${p.label}: ${p.value.toFixed(1)} km/h${p === peak ? " (peak)" : ""}`);

  drawAxes(ctx, x, y, {
    tickValues: tickDates(labels, ctx),
    xTitle: byMonth ? "Month" : "Date",
    yTitle: "Max wind speed (km/h)",
  });
}