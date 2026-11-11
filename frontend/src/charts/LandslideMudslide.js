import * as d3 from "d3";
import { drawAxes, gridLines, tickDates } from "./chartHelpers.js";

export function renderLandslideMudslide(ctx) {
  const { group, data, width, height, margin, colors } = ctx;
  let running = 0;
  const steps = data.map((d) => {
    const start = running;
    running += d.value;
    return { date: d.date, delta: d.value, start, end: running };
  });
  const dates = steps.map((s) => s.date);
  const x = d3.scaleBand().domain(dates).range([margin.left, width - margin.right]).padding(0.2);
  const y = d3
    .scaleLinear()
    .domain([0, Math.max(1, running)])
    .nice()
    .range([height - margin.bottom, margin.top]);

  gridLines(ctx, y);
  group
    .selectAll("line.connector")
    .data(steps.slice(0, -1))
    .join("line")
    .attr("class", "connector")
    .attr("x1", (s) => x(s.date) + x.bandwidth())
    .attr("x2", (s, i) => x(steps[i + 1].date))
    .attr("y1", (s) => y(s.end))
    .attr("y2", (s) => y(s.end))
    .attr("stroke", colors.axis)
    .attr("stroke-dasharray", "2 2");
  group
    .selectAll("rect.step")
    .data(steps)
    .join("rect")
    .attr("class", "step")
    .attr("x", (s) => x(s.date))
    .attr("y", (s) => y(s.end))
    .attr("width", x.bandwidth())
    .attr("height", (s) => Math.max(1, y(s.start) - y(s.end)))
    .attr("rx", 2)
    .attr("fill", (s) => (s.delta >= 20 ? colors.red : s.delta > 0 ? colors.orange : colors.axis))
    .append("title")
    .text((s) => `${s.date}: +${s.delta.toFixed(1)} mm, cumulative ${s.end.toFixed(1)} mm`);

  drawAxes(ctx, x, y, {
    tickValues: tickDates(dates, ctx),
    xTitle: "Date",
    yTitle: "Cumulative rainfall (mm)",
  });
}