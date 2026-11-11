
import * as d3 from "d3";
import { drawAxes, gridLines } from "./chartHelpers.js";

export function renderHeavySnowBlizzard(ctx) {
  const { group, allData, width, height, margin, colors } = ctx;

  const points = allData
    .map((d) => ({
      date: d.date,
      temp: Number(d.raw?.temperature_mean),
      snow: Number(d.value),
    }))
    .filter(
      (p) =>
        Number.isFinite(p.temp) &&
        Number.isFinite(p.snow) &&
        p.snow >= 0
    );

  if (!points.length) return;

  const tempExtent = d3.extent(points, (p) => p.temp);
  const minTemp = tempExtent[0];
  const maxTemp = tempExtent[1];

  const xDomain =
    minTemp === maxTemp
      ? [minTemp - 1, maxTemp + 1]
      : [minTemp, maxTemp];

  const x = d3
    .scaleLinear()
    .domain(xDomain)
    .nice()
    .range([margin.left + 6, width - margin.right - 6]);

  const maxSnow = d3.max(points, (p) => p.snow) || 1;

  const y = d3
    .scaleLinear()
    .domain([0, maxSnow])
    .nice()
    .range([height - margin.bottom, margin.top]);

  gridLines(ctx, y);

  if (points.length >= 3) {
    const meanTemp = d3.mean(points, (p) => p.temp);
    const meanSnow = d3.mean(points, (p) => p.snow);

    const denominator = d3.sum(
      points,
      (p) => (p.temp - meanTemp) ** 2
    );

    if (denominator > 0) {
      const numerator = d3.sum(
        points,
        (p) => (p.temp - meanTemp) * (p.snow - meanSnow)
      );

      const slope = numerator / denominator;
      const intercept = meanSnow - slope * meanTemp;

      const [x0, x1] = x.domain();
      const [yMin, yMax] = y.domain();

      const clampY = (value) =>
        Math.max(yMin, Math.min(yMax, value));

      group
        .append("line")
        .attr("class", "snow-trendline")
        .attr("x1", x(x0))
        .attr("x2", x(x1))
        .attr("y1", y(clampY(slope * x0 + intercept)))
        .attr("y2", y(clampY(slope * x1 + intercept)))
        .attr("stroke", colors.red)
        .attr("stroke-width", 1.7)
        .attr("stroke-dasharray", "5 4")
        .attr("opacity", 0.85);
    }
  }

  const circles = group
    .selectAll("circle.snow")
    .data(points)
    .join("circle")
    .attr("class", "snow")
    .attr("cx", (p) => x(p.temp))
    .attr("cy", (p) => y(p.snow))
    .attr("r", 2.5)
    .attr("fill", colors.teal)
    .attr("opacity", 0.38)
    .attr("stroke", "none");

  circles
    .on("mouseover", function () {
      d3.select(this)
        .raise()
        .attr("r", 5)
        .attr("opacity", 1)
        .attr("stroke", colors.text)
        .attr("stroke-width", 1);
    })
    .on("mouseout", function () {
      d3.select(this)
        .attr("r", 2.5)
        .attr("opacity", 0.38)
        .attr("stroke", "none");
    });

  circles
    .append("title")
    .text(
      (p) =>
        `Date: ${p.date}\n` +
        `Temperature: ${p.temp.toFixed(1)} °C\n` +
        `Snowfall: ${p.snow.toFixed(2)} cm`
    );

  drawAxes(ctx, x, y, {
    xAxis: d3.axisBottom(x).ticks(6),
    xTitle: "Mean temperature (°C)",
    yTitle: "Snowfall (cm)",
  });
}
