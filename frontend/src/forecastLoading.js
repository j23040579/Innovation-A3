export const FORECAST_LOADING_SELECTOR = [
  "#hazard-grid",
  "#stat-temp",
  "#mon-loc",
  "#map-risk-summary",
  "#chart-bar",
  "#chart-typhoon",
  "#chart-flood",
  "#chart-snow",
  ".map-shell",
].join(", ");

export const MAP_LOADING_SELECTOR = ".map-shell";

export function setForecastLoading(elements, isLoading) {
  elements.forEach((element) => {
    if (isLoading) {
      element.setAttribute("aria-busy", "true");
      element.setAttribute("data-forecast-loading", "true");
    } else {
      element.removeAttribute("aria-busy");
      element.removeAttribute("data-forecast-loading");
    }
  });
}
