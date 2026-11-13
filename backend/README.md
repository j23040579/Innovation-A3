# Backend

The backend is a FastAPI service that loads the forecast weather CSV at startup and provides metadata, weather-query, and hazard-prediction endpoints. The interactive OpenAPI documentation is available at `http://localhost:8000/docs` while the service is running.

## Requirements

- Python 3.10 or later
- The forecast CSV at `Future Weather Attributes/Forecast/Final/future_daily_weather_attributes.csv`, relative to the repository root

To use a different CSV, set `WEATHER_DATASET_PATH` to an absolute path or a path relative to the repository root before starting the server.

## Setup and run on Windows

Run these commands from the repository root in PowerShell:

```powershell
py -m venv backend\.venv
backend\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
backend\.venv\Scripts\python.exe backend\run.py
```

The API listens on `http://localhost:8000` by default. To override the dataset path:

```powershell
$env:WEATHER_DATASET_PATH = "C:\path\to\future_daily_weather_attributes.csv"
backend\.venv\Scripts\python.exe backend\run.py
```

## API

All application routes are grouped under `/api`:

- `/api/metadata` provides dataset and location metadata.
- `/api/weather` provides forecast weather queries.
- `/api/predict` provides hazard-prediction endpoints.

See `http://localhost:8000/docs` for the current routes, parameters, and response schemas. The service also exposes `/` and `/api/health` for status checks.

## Tests

From the repository root, run the backend verification script with the backend dependencies installed:

```powershell
backend\.venv\Scripts\python.exe backend\test_backend.py
```

The backend test modules are `test_backend.py` and `test_typhoon_predictions.py`.

## Structure

```text
backend/
  app/
    api/          API route modules
    core/         Configuration and shared behavior
    processors/   Hazard-specific feature processors
    schemas/      Request and response models
    services/     Dataset queries, inference, and model registry
    main.py       FastAPI application and router registration
  requirements.txt
  run.py          Local Uvicorn entry point
  test_backend.py
  test_typhoon_predictions.py
```
