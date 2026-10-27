# Wind Speed Regression — Project Guide

## 1. Project Objective

Predict **daily maximum wind speed at 10 m (`wind_speed_10m_max`, km/h)** from daily surface-pressure measurements, pressure change, and dominant wind direction. This is a **regression** task.

The project considers **Multiple Linear Regression**, **Gradient Boosting Regressor**, and **HistGradientBoostingRegressor**.

## 2. Folder Structure

```text
Wind/
├── dataset/
│   └── wind_preprocessed.csv        # Existing processed dataset
├── experiment_logs/                # Experiment configurations and model comparisons
├── trained_models/                 # Model artifacts and training/testing CSVs
├── plots/                          # Generated figures and IQR statistics
├── preprocess_wind.py              # Preprocessing from external Open-Meteo source folders
├── data_analysis_wind.py           # Creates analysis PNGs and IQR summary CSV
├── train_wind_models.py            # Standalone training script
├── README.md
└── .gitignore
```

## 3. How to Use

Open a terminal in `Wind/`.

**Step 1 — Install Python packages**

```powershell
python -m pip install numpy pandas matplotlib scikit-learn joblib
```

**Step 2 — Preprocess (only when the original external source folders are available)**

```powershell
python -B preprocess_wind.py
```

The preprocessing script expects source CSV folders at `../Data/Open-Meteo/Weather/` and `../Data/Open-Meteo/Daily_surface_pressure_wind_direction/`. **Those external source folders are not inside this ZIP.** The supplied `dataset/wind_preprocessed.csv` is ready for analysis without rerunning preprocessing.

**Step 3 — Generate data-analysis plots**

```powershell
python -B data_analysis_wind.py
```

Outputs are written automatically to `plots/`:

| Output | Description |
|---|---|
| `wind_boxplots.png` | Outlier and spread comparison for six numerical attributes |
| `wind_distributions.png` | Histograms of pressure, direction, and wind speed |
| `wind_missing_values.png` | Missing-value percentages by column |
| `wind_correlations.png` | Pearson correlations across numerical features |
| `wind_target_distribution.png` | Target wind-speed distribution and median |
| `wind_monthly_trends.png` | Mean and median daily maximum wind speed by month |
| `wind_prefecture_coverage.png` | Observations for the 20 most represented prefecture labels |
| `wind_direction_analysis.png` | Dominant wind direction distribution and wind-speed relationship |
| `wind_iqr_summary.csv` | Q1, Q3, IQR limits, and extreme-value counts for numerical features |

The IQR calculations use the **complete dataset**; dense histograms, boxplots, and direction scatterplots use reproducible samples for readability and performance. Wind direction is circular data, so ordinary linear correlations involving direction need caution.

**Step 4 — Train and evaluate models**

From the `Wind/` directory, execute the converted Python script:

```powershell
python -B train_wind_models.py
```

Edit `EXPERIMENT_ID`, `REMOVE_FEATURES`, `TEST_SIZE` or `MODEL_PARAM_OVERRIDES` near the top to configure a new experiment. The script trains the regression models, displays evaluation figures, and writes model files and evaluation data into `trained_models/`; existing files with matching names can be overwritten. No Jupyter installation is required.

## 4. Dataset and Experimental Outputs

- Input: `dataset/wind_preprocessed.csv` with date, prefecture, location, town, pressure measurements, pressure change, wind direction, and maximum wind speed.
- Model evaluation: `experiment_logs/` contains baseline and feature-removal/tuning experiment records.
- Saved artifacts: `trained_models/` contains training/testing CSVs, model results, and `.joblib` entries.
- The provided dataset spans **2021-01-02 through 2026-01-31**, with **458,432** records.

**Important:** The original guide described a 2023–2025 training / 2026 testing plan, while the baseline experiment configuration records `test_size: 0.2` and `random_state: 42`. The documented experiment does **not** by itself verify the planned chronological split.

## 5. Existing Source-File Issues (Not Altered)

The original project archive was reported to contain unresolved Git merge-conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) in some experimental files, as well as `.joblib` entries that were Git LFS pointers rather than working serialized models. The converted `train_wind_models.py` passed a Python syntax check, but its training was **not** run against the full dataset during conversion. If using older saved models, reconcile any conflicts and fetch valid Git LFS objects (for example, with `git lfs pull`) before loading them. The training script can create fresh model files once the dataset and Python dependencies are available.

## 6. Notes

The `plots/` folder is automatically created by `data_analysis_wind.py`. Run scripts using `python -B` to avoid generating `__pycache__/`. The original datasets, older model entries, and experiment logs remain separate from this instruction update.
