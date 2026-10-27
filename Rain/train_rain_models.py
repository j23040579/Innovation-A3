#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Standalone Python version of train_rain_models.ipynb.

Converted from notebook code for the final_test experiment configuration.
Trains Gradient Boosting and CART classifiers and saves them to trained_models/.
"""

import matplotlib
matplotlib.use('Agg')
from pathlib import Path
import json, datetime, time
import pandas as pd, numpy as np, matplotlib.pyplot as plt, joblib
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, ConfusionMatrixDisplay

# STANDARD EXPERIMENT CONTROL
EXPERIMENT_ID = "final_test"
REMOVE_FEATURES = ["temperature_2m_min"]
TEST_SIZE = 0.20
RANDOM_STATE = 42
MODEL_PARAM_OVERRIDES = {}

def main():
    R = Path.cwd()
    R = R if R.name.lower() == "rain" else (R / "Rain" if (R / "Rain").exists() else R.parent / "Rain")
    D = R / "dataset" / "rain_preprocessed.csv"
    M = R / "trained_models"
    M.mkdir(exist_ok=True)

    F = [
        "temperature_2m_max",
        "temperature_2m_min",
        "relative_humidity_2m_mean",
        "dew_point_2m_mean",
        "cloud_cover_mean",
        "pressure_msl_mean",
        "wind_speed_10m_max",
        "shortwave_radiation_sum",
        "month",
    ]
    T = "rain_class"
    C = ["No/Minimal Rain", "Low", "Moderate", "High"]

    F = [c for c in F if c not in REMOVE_FEATURES]
    print("Experiment ID:", EXPERIMENT_ID)
    print("Active features (F):", F)

    print("Loading preprocessed dataset from:", D)
    df = pd.read_csv(D)
    df["date"] = pd.to_datetime(df["date"])
    print("Shape:", df.shape, "Date range:", df["date"].min(), "to", df["date"].max())

    # Chronological train/test split: earliest dates train, latest dates test
    req = F + [T, "date"]
    missing = [c for c in req if c not in df.columns]
    assert not missing, f"Missing columns: {missing}"
    assert F, "At least one predictor must remain after REMOVE_FEATURES"

    d = df.dropna(subset=req).sort_values("date", kind="stable").copy()
    assert len(d) >= 2, "Need at least two complete rows for train/test split"

    cutoff = int(len(d) * (1 - TEST_SIZE))
    train, test = d.iloc[:cutoff].copy(), d.iloc[cutoff:].copy()
    boundary_date = test["date"].iloc[0]
    train = d[d["date"] < boundary_date].copy()
    test = d[d["date"] >= boundary_date].copy()
    assert len(train) and len(test), "Not enough distinct dates to make a chronological split"

    Xtr, ytr = train[F], train[T]
    Xte, yte = test[F], test[T]

    train.to_csv(M / "training.csv", index=False)
    test.to_csv(M / "testing.csv", index=False)
    print(f"Train rows: {len(train):,}, Test rows: {len(test):,}")

    models = {
        "Gradient Boosting": GradientBoostingClassifier(random_state=RANDOM_STATE),
        "CART": DecisionTreeClassifier(random_state=RANDOM_STATE, class_weight="balanced"),
    }

    names = {
        "Gradient Boosting": "gradient_boosting.joblib",
        "CART": "cart.joblib",
    }

    rows = []
    preds = {}

    for name, m in models.items():
        if name in MODEL_PARAM_OVERRIDES:
            m.set_params(**MODEL_PARAM_OVERRIDES[name])
        print("\n" + "=" * 60)
        print("Training", name, "...")
        print("=" * 60)
        start_t = time.time()
        m.fit(Xtr, ytr)
        dur = time.time() - start_t
        p = m.predict(Xte)
        preds[name] = p

        acc = accuracy_score(yte, p)
        prec = precision_score(yte, p, average="macro", zero_division=0)
        rec = recall_score(yte, p, average="macro", zero_division=0)
        f1 = f1_score(yte, p, average="macro", zero_division=0)

        print(f"{name} trained in {dur:.2f}s | Acc: {acc:.4f} | Macro F1: {f1:.4f}")
        rows.append({
            "Model": name,
            "Accuracy": acc,
            "Macro Precision": prec,
            "Macro Recall": rec,
            "Macro F1": f1,
            "Training time (s)": dur,
        })

        out_path = M / names[name]
        joblib.dump(m, out_path)
        print("Saved model to:", out_path)

    results = pd.DataFrame(rows).sort_values("Macro F1", ascending=False)
    print("\nModel Results:")
    print(results.to_string(index=False))
    results.to_csv(M / "model_results.csv", index=False)

    # Save experiment config log
    experiment_root = R / "experiment_logs" / EXPERIMENT_ID
    experiment_root.mkdir(parents=True, exist_ok=True)
    metadata = {
        "experiment_id": EXPERIMENT_ID,
        "notebook": "train_rain_models",
        "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "features": list(F),
        "removed": REMOVE_FEATURES,
        "test_size_requested": TEST_SIZE,
        "random_state": RANDOM_STATE,
        "train_rows": len(train),
        "test_rows": len(test),
        "train_end": str(train["date"].max()),
        "test_start": str(test["date"].min()),
        "model_overrides": MODEL_PARAM_OVERRIDES,
        "note": "Test metrics are descriptive; tune using validation data, not test data.",
    }
    (experiment_root / "experiment_config.json").write_text(json.dumps(metadata, indent=2, default=str), encoding="utf-8")
    results.to_csv(experiment_root / "model_comparison.csv", index=False)
    print("Experiment log saved to:", experiment_root)
    print("All Rain models retrained and saved successfully!")

if __name__ == "__main__":
    main()
