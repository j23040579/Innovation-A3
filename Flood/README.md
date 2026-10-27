# Flood Risk Classification

## Quick Start — Folder Guide and How to Use

This guide explains how to run the Flood data analysis and where to find its outputs. The detailed project methodology is documented below.

### Folder structure

```text
Flood/
├── dataset/
│   └── flood_preprocessed.csv     
├── plots/                          
├── experiment_logs/                 
├── trained_models/                 
├── flood_treshold_finder/           
├── preprocess_flood.py            
├── data_analysis_flood.py          
├── train_flood_models.py          
├── test_trained_model.py            # Interactive saved-model tester
└── info.md
```

### How to use

**1. Install the analysis and training dependencies** (run commands in PowerShell or a terminal opened in the `Flood/` folder):

```powershell
python -m pip install numpy pandas matplotlib scikit-learn joblib
```

**2. Prepare the dataset.** The included `dataset/flood_preprocessed.csv` can be used directly. To regenerate it from the source data, run:

```powershell
python -B preprocess_flood.py
```

Note: preprocessing expects the Open-Meteo source files in `../Data/Open-Meteo/` relative to the Flood folder; these source files are not required if you already have the processed CSV.

**3. Generate the data-analysis figures:**

```powershell
python -B data_analysis_flood.py
```

The script reads `dataset/flood_preprocessed.csv` and automatically creates `plots/` if necessary. It also supports an alternative location (`dataset/processed/flood_preprocessed.csv`) or a custom CSV path:

```powershell
python -B data_analysis_flood.py --input "path/to/flood_preprocessed.csv"
```

**4. Review the outputs in `plots/`:**

- `flood_boxplots.png` — feature outliers and spread (1.5 × IQR).
- `flood_distributions.png` — numerical feature distributions.
- `flood_missing_values.png` — missing-value percentages.
- `flood_correlations.png` — numerical feature correlations.
- `flood_class_distribution.png` — Low/Medium/High class counts.
- `flood_monthly_risk.png` — risk-class proportions by month.
- `flood_town_coverage.png` — top towns by record count.
- `flood_iqr_summary.csv` — quartiles, IQR bounds and flagged outlier counts.

Some class, month, or town charts are generated only when their respective columns exist. IQR flags describe unusual values; they do not automatically indicate erroneous records.

**5. Train and evaluate the classification models** (optional if you only need the saved outputs):

```powershell
python -B train_flood_models.py
```

Edit `EXPERIMENT_ID`, `REMOVE_FEATURES`, and `TEST_SIZE` near the top of `train_flood_models.py` before running a new experiment. The script trains Gradient Boosting, CART and an ID3-style entropy tree, displays evaluation figures, saves models and evaluation files to `trained_models/`, and records experiments in `experiment_logs/`. Its training run can overwrite existing files in `trained_models/`; generating analysis plots in Step 3 does **not** retrain the models.

### 6. Test saved flood models (interactive)

From the `Flood/` directory, run:

```powershell
python -B test_trained_model.py
```

The tester reads `trained_models/testing.csv` and loads the following saved models from `trained_models/`: `cart_flood.joblib`, `gradient_boosting_flood.joblib`, and `id3_flood.joblib`. All three model files must exist for the current script to start.

Choose **1** to select a row from `testing.csv` by its zero-based index and compare predictions with the actual `flood_class` (when present). Choose **2** to enter the flood-condition attributes manually. The tester prints each model's predicted class and, when supported, class probabilities.

**Feature compatibility:** The current tester obtains its feature list from the first loaded model and reuses that list for all three models. Therefore, the saved models must have the same trained input columns in the same order. Models trained with different attribute subsets require an update to the testing script before they can be compared reliably.

**Environment:** Load `.joblib` files with a compatible scikit-learn version (ideally the version used for training). If you see a model-loading error such as `No module named '_loss'`, check the Python interpreter and installed scikit-learn version.

Python can recreate `__pycache__/`; using `python -B` suppresses bytecode caching for the script run.

---

## 1. Project Objective

The Flood component predicts a daily **flood risk level** for locations
in Japan.

Final classes: - **Low** - **Medium** - **High**

This is a classification task.

The small historical flood-event dataset is **not** the final
machine-learning training dataset. It is a reference dataset used to
study flood conditions and derive project-specific thresholds.

## 2. Overall Pipeline

``` text
Known historical flood events / GLIDE
        ↓
japan_flood_training_dataset.csv
        ↓
Retrieve/check Open-Meteo historical weather and river conditions
        ↓
Compare flood vs non-flood conditions
        ↓
Derive project-specific thresholds
        ↓
Apply conditions to individual daily Open-Meteo datasets
        ↓
Concatenate individual daily datasets
        ↓
Generate Low / Medium / High flood-risk labels
        ↓
Preprocess final large ML dataset
        ↓
2023–2025 training / 2026 testing
        ↓
CART / Gradient Boosting / ID3-style Decision Tree
```

## 3. Historical Flood Reference Dataset

Reference dataset:

``` text
japan_flood_training_dataset.csv
```

It contains: - 25 known flood examples - 25 non-flood examples - 50 rows
total

Its purpose is to compare weather and river-discharge conditions
associated with flood and non-flood cases and derive candidate
thresholds.

**Important:** This is not the final ML training dataset.

## 4. Historical Window

For each historical event, the reference builder examines the **previous
7 complete days**:

``` python
start = anchor - pd.Timedelta(days=7)
end   = anchor - pd.Timedelta(days=1)
```

The event day itself is excluded from the historical 7-day aggregation.

## 5. Data Sources

Historical flood events / GLIDE provide known flood dates and locations.

Open-Meteo historical weather provides: - `rain_sum` -
`precipitation_sum` - `precipitation_hours`

Open-Meteo Flood API provides: - `river_discharge`

Elevation is also included as a location/environmental feature.

## 6. Reference Features

``` text
rain_sum_past_3day
rain_sum_past_7day
max_daily_rain_past_7day
rain_flag_50mm
precipitation_hours_past_7day
river_discharge
river_discharge_mean_7day
river_discharge_median_7day
river_discharge_max_7day
discharge_ratio
elevation
```

### Rain features

-   `rain_sum_past_3day`: total rainfall during the previous 3 days.
-   `rain_sum_past_7day`: total rainfall during the previous 7 days.
-   `max_daily_rain_past_7day`: highest single-day rainfall during the
    previous 7 days.
-   `rain_flag_50mm`: indicates whether rainfall reached the project's
    50 mm condition.
-   `precipitation_hours_past_7day`: total precipitation hours during
    the previous 7 days.

### River features

-   `river_discharge`: river discharge associated with the evaluated
    date/location.
-   `river_discharge_mean_7day`: mean river discharge over the
    historical 7-day period.
-   `river_discharge_median_7day`: median river discharge over the
    historical 7-day period.
-   `river_discharge_max_7day`: maximum river discharge over the
    historical 7-day period.
-   `discharge_ratio`: increase in river discharge relative to its
    earlier/baseline condition.

### Location feature

-   `elevation`: elevation of the evaluated location.

## 7. Flood vs Non-Flood Comparison

  Indicator                                   Non-flood median   Flood median
  ----------------------------------------- ------------------ --------------
  Rain past 3 days                                        0.90          46.30
  Rain past 7 days                                       16.20          71.40
  Maximum daily rain previous 7 days                      9.40          36.80
  Precipitation hours previous 7 days                       24             58
  Current river discharge                                 0.94           9.47
  Mean river discharge previous 7 days                    1.14           2.64
  Median river discharge previous 7 days                  0.94           0.52
  Maximum river discharge previous 7 days                 2.56           9.47
  Discharge ratio                                        0.64x          3.14x
  Elevation                                                 80             80

The strongest differences are visible in accumulated rainfall, maximum
daily rainfall, precipitation duration, river discharge, maximum river
discharge, and discharge ratio.

## 8. Candidate Project Thresholds
I have rewrittern the treshold, this treshold is based on the Glide events matching with the Open-meteo weather. I analyzed based on there

``` text
rain_sum_past_3day             >= 46.30
rain_sum_past_7day             >= 71.40
max_daily_rain_past_7day       >= 36.80
precipitation_hours_past_7day  >= 58
river_discharge                >= 9.47
river_discharge_mean_7day      >= 2.64
river_discharge_max_7day       >= 9.47
discharge_ratio                >= 3.14
```

These are **project-derived candidate thresholds** based on the current
reference dataset. They are not official Japanese flood-warning
thresholds because I am not sure how to find. Even in theory its hard to find.

## 9. Creating the Final Daily Dataset

After deriving the flood-related conditions, they are applied to the
individual daily Open-Meteo datasets.

For each location/date, preprocessing calculates the required rolling
rainfall and river-discharge features.

The individual datasets are then concatenated into one large dataset for
ML training and testing.

Therefore:

``` text
50-row historical dataset
        ↓
derive conditions/thresholds

Daily Open-Meteo datasets
        ↓
calculate flood indicators
        ↓
apply conditions
        ↓
Low / Medium / High labels
        ↓
concatenate
        ↓
final ML dataset
```

## 10. Avoiding Future-Data Leakage

Rolling historical features must use information available **before the
day being classified**.

For example:

``` python
group["rain_sum"].shift(1).rolling(...)
```

The same principle applies to historical river-discharge features.

This prevents future/current-day information from leaking into
historical rolling features.

## 11. Flood Risk Labels

The final classes are:

``` text
Low
Medium
High
```

The current approach combines multiple rainfall and river conditions
rather than relying on one measurement.

The current Low/Medium/High rule is **project-defined** and should be
validated against the historical flood/non-flood reference examples.

## 12. Machine-Learning Split

``` text
2023–2025 → Training
2026      → Testing
```

This time-based split trains the models using historical observations
and evaluates them using later unseen observations.

For the current project, data is only required through:

``` text
2026-01-31
```

Therefore the actual testing period is:

``` text
2026-01-01 → 2026-01-31
```

Dates after January 31, 2026 are not required.

## 13. Models

The Flood component uses:

1.  **CART / Decision Tree**
2.  **Gradient Boosting**
3.  **ID3-style Decision Tree**

General model flow:

``` text
Flood-condition features
        ↓
Classification model
        ↓
Low / Medium / High
```

## 14. Important Dataset Distinction

### Reference dataset

``` text
japan_flood_training_dataset.csv
```

Used for:

``` text
Known flood/non-flood examples
→ compare conditions
→ derive candidate thresholds
```

### Final ML dataset

Created from:

``` text
Individual daily Open-Meteo datasets
→ rolling rainfall/river indicators
→ flood-risk conditions
→ Low / Medium / High labels
→ concatenate
→ train/test models
```

Do **not** describe the 50-row reference dataset as the final model
training dataset.

## 15. Current Limitations

The candidate thresholds come from a relatively small reference dataset
of 50 observations.

The Low / Medium / High labelling rule is project-defined and still
needs validation.

There is also a target-leakage consideration. If the labels are
deterministically generated from specific rainfall and river-discharge
features and those exact same features are supplied directly to the
classifier, the model may mainly learn to reproduce the labelling rule.

Model accuracy therefore needs to be interpreted together with the
method used to create the target labels.

## 16. Summary

The Flood project uses known historical flood events to identify
rainfall and river-discharge patterns associated with flooding.

The historical event dataset is a **reference for threshold
development**, while the actual machine-learning dataset comes from the
much larger daily Open-Meteo datasets.

``` text
Historical flood evidence
→ derive flood conditions
→ process daily weather + river data
→ calculate rolling indicators
→ generate Low / Medium / High risk labels
→ concatenate locations
→ train on 2023–2025
→ test on Jan 2026
→ compare CART, Gradient Boosting and ID3-style models
```
