# ============================================================
# Japan Snowfall Risk Predictor (Yamagata & Niigata) — 3 MODELS
# Models: Linear Regression (threshold), Logistic Regression,
#         Random Forest Classifier
# ============================================================

import logging
import warnings
import random
from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.model_selection import (
    GridSearchCV, StratifiedKFold, KFold,
    train_test_split, cross_val_predict,
)
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report,
    mean_squared_error, r2_score, mean_absolute_error,
)

# -----------------------------
# Global settings
# -----------------------------
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
warnings.filterwarnings("ignore")

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)


# -----------------------------
# Feature lists
# -----------------------------
FEATURES = [
    "max_temperature",
    "min_temperature",
    "max_humidity",
    "min_humidity",
    "max_wind_speed",
    "min_wind_speed_log",
]

REG_TARGET = "snowfall_sum_log"


# -----------------------------
# Project paths
# -----------------------------
def find_project_root(marker="src") -> Path:
    p = Path(__file__).resolve().parent
    for parent in [p, *p.parents]:
        if (parent / marker).is_dir():
            return parent
    raise RuntimeError(f"Could not find project root (folder containing '{marker}')")


PROJECT_ROOT  = find_project_root()
PROCESSED_DIR = PROJECT_ROOT / "dataset" / "processed"

DATASETS = {
    "Yamagata": PROCESSED_DIR / "Yamagata_winter_avg.csv",
    "Niigata":  PROCESSED_DIR / "Niigata_winter_avg.csv",
}


# -----------------------------
# Startup banner
# -----------------------------
log.info("=" * 60)
log.info("FEATURES:")
for f in FEATURES:
    log.info(f"  - {f}")
log.info("Models: Linear Regression (thr), Logistic Regression, Random Forest")
log.info("=" * 60)


# -----------------------------
# ThresholdWrapper
# -----------------------------
class ThresholdWrapper(BaseEstimator, ClassifierMixin):
    """Regression model + scaler + thresholds -> 3-class classifier.
    Pass RAW (unscaled) X to 'predict()'; scaling happens internally.
    """

    def __init__(self, regressor=None, scaler=None,
                 thr_med=None, thr_high=None, use_log=True):
        self.regressor = regressor
        self.scaler = scaler
        self.thr_med = thr_med
        self.thr_high = thr_high
        self.use_log = use_log

    def predict(self, X):
        X_arr = np.asarray(X, dtype=float)
        if self.scaler is not None:
            X_arr = self.scaler.transform(X_arr)
        y_hat = self.regressor.predict(X_arr)
        if self.use_log:
            y_hat = np.expm1(y_hat)
        y_hat = np.clip(y_hat, 0.0, None)
        return np.where(
            y_hat >= self.thr_high, 2,
            np.where(y_hat >= self.thr_med, 1, 0),
        ).astype(int)


# -----------------------------
# Threshold tuning (Out-Of-Fold)
# -----------------------------
def tune_thresholds(y_pred_cm, y_true_cls, n_steps=25):
    y_pred_cm = np.asarray(y_pred_cm).ravel()
    y_true_cls = np.asarray(y_true_cls).ravel()

    lo, hi = np.percentile(y_pred_cm, [2, 98])
    if hi <= lo:
        return float(np.median(y_pred_cm)), float(np.percentile(y_pred_cm, 80)), 0.0

    grid = np.linspace(lo, hi, n_steps)
    best = (float(grid[0]), float(grid[-1]), -1.0)

    for i in range(len(grid) - 1):
        for j in range(i + 1, len(grid)):
            thr_med, thr_high = float(grid[i]), float(grid[j])
            preds = np.where(
                y_pred_cm >= thr_high, 2,
                np.where(y_pred_cm >= thr_med, 1, 0),
            ).astype(int)
            score = f1_score(y_true_cls, preds, average="macro", zero_division=0)
            if score > best[2]:
                best = (thr_med, thr_high, score)
    return best


# -----------------------------
# Evaluation
# -----------------------------
def _present_labels(y_true, y_pred):
    return sorted(set(np.asarray(y_true).tolist()) |
                  set(np.asarray(y_pred).tolist()))


def evaluate_classifier(model, X_test, y_test, name, label_names=None):
    y_pred = model.predict(X_test)
    present = _present_labels(y_test, y_pred)
    label_names = label_names or [f"class_{i}" for i in range(3)]
    target_names = [label_names[i] for i in present]

    accuracy  = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average="weighted", zero_division=0)
    recall    = recall_score(y_test, y_pred, average="weighted", zero_division=0)
    f1        = f1_score(y_test, y_pred, average="weighted", zero_division=0)
    macro_f1  = f1_score(y_test, y_pred, average="macro", zero_division=0)

    log.info(f"\n--- {name} ---")
    log.info(f"Accuracy      : {accuracy:.4f}")
    log.info(f"F1 (weighted) : {f1:.4f}")
    log.info(f"F1 (MACRO)    : {macro_f1:.4f}")
    log.info(f"Precision(w)  : {precision:.4f}")
    log.info(f"Recall(w)     : {recall:.4f}")

    cm = confusion_matrix(y_test, y_pred, labels=present)
    log.info("\nConfusion Matrix (rows = actual, cols = predicted):")
    header = "True \\ Pred | " + " | ".join(f"{n:>7}" for n in target_names) + " |"
    log.info(header)
    log.info("-" * len(header))
    for i, row in enumerate(cm):
        row_str = " | ".join(f"{v:>7}" for v in row)
        log.info(f"{target_names[i]:>11} | {row_str} |")

    log.info("\nClassification Report:")
    log.info("\n" + classification_report(
        y_test, y_pred,
        labels=present,
        target_names=target_names,
        zero_division=0,
    ))

    return {
        "accuracy": accuracy, "precision": precision, "recall": recall,
        "f1_score": f1, "macro_f1": macro_f1,
        "y_pred": y_pred, "y_test": y_test,
        "confusion_matrix": cm,
    }


# -----------------------------
# Experiment runner (3 models)
# -----------------------------
def run_experiment(df, features_to_use,
                   label_names=("Low", "Medium", "High"),
                   do_cv=True):
    log.info("\n" + "=" * 80)
    log.info(f"Features: {features_to_use}")
    log.info("=" * 80)

    X      = df[features_to_use].values
    y_reg  = df[REG_TARGET].values
    y_snow = df["snowfall_sum"].values

    strat_bins = pd.qcut(y_snow, q=3, labels=False, duplicates="drop")

    (X_train, X_test,
     y_reg_train, y_reg_test,
     y_snow_train, y_snow_test) = train_test_split(
        X, y_reg, y_snow,
        test_size=0.20, random_state=SEED, stratify=strat_bins,
    )

    # Thresholds computed on Train only
    thr_med  = float(np.quantile(y_snow_train, 0.60))
    thr_high = float(np.quantile(y_snow_train, 0.85))

    def to_cls(s):
        s = np.asarray(s)
        return np.where(s >= thr_high, 2, np.where(s >= thr_med, 1, 0)).astype(int)

    y_cls_train = to_cls(y_snow_train)
    y_cls_test  = to_cls(y_snow_test)

    log.info(f"Training: {X_train.shape[0]} rows  |  Test: {X_test.shape[0]} rows (80/20 Split)")
    log.info(f"Train thresholds (TRAIN-only): med={thr_med:.2f} cm, high={thr_high:.2f} cm")
    log.info(f"Train class distribution: {np.bincount(y_cls_train, minlength=3).tolist()}")
    log.info(f"Test  class distribution: {np.bincount(y_cls_test, minlength=3).tolist()}")

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled  = scaler.transform(X_test)

    results = {}

    # ============================================================
    # MODEL 1: Linear Regression -> tuned thresholds
    # ============================================================
    log.info("\nMODEL 1: Linear Regression -> Tuned Thresholds")

    lin_reg = LinearRegression()
    lin_reg.fit(X_train_scaled, y_reg_train)

    y_log_pred = lin_reg.predict(X_test_scaled)
    y_snowfall_pred = np.clip(np.expm1(y_log_pred), 0.0, None)
    y_snowfall_true = np.expm1(y_reg_test)

    mse  = mean_squared_error(y_snowfall_true, y_snowfall_pred)
    rmse = np.sqrt(mse)
    mae  = mean_absolute_error(y_snowfall_true, y_snowfall_pred)
    r2   = r2_score(y_snowfall_true, y_snowfall_pred)
    log.info(f"  R²={r2:.4f}  RMSE={rmse:.4f}  MAE={mae:.4f}")

    oof_log = cross_val_predict(LinearRegression(), X_train_scaled, y_reg_train,
                                cv=KFold(5, shuffle=True, random_state=SEED), n_jobs=-1)
    oof_log_cm = np.clip(np.expm1(oof_log), 0, None)
    t_med, t_high, t_f1 = tune_thresholds(oof_log_cm, y_cls_train)
    log.info(f"  Tuned thresholds: med={t_med:.2f} cm, high={t_high:.2f} cm "
             f"(OOF macro-F1={t_f1:.4f})")

    lin_wrap = ThresholdWrapper(
        regressor=lin_reg, scaler=scaler,
        thr_med=t_med, thr_high=t_high, use_log=True,
    )

    results["Linear Regression (tuned thr)"] = evaluate_classifier(
        lin_wrap, X_test, y_cls_test,
        "Linear Regression -> Tuned Thresholds",
        label_names=list(label_names),
    )
    results["Linear Regression (tuned thr)"].update({
        "rmse": rmse, "mae": mae, "r2": r2,
    })

    # ============================================================
    # MODEL 2: Logistic Regression (class_weight='balanced')
    # ============================================================
    log.info("\nMODEL 2: Logistic Regression (class_weight='balanced')")

    log_reg = LogisticRegression(
        random_state=SEED, max_iter=5000,
        class_weight="balanced",
    )
    if do_cv and X_train_scaled.shape[0] > 20:
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
        try:
            gs = GridSearchCV(
                log_reg,
                {"C": [0.01, 0.1, 1.0, 10.0, 100.0]},
                cv=cv, scoring="f1_macro", n_jobs=-1,
            )
            gs.fit(X_train_scaled, y_cls_train)
            log_reg = gs.best_estimator_
            log.info(f"  Best C: {gs.best_params_['C']}  (CV macro-F1={gs.best_score_:.4f})")
        except Exception as e:
            log.info(f"  [warn] GridSearch skipped: {e}")
            log_reg.fit(X_train_scaled, y_cls_train)
    else:
        log_reg.fit(X_train_scaled, y_cls_train)

    results["Logistic Regression (balanced)"] = evaluate_classifier(
        log_reg, X_test_scaled, y_cls_test,
        "Logistic Regression (class_weight='balanced')",
        label_names=list(label_names),
    )

    # ============================================================
    # MODEL 3: Random Forest Classifier (class_weight='balanced')
    # ============================================================
    log.info("\nMODEL 3: Random Forest Classifier (class_weight='balanced')")

    rf = RandomForestClassifier(
        random_state=SEED, n_jobs=-1,
        class_weight="balanced",
    )
    if do_cv and X_train_scaled.shape[0] > 20:
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
        param_grid = {
            "n_estimators": [200, 400],
            "max_depth": [None, 15, 25],
            "min_samples_leaf": [1, 3],
            "max_features": ["sqrt", "log2"],
        }
        try:
            gs = GridSearchCV(rf, param_grid, cv=cv,
                              scoring="f1_macro", n_jobs=-1)
            gs.fit(X_train_scaled, y_cls_train)
            rf = gs.best_estimator_
            log.info(f"  Best params: {gs.best_params_}")
            log.info(f"  CV macro-F1 = {gs.best_score_:.4f}")
        except Exception as e:
            log.info(f"  [warn] GridSearch skipped: {e}")
            rf.fit(X_train_scaled, y_cls_train)
    else:
        rf.fit(X_train_scaled, y_cls_train)

    results["Random Forest (balanced)"] = evaluate_classifier(
        rf, X_test_scaled, y_cls_test,
        "Random Forest Classifier (class_weight='balanced')",
        label_names=list(label_names),
    )
    results["Random Forest (balanced)"]["model"] = rf
    results["Random Forest (balanced)"]["features"] = features_to_use

    return results


# -----------------------------
# Pipeline for a single prefecture
# -----------------------------
def run_pipeline(file_path, dataset_name):
    log.info("\n" + "=" * 40)
    log.info(f"# Dataset: {dataset_name}")
    log.info("=" * 40)

    df = pd.read_csv(file_path)
    df["time"] = pd.to_datetime(df["time"])
    df = df.sort_values("time").reset_index(drop=True)

    log.info(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")

    label_names = ("Low", "Medium", "High")

    results = run_experiment(df, FEATURES, label_names, do_cv=True)

    # ---- Feature importance ----
    rf_model = results["Random Forest (balanced)"]["model"]
    fi_df = pd.DataFrame({
        "feature": results["Random Forest (balanced)"]["features"],
        "importance": rf_model.feature_importances_,
    }).sort_values("importance", ascending=False)

    log.info("\n--- Random Forest Feature Importance ---")
    for _, row in fi_df.iterrows():
        log.info(f"  {row['feature']:24s}  {row['importance']:.4f}")

    return {"dataset_name": dataset_name, "results": results}


# -----------------------------
# Summaries
# -----------------------------
def summarize(name, results):
    log.info(f"\n--- {name} ---")
    header = (f"  {'Model':<42} {'MacroF1':>8} {'Acc':>7} "
              f"{'F1w':>7} {'Prec(w)':>8} {'Rec(w)':>8}")
    log.info(header)
    log.info("  " + "-" * (len(header) - 2))
    for model_name, m in results.items():
        log.info(
            f"  {model_name:<42} "
            f"{m['macro_f1']:>8.3f} {m['accuracy']:>7.3f} "
            f"{m['f1_score']:>7.3f} {m['precision']:>8.3f} "
            f"{m['recall']:>8.3f}"
        )


def print_city_summary(city):
    log.info("\n" + "=" * 80)
    log.info(f"Summary — {city['dataset_name'].upper()}")
    log.info("=" * 80)
    summarize("All Models", city["results"])


# -----------------------------
# Main
# -----------------------------
def main():
    cities = {}
    for name, path in DATASETS.items():
        path = Path(path)
        if not path.exists():
            log.info(f"\n[WARN] File not found, skipping: {path}")
            continue
        cities[name] = run_pipeline(path, name)

    if not cities:
        log.info("\nNo datasets processed. Check the paths in DATASETS.")
        return

    for city in cities.values():
        print_city_summary(city)

    log.info("\nDone.")


if __name__ == "__main__":
    main()
