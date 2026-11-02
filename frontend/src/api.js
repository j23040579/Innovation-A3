const configuredBaseUrl = (import.meta.env.VITE_API_BASE_URL || "http://localhost:8000").trim();
const API_BASE_URL = configuredBaseUrl.replace(/\/api\/?$/, "").replace(/\/$/, "");

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { Accept: "application/json", ...(options.headers || {}) },
    ...options,
  });
  if (!response.ok) {
    let detail = `Request failed (${response.status})`;
    try {
      const body = await response.json();
      detail = body.detail || detail;
    } catch {
      // Keep the HTTP status when the server does not return JSON.
    }
    throw new Error(detail);
  }
  return response.json();
}

export const api = {
  getPrefectures: () => request("/api/metadata/prefectures"),
  getDateRange: () => request("/api/metadata/date-range"),
  getDaily: ({ prefecture, date, town }) =>
    request(`/api/weather/daily?${new URLSearchParams({ prefecture, date, ...(town ? { town } : {}) })}`),
  getTimeseries: ({ prefecture, startDate, endDate, town }) =>
    request(
      `/api/weather/timeseries?${new URLSearchParams({
        prefecture,
        start_date: startDate,
        end_date: endDate,
        ...(town ? { town } : {}),
      })}`,
    ),
  getMapOverview: (date) => request(`/api/weather/map-overview?date=${encodeURIComponent(date)}`),
  predict: (body) =>
    request("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }),
};
