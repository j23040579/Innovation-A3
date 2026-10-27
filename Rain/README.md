# Rain — Project Folder Guide

## 1. Project Objective
Predict a daily rainfall class for Japanese locations from daily meteorological features. The target `rain_class` is derived from `rain_sum` using project-defined boundaries:

| Class | Daily rainfall |
|---|---|
| No/Minimal Rain | < 1 mm |
| Low | 1 to < 10 mm |
| Moderate | 10 to < 100 mm |
| High | ≥ 100 mm |

These categories are project-specific, **not official JMA warning classes**. Do not include `rain_sum` among the classifier inputs because it determines the target.

## 2. Folder Structure

```text
Rain/
├── dataset/
│   └── rain_preprocessed.csv
├── experiment_logs/        
├── trained_models/
│   ├── testing.csv
│   ├── cart.joblib
│   └── gradient_boosting.joblib
├── plots/                  
├── preprocess_rain.py
├── data_analysis_rain.py
├── train_rain_models.py
├── rain_test_trained_model_fixed.py
└── README.md
```

## 3. How to Use

Run commands from inside the `Rain/` folder.

### Step 1 — Set up the compatible Python environment (first-time setup only)
The saved CART and Gradient Boosting models were trained with **scikit-learn 1.8.0**. Use Python 3.13 and a dedicated virtual environment to avoid incompatible model-loading errors.

```powershell
py -3.13 -m venv .venv-rain
.\.venv-rain\Scripts\python.exe -m pip install "scikit-learn==1.8.0" pandas numpy scipy joblib matplotlib seaborn
```

Verify the installed versions:

```powershell
.\.venv-rain\Scripts\python.exe -c "import sys, sklearn; print(sys.version); print(sklearn.__version__)"
```

Expected: Python 3.13.x and scikit-learn 1.8.0. All commands below use the virtual environment explicitly; **do not use the system `python` command** if it points to Python 3.15.

### Step 2 — Prepare the dataset (only when preprocessing is needed)
```powershell
.\.venv-rain\Scripts\python.exe -B preprocess_rain.py
```

This project includes `dataset/rain_preprocessed.csv`. The preprocessing script may require its own input data files; verify its source paths before rerunning it. You can skip this step when using the included processed dataset.

### Step 3 — Generate data analysis figures
```powershell
.\.venv-rain\Scripts\python.exe -B data_analysis_rain.py
```

The script reads `dataset/rain_preprocessed.csv` and automatically exports PNG charts to `plots/`, plus `rain_iqr_summary.csv`. It creates `plots/` when missing. Boxplots and histograms use a reproducible sample of at most 40,000 rows for plotting speed; missing-value rates, IQR statistics, correlations, and class counts are computed using the full dataset.

### Step 4 — Evaluate all available saved models

```powershell
.\.venv-rain\Scripts\python.exe -B train_rain_models.py
```

**Important:** Despite its filename, the current `train_rain_models.py` is an **evaluation script**, not a model-training script. It does not fit or save new models. It loads `trained_models/testing.csv` and discovers `.joblib` models in `trained_models/`. For each model, it selects the saved training feature names **in their original order**, then prints accuracy, classification report, and confusion matrix. Extra CSV columns are ignored. Models without usable feature-name metadata may require an explicit `--feature-map`.

If `random_forest.joblib` is added to `trained_models/`, the evaluator discovers it automatically, provided the saved model is compatible and has the required feature information. There is no need to add a missing model just to test the others.

To evaluate only one model:

```powershell
.\.venv-rain\Scripts\python.exe -B train_rain_models.py --model cart.joblib
```

To export predictions:

```powershell
.\.venv-rain\Scripts\python.exe -B train_rain_models.py --save-predictions trained_models/predictions.csv
```

### Step 5 — Test an individual row or enter weather attributes

Use the updated interactive tester if it is present in your `Rain/` directory:

```powershell
.\.venv-rain\Scripts\python.exe -B rain_test_trained_model_fixed.py
```

- **Option 1:** Choose a row from `trained_models/testing.csv`.
- **Option 2:** Enter weather attributes manually.

The tester automatically detects available compatible models and supplies each model with its expected feature subset. It does not modify the saved models or dataset. If your local tester is instead named `rain_test_trained_model.py`, use that filename only if it contains the updated adaptive feature-selection logic.

### Step 6 — Verified evaluation results

The following results were produced from **85,932 testing rows** using the supplied models:

| Metric | CART | Gradient Boosting |
|---|---:|---:|
| Accuracy | 0.6697 | 0.7434 |
| Macro precision | 0.44 | 0.54 |
| Macro recall | 0.44 | 0.48 |
| Macro F1 | 0.44 | 0.50 |
| Weighted F1 | 0.67 | 0.73 |

Both models used eight training attributes (excluding `temperature_2m_min`). Gradient Boosting performed better overall, but High rainfall recall was low (2 of 52 High observations correctly predicted), so accuracy alone should not be used to judge rare-event detection.

## 4. Inputs and Outputs

**Candidate model feature columns (actual subset varies by saved model):** `temperature_2m_max`, `temperature_2m_min`, `relative_humidity_2m_mean`, `dew_point_2m_mean`, `cloud_cover_mean`, `pressure_msl_mean`, `wind_speed_10m_max`, `shortwave_radiation_sum`, and `month`.

**Analysis figures:** `rain_boxplots.png`, `rain_distributions.png`, `rain_log_transform_comparison.png`, `rain_missing_values.png`, `rain_correlations.png`, `rain_class_distribution.png`, `rain_monthly_classes.png`, and `rain_prefecture_coverage.png`.

**Analysis table:** `plots/rain_iqr_summary.csv` contains quartiles, 1.5×IQR fences, and outlier counts/percentages for numeric features. Outlier flags are exploratory and do not automatically mean observations should be deleted. The log1p figure is an analysis visualization, not a change to model training data.

## 5. Training and Evaluation Notes

Existing `experiment_logs/` contains baseline and feature-removal experiments with `experiment_config.json` and `model_comparison.csv`. Stored trained models and split files are under `trained_models/`. Evaluate with accuracy, macro precision, macro recall, macro F1, classification report, and confusion matrix; macro scores are useful with class imbalance.

**Important:** Although earlier notes describe a 2023–2025 training / 2026 testing split, the included `baseline_v1/experiment_config.json` records a 2025-01-24 train end and 2025-01-25 test start for that experiment. Check each saved experiment's actual split before describing its evaluation as a 2026 holdout.

## 6. Housekeeping

`__pycache__/` is a generated cache and is not required for submission. `python -B` suppresses Python bytecode generation. Jupyter is not needed to run these `.py` scripts. If `ModuleNotFoundError: No module named '_loss'` appears, check that the script is running with `.venv-rain` and scikit-learn 1.8.0. If feature-name mismatch errors appear, use the updated adaptive testing scripts. Only load `.joblib` files from trusted sources.
