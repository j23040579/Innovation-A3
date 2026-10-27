# Temperature Regression

## 1. Project Objective
Predict daily **maximum air temperature** (`temperature_2m_max`, °C) for Japanese locations using meteorological attributes. This is a **regression** task.

## 2. Dataset and Inputs

- Dataset: `dataset/temperature_preprocessed.csv`
- Features: `shortwave_radiation_sum`, `sunshine_duration`, `daylight_duration`, `cloud_cover_mean`, `dew_point_2m_mean`, `month`.
- Prediction target: `temperature_2m_max` (°C). The dataset also contains `temperature_2m_min` for exploratory analysis.
- The processed dataset in this archive contains **380,685 rows**.

## 3. Models

1. Multiple Linear Regression
2. Gradient Boosting Regressor
3. HistGradientBoostingRegressor

The training script is `train_temperature_models.py`. Saved models are found in `trained_models/`.

## 4. Folder Structure

```text
Temperature/
├── dataset/
│   └── temperature_preprocessed.csv
├── experiment_logs/
│   ├── baseline_v1/
│   ├── remove_cloud_cover_v1/
│   ├── remove_month_v1/
│   └── tune_hgb_v1/
├── trained_models/
│   ├── linear_regression_temp_max.joblib
│   ├── gradient_boosting_temp_max.joblib
│   ├── hist_gradient_boosting_temp_max.joblib
│   ├── training.csv
│   ├── testing.csv
│   └── model_results.csv
├── plots/                       
├── preprocess_temperature.py
├── data_analysis_temperature.py
├── train_temperature_models.py
├── test_trained_model.py
└── README.md
```

## 5. How to Use

Run commands in the **Temperature** project directory.

### Step 1 — Install dependencies

```powershell
python -m pip install numpy pandas matplotlib scikit-learn joblib
```

### Step 2 — Preprocess data (only if rebuilding)

```powershell
python -B preprocess_temperature.py
```

The preprocessing script expects source CSV folders at `../Data/Open-Meteo/Weather/`, `../Data/Open-Meteo/Daily_solar_dewpoint/`, and `../Data/Open-Meteo/Daily_cloud_humid_pressure/`. Those raw source folders **are not included** in this ZIP. You can skip this step and use the supplied processed dataset.

### Step 3 — Generate analysis plots

```powershell
python -B data_analysis_temperature.py
```

This generates PNG figures and `temperature_iqr_summary.csv` inside `plots/`. Plot generation does not alter the processed dataset or retrain the models.

### Step 4 — Train the models (optional)

```powershell
python -B train_temperature_models.py
```

Run the script from the `Temperature/` folder. Edit `EXPERIMENT_ID`, `REMOVE_FEATURES`, `TEST_SIZE`, or `MODEL_PARAM_OVERRIDES` near the top before starting a new experiment. Previously supplied models and train/test CSVs make retraining optional. Running training can overwrite existing model outputs in `trained_models/`.

### Step 5 — Test saved models

```powershell
python -B test_trained_model.py
```

Choose a test row or provide meteorological attributes manually when prompted.

## 6. Data Analysis Outputs

- `temperature_boxplots.png`: feature boxplots with IQR outlier counts; outlier markers are hidden to keep axes readable.
- `temperature_iqr_summary.csv`: first/third quartiles, IQR fences, and outlier percentages calculated from the full dataset.
- `temperature_distributions.png`: distributions of numeric weather features (sampled for plotting speed).
- `temperature_missing_values.png`: missing-value percentage per column.
- `temperature_correlations.png`: Pearson correlations among weather attributes and temperature targets.
- `temperature_target_distributions.png`: histograms of daily maximum and minimum temperature.
- `temperature_monthly_trends.png`: average maximum and minimum temperatures by month.
- `temperature_prefecture_coverage.png`: 20 prefectures with the most observations.
- `temperature_dewpoint_vs_max.png`: sampled scatter plot of dew point and maximum temperature.

## 7. Experiment Results and Important Notes

Experiment configurations and model comparisons are in `experiment_logs/`; saved predictors and training/testing subsets are in `trained_models/`.

**Data split clarification:** The earlier `info.md` described a 2023–2025 training / 2026 testing plan. However, the supplied `baseline_v1/experiment_config.json` records `test_size: 0.2` and `random_state: 42`. Consult the training script and saved datasets to establish the actual split used for each reported result rather than presenting the planned chronological split as verified.

Outlier counts based on the IQR rule are **descriptive**, not an instruction to delete extreme weather readings. Only load `.joblib` models from trusted sources.

`__pycache__/` files are disposable Python caches; run scripts with `python -B` to avoid generating them.
