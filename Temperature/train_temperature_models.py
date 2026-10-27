#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Standalone Python version of train_temperature_models(1).ipynb.

Converted from notebook code in its original execution order.
Edit the existing Settings / STANDARD EXPERIMENT CONTROL section below.
Run from the same working directory you used for the notebook:
    python train_temperature_models.py

No training, evaluation, model selection or output paths were altered.
"""

def display(*objects):
    """Print values that appeared as rich cell output in the notebook."""
    for obj in objects:
        print(obj)

# %% — original code cell 1
# STANDARD EXPERIMENT CONTROL — edit only this cell for normal experiments
EXPERIMENT_ID = "final_test"  # e.g. remove_month_v1, split_30pct_v1
REMOVE_FEATURES = []           # e.g. ["month"] — use actual predictor column names
TEST_SIZE = 0.20               # 0.20=80/20, 0.30=70/30, 0.10=90/10
RANDOM_STATE = 42              # fixed seed makes group splits reproducible

MODEL_PARAM_OVERRIDES = {"HistGradientBoosting": {"max_iter": 300, "max_leaf_nodes": 20, "l2_regularization": 0.1}}
assert 0 < TEST_SIZE < 1, "TEST_SIZE must be between 0 and 1"

# %% [markdown] — original cell 2
# # Temperature Regression Training
# Models: Multiple Linear Regression, Gradient Boosting Regressor, HistGradientBoostingRegressor.  
# Target: daily maximum temperature (`temperature_2m_max`).  
# Split: 2023–2025 train, 2026 test.

# %% — original code cell 3
from pathlib import Path
import time, joblib, numpy as np, pandas as pd, matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor, HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
ROOT=Path.cwd()
if ROOT.name.lower()!="temperature" and (ROOT/"Temperature").exists(): ROOT=ROOT/"Temperature"
M=ROOT/"trained_models"; M.mkdir(exist_ok=True)
F=["shortwave_radiation_sum","sunshine_duration","daylight_duration","cloud_cover_mean","dew_point_2m_mean","month"]
TARGET="temperature_2m_max"

F = [c for c in F if c not in REMOVE_FEATURES]
print("Experiment features:", F)
df=pd.read_csv(ROOT/"dataset"/"temperature_preprocessed.csv"); df["date"]=pd.to_datetime(df["date"])
df=df.dropna(subset=["date"]+F+[TARGET]).sort_values("date")
print("Rows:",len(df)); display(df.head())

# %% — original code cell 4
split_at = int(len(df) * (1 - TEST_SIZE))
train=df.iloc[:split_at].copy(); test=df.iloc[split_at:].copy()
if train.empty or test.empty: raise ValueError("Split resulted in an empty training or test set.")
train.to_csv(M/"training.csv",index=False); test.to_csv(M/"testing.csv",index=False)
Xtr=train[F]; Xte=test[F]
print("Training:",len(train),"Testing:",len(test))

# %% — original code cell 5
def models():
    return {
      "Multiple Linear Regression": LinearRegression(),
      "Gradient Boosting": GradientBoostingRegressor(
          n_estimators=200, learning_rate=.05, max_depth=3, random_state=42
      ),
      "HistGradientBoosting": HistGradientBoostingRegressor(
          learning_rate=.1, max_iter=200, max_leaf_nodes=31, random_state=42
      )
    }

filenames = {
    "Multiple Linear Regression": "linear_regression_temp_max.joblib",
    "Gradient Boosting": "gradient_boosting_temp_max.joblib",
    "HistGradientBoosting": "hist_gradient_boosting_temp_max.joblib",
}

rows = []
preds = {}

for name, model in models().items():
    if name in MODEL_PARAM_OVERRIDES: model.set_params(**MODEL_PARAM_OVERRIDES[name])
    st = time.time()
    model.fit(Xtr, train[TARGET])
    pred = model.predict(Xte)

    mae = mean_absolute_error(test[TARGET], pred)
    rmse = np.sqrt(mean_squared_error(test[TARGET], pred))
    r2 = r2_score(test[TARGET], pred)

    joblib.dump(model, M / filenames[name])

    rows.append({
        "Target": TARGET,
        "Model": name,
        "MAE (°C)": mae,
        "RMSE (°C)": rmse,
        "R²": r2,
        "Training time (s)": time.time() - st
    })
    preds[name] = pred

results = pd.DataFrame(rows)
results.to_csv(M / "model_results.csv", index=False)
display(results.sort_values("RMSE (°C)"))

# %% — original code cell 6
actual = test[TARGET]

for name in ["Multiple Linear Regression", "Gradient Boosting", "HistGradientBoosting"]:
    pred = preds[name]

    plt.figure(figsize=(7, 6))
    plt.scatter(actual, pred, alpha=.25)

    lo = min(actual.min(), pred.min())
    hi = max(actual.max(), pred.max())
    plt.plot([lo, hi], [lo, hi])

    plt.xlabel("Actual max temperature (°C)")
    plt.ylabel("Predicted max temperature (°C)")
    plt.title(f"Maximum Temperature — {name}")
    plt.show()

# %% [markdown] — original cell 7
# ## Experiment log (run after training)
#
# The CSV and JSON are intended for reporting. This cell does **not** retrain or tune anything. Record the score table above and compare it with earlier runs. Review data leakage and validation methodology before claiming improvements.

# %% — original code cell 8
from pathlib import Path
import json, datetime
import pandas as pd
experiment_root = Path.cwd() / "experiment_logs" / EXPERIMENT_ID
experiment_root.mkdir(parents=True, exist_ok=True)
active_features = globals().get("FEATURES", globals().get("feature_columns", globals().get("F", [])))
metadata = {"experiment_id": EXPERIMENT_ID, "notebook": "train_temperature_models", "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "features": list(active_features), "removed": REMOVE_FEATURES, "test_size": TEST_SIZE, "random_state": RANDOM_STATE, 
 "model_overrides": MODEL_PARAM_OVERRIDES, 
 "note": "Test metrics are descriptive; tune using validation data, not test data."}
(experiment_root / "experiment_config.json").write_text(json.dumps(metadata, indent=2, default=str), encoding="utf-8")
for key in ("results", "results_df"):
    obj = globals().get(key)
    if isinstance(obj, pd.DataFrame):
        obj.to_csv(experiment_root / "model_comparison.csv", index=False)
        display(obj)
        break
else:
    print("No tabular model comparison found; refer to evaluation outputs above.")
print("Experiment saved to:", experiment_root)
print("Report checklist: model | features | parameter changes | split | validation metric | test metric | training time | interpretation")
