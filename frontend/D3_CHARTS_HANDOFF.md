# D3.js charts handoff

This note covers the frontend's existing weather time-series charts and the API they use. The timeseries endpoint supplies weather measurements; this is not a claim that every chart or hazard is backed by a trained model.

## Run locally on Windows

Open a PowerShell or Command Prompt at the repository root, then start the frontend:

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL printed in the terminal (usually `http://localhost:5173`). Keep this terminal open while using the frontend.

In a **second** terminal, from the repository root, set up and start the backend:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

If the backend dependencies and virtual environment are already prepared, activate `.venv` and run `python run.py` only. Keep the backend terminal open too. The API is at `http://localhost:8000`; interactive Swagger documentation is at `http://localhost:8000/docs`.

## API configuration and timeseries request

`frontend/src/api.js` defaults the API base URL to `http://localhost:8000`. To use another backend, set `VITE_API_BASE_URL` in the frontend environment (for example, in `frontend/.env.local`) and restart Vite:

```text
VITE_API_BASE_URL=http://localhost:8000
```

The frontend requests a prefecture's daily series using:

```text
GET http://localhost:8000/api/weather/timeseries?prefecture=Tokyo&start_date=2026-06-01&end_date=2026-06-10
```

The supported forecast date range is **2026-02-01 through 2027-12-31**. The API response includes `prefecture`, optional `town`, `start_date`, `end_date`, `total_data_points`, and a `series` array. Each series point has a `date` and may include `temperature_max`, `temperature_min`, `temperature_mean`, `rain_sum`, `precipitation_sum`, `snowfall_sum`, `wind_speed_max`, `wind_gusts_max`, `relative_humidity_mean`, `surface_pressure_mean`, `cloud_cover_mean`, and `river_discharge`.

The charts currently read these point fields:

| Chart | Series field |
|---|---|
| Temperature | `temperature_mean` |
| Wind speed | `wind_speed_max` |
| Rainfall charts | `rain_sum` |
| Snowfall | `snowfall_sum` |

Other fields may be present in the API response but are not currently mapped to these charts. Check `/docs` and the backend schema if the response contract changes.

## Existing data flow and chart behavior

`frontend/src/App.jsx` calls `api.getTimeseries(...)`, takes `response.series`, and passes it to `renderTimeseriesCharts`. The API helper and base URL configuration live in `frontend/src/api.js`; D3 drawing and the metric-to-chart mapping live in `frontend/src/charts/d3Charts.js`.

The D3 renderer draws the time-series charts, keeps independent zoom windows, supports the chart zoom controls and D3 zoom gestures, redraws charts on window resize, and reads chart colors from the active theme's CSS variables when rendering. Keep network fetching and response handling in the API/App layers; put chart drawing and presentation changes in the D3 renderer.

## Working notes

- Before adding or changing a chart metric, confirm that the selected API response's `series` points contain that field and that it is numeric or nullable.
- If no time-series data exists for the selected prefecture and date interval, the backend returns **404** with a detail message. Check the selected range, prefecture/town, and backend response rather than treating an empty chart as a successful data result.
- Frontend checks, run from `frontend`, are `npm test` and `npm run build`.
- Coordinate API response or metric changes with the backend owner before relying on them in a chart. Do not infer broader model integration from these weather-series charts.
