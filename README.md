# Japan Disaster & Weather Intelligence System

A React and D3 dashboard backed by a FastAPI service for exploring forecast weather data and multi-hazard predictions for Japan.

## Requirements

- Python 3.10 or later
- Node.js and npm
- The forecast CSV at `Future Weather Attributes/Forecast/Final/future_daily_weather_attributes.csv` (or configure a different file with `WEATHER_DATASET_PATH`)

## Run locally on Windows

Start the backend in PowerShell from the repository root:

```powershell
py -m venv backend\.venv
backend\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
backend\.venv\Scripts\python.exe backend\run.py
```

The API listens on port `8000`. Open `http://localhost:8000/docs` for the interactive API documentation.

In a second PowerShell window, start the frontend:

```powershell
cd frontend
npm install
npm run dev
```

Vite prints the local dashboard URL, normally `http://localhost:5173`.

If your forecast CSV is stored elsewhere, set its path before starting the backend. Relative paths are resolved from the repository root:

```powershell
$env:WEATHER_DATASET_PATH = "C:\path\to\future_daily_weather_attributes.csv"
backend\.venv\Scripts\python.exe backend\run.py
```

See [backend/README.md](backend/README.md) for backend setup, structure, API, and test details.
