import * as d3 from "d3";

export function drawAxes(ctx, x, y, { tickValues, xTitle, yTitle, xAxis }) {
  const { group, height, width, margin, colors } = ctx;
  const bottom = xAxis || d3.axisBottom(x).tickValues(tickValues);
  group
    .append("g")
    .attr("class", "axis")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(bottom.tickSizeOuter(0));
  group
    .append("g")
    .attr("class", "axis")
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y).ticks(5).tickSizeOuter(0));
  group
    .append("text")
    .attr("x", margin.left + (width - margin.left - margin.right) / 2)
    .attr("y", height - 3)
    .attr("text-anchor", "middle")
    .attr("font-size", 10)
    .attr("fill", colors.text)
    .text(xTitle);
  group
    .append("text")
    .attr("transform", `translate(11,${margin.top + (height - margin.top - margin.bottom) / 2}) rotate(-90)`)
    .attr("text-anchor", "middle")
    .attr("font-size", 10)
    .attr("fill", colors.text)
    .text(yTitle);
}

export function gridLines(ctx, y) {
  const { group, width, margin, colors } = ctx;
  group
    .append("g")
    .attr("class", "grid")
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y).ticks(5).tickSize(-(width - margin.left - margin.right)).tickFormat(() => ""))
    .selectAll("line")
    .attr("stroke", colors.grid);
}

export function tickDates(dates, ctx) {
  const step = Math.max(1, Math.ceil(dates.length / Math.max(2, Math.floor(ctx.innerWidth / 64))));
  return dates.filter((_, i) => i % step === 0);
}