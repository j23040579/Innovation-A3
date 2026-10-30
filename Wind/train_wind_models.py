#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Standalone Python version of train_wind_models(3).ipynb.

Converted from notebook code in its original execution order.
Edit the existing Settings / STANDARD EXPERIMENT CONTROL section below.
Run from the same working directory you used for the notebook:
    python train_wind_models.py

No training, evaluation, model selection or output paths were altered.
"""

def display(*objects):
    """Print values that appeared as rich cell output in the notebook."""
    for obj in objects:
        print(obj)

# %% [markdown] — original cell 1
# # Shared experiment workflow
#
# Edit the **STANDARD EXPERIMENT CONTROL** cell, then run the notebook top to bottom. Change `EXPERIMENT_ID` for each run. Try a baseline, remove one feature, adjust one model parameter, or vary `TEST_SIZE`. The examples are commented out; uncomment only the desired entries.
#
# **Evaluation:** For a fair feature/parameter comparison, keep the split and random seed fixed. Changing the split is a separate experiment. The held-out test set is for final assessment, not repeated parameter selection. For daily weather regression, splitting is chronological; for typhoon notebooks, storms/events are kept together to prevent leakage.
#
# **Reporting:** Record experiment ID, removed features, test ratio, parameters, metric, and interpretation. Each run writes a configuration JSON and available result CSV.

# %% — original code cell 2
# STANDARD EXPERIMENT CONTROL — edit only this cell for normal experiments
EXPERIMENT_ID = "final_test"  # e.g. remove_month_v1, split_30pct_v1
REMOVE_FEATURES = []           # e.g. ["month"] — use actual predictor column names
TEST_SIZE = 0.20               # 0.20=80/20, 0.30=70/30, 0.10=90/10
RANDOM_STATE = 42              # fixed seed makes group splits reproducible

#Example of Model param overrides.
# "Gradient Boosting": {"n_estimators": 300, "learning_rate": 0.03, "max_depth": 4, "subsample": 0.8},
# "HistGradientBoosting": {"max_iter": 300, "max_leaf_nodes": 20, "l2_regularization": 0.1},
# "Multiple Linear Regression": {"fit_intercept": False},
MODEL_PARAM_OVERRIDES = {"HistGradientBoosting": {"max_iter": 300, "max_leaf_nodes": 20, "l2_regularization": 0.1}}
assert 0 < TEST_SIZE < 1, "TEST_SIZE must be between 0 and 1"

# %% [markdown] — original cell 3
# # Wind Speed Regression — Model Training and Comparison
#
# This notebook trains and compares three regression models:
#
# 1. Multiple Linear Regression
# 2. Gradient Boosting Regressor
# 3. HistGradientBoostingRegressor
#
# ### Input (X)
# - `surface_pressure_mean`
# - `surface_pressure_max`
# - `surface_pressure_min`
# - `pressure_change`
# - `wind_direction_10m_dominant`
#
# ### Output (y)
# - `wind_speed_10m_max` in km/h
#
# The dataset is split chronologically:
# - **2023–2025:** training
# - **2026:** testing
#
# Evaluation metrics:
# - MAE
# - RMSE
# - R²

# %% — original code cell 4
from pathlib import Path
import time
import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor, HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Resolve project directory.
ROOT = Path(__file__).resolve().parent

DATA_FILE = ROOT / "dataset" / "wind_preprocessed.csv"
MODEL_DIR = ROOT / "trained_models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

FEATURES = [
    "surface_pressure_mean",
    "surface_pressure_max",
    "surface_pressure_min",
    "pressure_change",
    "wind_direction_10m_dominant",
]

TARGET = "wind_speed_10m_max"


FEATURES = [c for c in FEATURES if c not in REMOVE_FEATURES]
print("Experiment features:", FEATURES)
print("Project root:", ROOT)
print("Dataset:", DATA_FILE)

# %% [markdown] — original cell 5
# ## 1. Load the preprocessed Wind dataset

# %% — original code cell 6
df = pd.read_csv(DATA_FILE)
df["date"] = pd.to_datetime(df["date"], errors="coerce")

required = ["date"] + FEATURES + [TARGET]
missing = [c for c in required if c not in df.columns]

if missing:
    raise KeyError(f"Missing required columns: {missing}")

for c in FEATURES + [TARGET]:
    df[c] = pd.to_numeric(df[c], errors="coerce")

df = df.dropna(subset=required).copy()
df = df.sort_values("date").reset_index(drop=True)

print("Rows:", f"{len(df):,}")
print("Date range:", df["date"].min(), "to", df["date"].max())
display(df.head())

# %% [markdown] — original cell 7
# ## 2. Basic Wind Speed Distribution

# %% — original code cell 8
print(df[TARGET].describe())

plt.figure(figsize=(9, 5))
plt.hist(df[TARGET], bins=40)
plt.xlabel("Maximum daily wind speed (km/h)")
plt.ylabel("Frequency")
plt.title("Distribution of Maximum Daily Wind Speed")
plt.show()

# %% [markdown] — original cell 9
# ## 3. Chronological Train/Test Split

# %% — original code cell 10
split_at = int(len(df) * (1 - TEST_SIZE))
train = df.iloc[:split_at].copy()
test = df.iloc[split_at:].copy()

if train.empty:
    raise ValueError("Training set is empty.")
if test.empty:
    raise ValueError("Testing set is empty.")

X_train = train[FEATURES]
y_train = train[TARGET]

X_test = test[FEATURES]
y_test = test[TARGET]

print("Training rows:", f"{len(train):,}")
print("Testing rows :", f"{len(test):,}")
print("Training:", train["date"].min(), "to", train["date"].max())
print("Testing :", test["date"].min(), "to", test["date"].max())

train.to_csv(MODEL_DIR / "training.csv", index=False)
test.to_csv(MODEL_DIR / "testing.csv", index=False)

print("Saved training.csv and testing.csv")

# %% [markdown] — original cell 11
# ## 4. Define Models
#
# `HistGradientBoostingRegressor` is included as the more computationally efficient
# tree-based boosting model for larger datasets.
#
# Random Forest and MARS are not used in this experiment.

# %% — original code cell 12
models = {
    "Multiple Linear Regression": LinearRegression(),

    "Gradient Boosting": GradientBoostingRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=3,
        random_state=42
    ),

    "HistGradientBoosting": HistGradientBoostingRegressor(
        learning_rate=0.1,
        max_iter=200,
        max_leaf_nodes=31,
        random_state=42
    ),
}

MODEL_FILES = {
    "Multiple Linear Regression": "multiple_linear_regression.joblib",
    "Gradient Boosting": "gradient_boosting.joblib",
    "HistGradientBoosting": "hist_gradient_boosting.joblib",
}

for name, estimator in models.items():
    if name in MODEL_PARAM_OVERRIDES:
        estimator.set_params(**MODEL_PARAM_OVERRIDES[name])
models

# %% [markdown] — original cell 13
# ## 5. Train, Predict, Evaluate and Save

# %% — original code cell 14
results = []
predictions = {}

for name, model in models.items():
    print("\n" + "=" * 70)
    print("Training:", name)
    print("=" * 70)

    start = time.time()

    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    elapsed = time.time() - start

    mae = mean_absolute_error(y_test, pred)
    rmse = np.sqrt(mean_squared_error(y_test, pred))
    r2 = r2_score(y_test, pred)

    results.append({
        "Model": name,
        "MAE (km/h)": mae,
        "RMSE (km/h)": rmse,
        "R²": r2,
        "Training time (s)": elapsed,
    })

    predictions[name] = pred

    path = MODEL_DIR / MODEL_FILES[name]
    joblib.dump(model, path)

    print(f"MAE : {mae:.4f} km/h")
    print(f"RMSE: {rmse:.4f} km/h")
    print(f"R²  : {r2:.4f}")
    print(f"Time: {elapsed:.2f} seconds")
    print("Saved:", path)

results_df = pd.DataFrame(results).sort_values("RMSE (km/h)").reset_index(drop=True)
results_df.to_csv(MODEL_DIR / "model_results.csv", index=False)

display(results_df)

# %% [markdown] — original cell 15
# ## 6. Actual vs Predicted

# %% — original code cell 16
for name, pred in predictions.items():
    plt.figure(figsize=(7, 6))
    plt.scatter(y_test, pred, alpha=0.25)

    low = min(y_test.min(), pred.min())
    high = max(y_test.max(), pred.max())
    plt.plot([low, high], [low, high])

    plt.xlabel("Actual wind speed (km/h)")
    plt.ylabel("Predicted wind speed (km/h)")
    plt.title(f"Actual vs Predicted — {name}")
    plt.show()

# %% [markdown] — original cell 17
# ## 7. Compare Errors

# %% — original code cell 18
plot_df = results_df.set_index("Model")

plt.figure(figsize=(9, 5))
plot_df[["MAE (km/h)", "RMSE (km/h)"]].plot(kind="bar", ax=plt.gca())
plt.ylabel("Error (km/h)")
plt.title("Wind Regression Model Error Comparison")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.show()

# %% [markdown] — original cell 19
# ## 8. Multiple Linear Regression Coefficients

# %% — original code cell 20
mlr = models["Multiple Linear Regression"]

coef_df = pd.DataFrame({
    "Feature": FEATURES,
    "Coefficient": mlr.coef_
}).sort_values("Coefficient", key=abs, ascending=False)

display(coef_df)

# %% [markdown] — original cell 21
# ## 9. Final Model Ranking
#
# For **MAE** and **RMSE**, lower is better.
#
# For **R²**, higher is better and values closer to 1 indicate that the model explains
# more of the variation in maximum wind speed.
#
# Do not select the final model from training time alone. Compare predictive performance
# and computational cost together.

# %% — original code cell 22
display(
    results_df[
        ["Model", "MAE (km/h)", "RMSE (km/h)", "R²", "Training time (s)"]
    ]
)

best = results_df.iloc[0]
print("Lowest RMSE model:", best["Model"])
print(f'RMSE: {best["RMSE (km/h)"]:.4f} km/h')
print(f'MAE : {best["MAE (km/h)"]:.4f} km/h')
print(f'R²  : {best["R²"]:.4f}')

# %% [markdown] — original cell 23
# ## Experiment log (run after training)
#
# The CSV and JSON are intended for reporting. This cell does **not** retrain or tune anything. Record the score table above and compare it with earlier runs. Review data leakage and validation methodology before claiming improvements.

# %% — original code cell 24
from pathlib import Path
import json, datetime
import pandas as pd
experiment_root = ROOT / "experiment_logs" / EXPERIMENT_ID
experiment_root.mkdir(parents=True, exist_ok=True)
active_features = globals().get("FEATURES", globals().get("feature_columns", globals().get("F", [])))
metadata = {"experiment_id": EXPERIMENT_ID, "notebook": "train_wind_models_split", "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "features": list(active_features), "removed": REMOVE_FEATURES, "test_size": TEST_SIZE, "random_state": RANDOM_STATE, 
 "model_overrides": MODEL_PARAM_OVERRIDES, 
 "note": "Test metrics are descriptive; tune using validation data, not test data."}
(experiment_root / "experiment_config.json").write_text(json.dumps(metadata, indent=2, default=str), encoding="utf-8")
for key in ("results_df", "results"):
    obj = globals().get(key)
    if isinstance(obj, pd.DataFrame):
        obj.to_csv(experiment_root / "model_comparison.csv", index=False)
        display(obj)
        break
else:
    print("No tabular model comparison found; refer to evaluation outputs above.")
print("Experiment saved to:", experiment_root)
print("Report checklist: model | features | parameter changes | split | validation metric | test metric | training time | interpretation")
