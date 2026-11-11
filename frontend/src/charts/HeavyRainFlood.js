import * as d3 from "d3";
import { drawAxes, gridLines, tickDates } from "./chartHelpers.js";

export function renderHeavyRainFlood(ctx) {
  const { group, data, width, height, margin, colors } = ctx;
  const dates = data.map((d) => d.date);
  const x = d3.scalePoint().domain(dates).range([margin.left, width - margin.right]);
  const y = d3
    .scaleLinear()
    .domain([0, d3.max(data, (d) => d.value) || 1])
    .nice()
    .range([height - margin.bottom, margin.top]);

  gridLines(ctx, y);
  group
    .append("path")
    .datum(data)
    .attr("fill", colors.blue)
    .attr("opacity", 0.22)
    .attr("d", d3.area().x((d) => x(d.date)).y0(height - margin.bottom).y1((d) => y(d.value)).curve(d3.curveMonotoneX));
  group
    .append("path")
    .datum(data)
    .attr("fill", "none")
    .attr("stroke", colors.blue)
    .attr("stroke-width", 2.2)
    .attr("d", d3.line().x((d) => x(d.date)).y((d) => y(d.value)).curve(d3.curveMonotoneX));

  const HEAVY = 20;
  group
    .selectAll("circle.heavy")
    .data(data.filter((d) => d.value >= HEAVY))
    .join("circle")
    .attr("class", "heavy")
    .attr("cx", (d) => x(d.date))
    .attr("cy", (d) => y(d.value))
    .attr("r", 4)
    .attr("fill", colors.red)
    .attr("stroke", colors.surface)
    .append("title")
    .text((d) => `${d.date}: ${d.value.toFixed(1)} mm (heavy rain)`);

  drawAxes(ctx, x, y, { tickValues: tickDates(dates, ctx), xTitle: "Date", yTitle: "Daily rainfall (mm)" });
}