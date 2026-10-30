#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Standalone Python version of train_flood_models(1).ipynb.

Converted from notebook code in its original execution order.
Edit the existing Settings / STANDARD EXPERIMENT CONTROL section below.
Run from the same working directory you used for the notebook:
    python train_flood_models.py

No training, evaluation, model selection or output paths were altered.
"""

def display(*objects):
    """Print values that appeared as rich cell output in the notebook."""
    for obj in objects:
        print(obj)

# %% — original code cell 1
# STANDARD EXPERIMENT CONTROL — edit only this cell for normal experiments
EXPERIMENT_ID = "final_test"  # e.g. remove_month_v1, split_30pct_v1
REMOVE_FEATURES = ["month"]           # e.g. ["month"] — use actual predictor column names
TEST_SIZE = 0.20               # 0.20=80/20, 0.30=70/30, 0.10=90/10
RANDOM_STATE = 42              # fixed seed makes group splits reproducible


MODEL_PARAM_OVERRIDES = {}
assert 0 < TEST_SIZE < 1, "TEST_SIZE must be between 0 and 1"

# %% [markdown] — original cell 2
# # Flood Classification — Visualise, Split, Train & Save
# Project-derived daily flood-risk classes: **Low, Medium, High**.
#
# Training: **2023–2025**  
# Testing: **2026**
#
# Models: **Gradient Boosting, CART, ID3-style Entropy Tree**.

# %% — original code cell 3
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import pandas as pd, numpy as np, matplotlib.pyplot as plt, joblib
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, ConfusionMatrixDisplay

R = Path(__file__).resolve().parent
D=R/"dataset"/"flood_preprocessed.csv"; M=R/"trained_models"; M.mkdir(exist_ok=True)

F=[
    "rain_sum_past_3day",
    "rain_sum_past_7day",
    "max_daily_rain_past_7day",
    "precipitation_hours_past_7day",
    "river_discharge_previous_day",
    "river_discharge_mean_7day",
    "river_discharge_median_7day",
    "river_discharge_max_7day",
    "discharge_ratio",
    "elevation",
    "month"
]
T="flood_class"; C=["Low","Medium","High"]


F = [c for c in F if c not in REMOVE_FEATURES] 
print("Experiment features:", F)
df=pd.read_csv(D); df["date"]=pd.to_datetime(df.date)
print(df.shape,df.date.min(),df.date.max()); display(df.head()); display(df[F+[T]].isna().sum().to_frame("missing"))

# %% [markdown] — original cell 4
# ## Plot 1 — Class distribution
# Check Low / Medium / High class imbalance before training.

# %% — original code cell 5
counts=df[T].value_counts().reindex(C,fill_value=0); counts.plot(kind="bar",figsize=(9,5)); plt.title("Flood-risk class distribution"); plt.ylabel("Daily observations"); plt.xticks(rotation=0); plt.tight_layout(); plt.show()
display(pd.DataFrame({"count":counts,"percent":(100*counts/counts.sum()).round(2)}))

# %% [markdown] — original cell 6
# ## Plot 2: 3-day rainfall distribution
# Inspect the distribution of accumulated rainfall during the previous three complete days.

# %% — original code cell 7
plt.figure(figsize=(10,5)); plt.hist(df.rain_sum_past_3day.dropna(),bins=100); plt.title("Previous 3-day rainfall distribution"); plt.xlabel("rain_sum_past_3day (mm)"); plt.ylabel("Observations"); plt.tight_layout(); plt.show()
display(df.rain_sum_past_3day.describe(percentiles=[.5,.75,.9,.95,.99,.995,.999]))

# %% [markdown] — original cell 8
# ## Plot 3 — Monthly class distribution

# %% — original code cell 9
pd.crosstab(df.month,df[T]).reindex(columns=C,fill_value=0).plot(kind="bar",stacked=True,figsize=(11,6)); plt.title("Flood-risk classes by month"); plt.ylabel("Daily observations"); plt.tight_layout(); plt.show()

# %% [markdown] — original cell 10
# ## Plot 4 — Correlation heatmap

# %% — original code cell 11
corr=df[F].corr(); fig,ax=plt.subplots(figsize=(11,9)); im=ax.imshow(corr); ax.set_xticks(range(len(corr))); ax.set_yticks(range(len(corr))); ax.set_xticklabels(corr.columns,rotation=75,ha="right"); ax.set_yticklabels(corr.columns); fig.colorbar(im,ax=ax); plt.title("Flood feature correlation"); plt.tight_layout(); plt.show()

# %% [markdown] — original cell 12
# ## Chronological train/test split
#
# Set `TEST_SIZE` in the first cell. The earliest dates train the model; the latest dates are held out for testing. Rows from the same date stay together, so the actual fraction may differ slightly. Keep the split fixed when comparing feature removal or hyperparameters.

# %% — original code cell 13
# Chronological train/test split: earliest dates train, latest dates test.
# TEST_SIZE is a fraction of eligible rows, not a percentage of calendar years.
req = F + [T, "date"]
missing = [c for c in req if c not in df]
assert not missing, f"Missing columns: {missing}"
assert F, "At least one predictor must remain after REMOVE_FEATURES"
d = df.dropna(subset=req).sort_values("date", kind="stable").copy()
assert len(d) >= 2, "Need at least two complete rows for train/test split"
cutoff = int(len(d) * (1 - TEST_SIZE))
assert 0 < cutoff < len(d), "TEST_SIZE leaves an empty train or test set"
train, test = d.iloc[:cutoff].copy(), d.iloc[cutoff:].copy()
# Prevent the same date from appearing in both partitions (multiple towns/day).
boundary_date = test["date"].iloc[0]
train = d[d["date"] < boundary_date].copy()
test = d[d["date"] >= boundary_date].copy()
assert len(train) and len(test), "Not enough distinct dates to make a chronological split"
Xtr, ytr = train[F], train[T]
Xte, yte = test[F], test[T]
train.to_csv(M / "training.csv", index=False)
test.to_csv(M / "testing.csv", index=False)
print(f"Requested test fraction: {TEST_SIZE:.0%}")
print(f"Actual row fraction: train={len(train)/len(d):.1%}, test={len(test)/len(d):.1%}")
print("Train:", len(train), train.date.min(), "to", train.date.max())
print("Test: ", len(test), test.date.min(), "to", test.date.max())
display(pd.DataFrame({"train": ytr.value_counts().reindex(C, fill_value=0),
                      "test": yte.value_counts().reindex(C, fill_value=0)}))

# %% [markdown] — original cell 14
# ## Train three classifiers

# %% — original code cell 15
models={
    "Gradient Boosting":GradientBoostingClassifier(random_state=RANDOM_STATE),
    "CART":DecisionTreeClassifier(random_state=RANDOM_STATE,class_weight="balanced"),
    "ID3-style Entropy Tree":DecisionTreeClassifier(criterion="entropy",random_state=RANDOM_STATE,class_weight="balanced")
}
rows=[]; preds={}
for name,m in models.items():
 if name in MODEL_PARAM_OVERRIDES: m.set_params(**MODEL_PARAM_OVERRIDES[name])
 print("Training",name); m.fit(Xtr,ytr); p=m.predict(Xte); preds[name]=p
 rows.append({"Model":name,"Accuracy":accuracy_score(yte,p),"Macro Precision":precision_score(yte,p,average="macro",zero_division=0),"Macro Recall":recall_score(yte,p,average="macro",zero_division=0),"Macro F1":f1_score(yte,p,average="macro",zero_division=0)})
results=pd.DataFrame(rows).sort_values("Macro F1",ascending=False); display(results)

# %% [markdown] — original cell 16
# ## Detailed reports and confusion matrices

# %% — original code cell 17
for name,p in preds.items():
 print("\n",name); print(classification_report(yte,p,labels=C,zero_division=0))
 ConfusionMatrixDisplay.from_predictions(yte,p,labels=C,xticks_rotation=25); plt.title(name+" confusion matrix"); plt.tight_layout(); plt.show()

# %% [markdown] — original cell 18
# ## Feature importance

# %% — original code cell 19
for name in ["Gradient Boosting","CART","ID3-style Entropy Tree"]:
 pd.Series(models[name].feature_importances_,index=F).sort_values().plot(kind="barh",figsize=(8,6)); plt.title(name+" feature importance"); plt.tight_layout(); plt.show()

# %% [markdown] — original cell 20
# ## Save models and results

# %% — original code cell 21
names={"Gradient Boosting":"gradient_boosting_flood.joblib","CART":"cart_flood.joblib","ID3-style Entropy Tree":"id3_flood.joblib"}
for n,m in models.items(): joblib.dump(m,M/names[n]); print("Saved",M/names[n])
results.to_csv(M/"model_results.csv",index=False); print("Done:",M)

# %% [markdown] — original cell 22
# ## Experiment log (run after training)
#
# The CSV and JSON are intended for reporting. This cell does **not** retrain or tune anything. Record the score table above and compare it with earlier runs. Review data leakage and validation methodology before claiming improvements.

# %% — original code cell 23
from pathlib import Path
import json, datetime
import pandas as pd
experiment_root = Path.cwd() / "experiment_logs" / EXPERIMENT_ID
experiment_root.mkdir(parents=True, exist_ok=True)
active_features = globals().get("FEATURES", globals().get("feature_columns", globals().get("F", [])))
metadata = {"experiment_id": EXPERIMENT_ID, "notebook": "train_flood_models", "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "features": list(active_features), "removed": REMOVE_FEATURES, "test_size_requested": TEST_SIZE, "random_state": RANDOM_STATE,
 "train_rows": len(train), "test_rows": len(test), "train_end": str(train.date.max()), "test_start": str(test.date.min()), 
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
