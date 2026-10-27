# Future Weather Attributes — Project Guide

## 1. Project objective

Forecast future daily meteorological attributes for Japanese towns using LSTM and GRU models. The historical weather input is assembled from Open-Meteo source datasets and prepared as a continuous daily, model-ready dataset.

## 2. Folder structure

```text
Group1_COS30049_Computing-Technology-Innovation/
├── Data/
│   └── Open-Meteo/
│       ├── Weather/
│       ├── Flood/
│       ├── Daily_solar_dewpoint/
│       ├── Daily_surface_pressure_wind_direction/
│       ├── Missing_weather_dataset/         # if available
│       ├── Daily_cloud_humid_pressure/      # optional fallback
│       └── Combined_daily_dataset/          # created by merge script
└── Future Weather Attributes/
    ├── dataset/LSTM_processed/
    │   └── japan_daily_lstm_processed.csv
    ├── Forecast/60lookback/
    ├── experiment_logs/60lookback/
    ├── trained_models/future_weather/60lookback/
    ├── merge_future_weather_folders.py
    ├── future_weather_attributes.py
    └── README.md
```

The source folders under `Data/Open-Meteo/` must contain **extracted CSV files**; the merge script does not read files inside ZIP archives. The source CSV folders are **not duplicated** inside this project.

## 3. How to use

Open PowerShell in `Future Weather Attributes/`.

### Step 1 — Install merging dependencies

```powershell
python -m pip install numpy pandas
```

### Step 2 — Merge and preprocess historical datasets

```powershell
python -B merge_future_weather_folders.py
```

By default, the script reads extracted CSVs from `../Data/Open-Meteo/`. It merges by prefecture, town, and date; checks duplicate location/date keys; creates a continuous daily calendar; and imputes missing feature values using a limited forward fill and **training-period** medians. Its default historical date range is **2021-01-01 to 2026-01-31**.

Outputs:

- `../Data/Open-Meteo/Combined_daily_dataset/japan_complete_daily_2021_2026.csv` — merged historical dataset before imputation (the filename is retained for compatibility; dates stop at 2026-01-31 by default).
- `dataset/LSTM_processed/japan_daily_lstm_processed.csv` — model-ready continuous data for the training script.
- `../Data/Open-Meteo/Combined_daily_dataset/imputation_summary.csv` — feature-wise imputation counts.
- `../Data/Open-Meteo/Combined_daily_dataset/merge_report.txt` — merge and validation messages.

To change the source location or the historical period:

```powershell
python -B merge_future_weather_folders.py --root "C:\path\to\Data\Open-Meteo" --start-date 2021-01-01 --end-date 2026-01-31
```

To override the output project directory (only if moving the scripts or outputs elsewhere), the merge script offers `--notebook-root` for backward compatibility.

### Step 3 — Train and compare LSTM / GRU in the terminal

Install the additional machine-learning packages:

```powershell
python -m pip install matplotlib scikit-learn tensorflow joblib
```

Then run the script **from `Future Weather Attributes/`**:

```powershell
python -B future_weather_attributes.py
```

By default, `MODEL_CHOICE = "BOTH"` compares LSTM and GRU and selects a run using validation data before testing. The script reads `dataset/LSTM_processed/japan_daily_lstm_processed.csv`, evaluates historical predictions and generates future forecasts. Edit `EXPERIMENT_ID`, `MODEL_CHOICE`, `SEEDS`, or `EXPERIMENT_SETTINGS` in the script to run another experiment. This training can be time-consuming.


## 4. Outputs

- `Forecast/<EXPERIMENT_ID>/future_daily_weather_attributes.csv` — predicted daily weather attributes (when forecasting is enabled).
- `experiment_logs/<EXPERIMENT_ID>/` — training history, forecast evaluation metrics, data quality reports and PNG charts.
- `trained_models/future_weather/<EXPERIMENT_ID>/` — saved models, scalers and run configurations.

The converted script defaults to `EXPERIMENT_ID = "60lookback"`; older `baseline_v1` outputs may also be present. Outputs depend on the selected experiment and run flags.

**Existing files have been preserved.** The merge script can overwrite its generated historical datasets and reports when rerun; the Python training script may overwrite its configured forecast and model outputs when executed.

## 5. Notes

- This folder contains the merge/processing script but **does not include** the raw Open-Meteo source directories. Those remain in the repository's `Data/Open-Meteo/` directory.
- Avoid interpreting forecasts as observed weather. The script evaluates historical tests; keep experimental results separate from future predictions.
- `__pycache__/` and `.pyc` files are unnecessary for submission. No Jupyter installation is required to run the Python script.


## Exploratory Data Analysis and Plots

Run the analysis from the `Future Weather Attributes` folder:

```powershell
python -m pip install numpy pandas matplotlib
python -B data_analysis_future_weather.py
```

The script reads `dataset/LSTM_processed/japan_daily_lstm_processed.csv` and automatically writes eight PNG images and `future_weather_iqr_summary.csv` to `plots/`. The figures cover boxplots (Tukey IQR outliers), distributions, missing values, correlations, monthly patterns, prefecture coverage, historical trends, and wind direction. The boxplots and histograms use a reproducible sample of up to 40,000 observations for plotting performance; the IQR CSV is calculated on all rows. IQR flags unusual observations, not necessarily invalid measurements.

The training script also saves **model training and forecast evaluation figures** (including loss plots and recursive comparisons) under the selected `experiment_logs/<EXPERIMENT_ID>/` directory.
