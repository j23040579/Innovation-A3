
import argparse
import json
import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


SCRIPT_DIR = Path(__file__).resolve().parent
MODEL_KEYS = ("model", "pipeline", "estimator", "classifier")
FEATURE_KEYS = ("feature_names", "feature_columns", "selected_features", "features")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Evaluate saved models using the exact features used for training."
    )
    parser.add_argument("--data", type=Path, default=SCRIPT_DIR / "trained_models" / "testing.csv",
                        help="Test CSV (default: trained_models/testing.csv).")
    parser.add_argument("--models-dir", type=Path, default=SCRIPT_DIR / "trained_models",
                        help="Folder containing .joblib files (default: trained_models folder).")
    parser.add_argument("--model", action="append", default=[],
                        help="Specific .joblib filename; repeat for multiple models. Default: all.")
    parser.add_argument("--target", default="rain_class",
                        help="True-label column for evaluation (default: rain_class).")
    parser.add_argument("--feature-map", type=Path,
                        help="Optional JSON mapping filenames to ordered input column lists. "
                             "Used only if a saved model has no feature names.")
    parser.add_argument("--save-predictions", type=Path,
                        help="Optional output CSV with one prediction column per model.")
    return parser.parse_args()


def load_feature_map(path):
    if path is None:
        return {}
    mapping = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(mapping, dict):
        raise ValueError("Feature map must be a JSON object of model names to feature lists.")
    return mapping


def unwrap_model(saved):
    """Support either a direct estimator/pipeline or a dictionary bundle."""
    if hasattr(saved, "predict"):
        return saved, None
    if isinstance(saved, dict):
        for key in MODEL_KEYS:
            candidate = saved.get(key)
            if hasattr(candidate, "predict"):
                return candidate, saved
    raise TypeError("Saved file is not a predict-capable model or known model bundle.")


def checked_feature_list(value, source):
    if value is None:
        return None
    if not isinstance(value, (list, tuple, pd.Index)) and not hasattr(value, "tolist"):
        raise ValueError(f"{source}: features must be an ordered list of column names.")
    names = list(value)
    if not names or any(not isinstance(name, str) or not name for name in names):
        raise ValueError(f"{source}: expected a nonempty list of string feature names.")
    if len(names) != len(set(names)):
        raise ValueError(f"{source}: duplicate feature names are not allowed.")
    return names


def get_expected_features(model, bundle, model_path, feature_map):
    # The estimator's feature_names_in_ is authoritative: it records the
    # *actual feature names and order* used when fit with a DataFrame.
    names = checked_feature_list(getattr(model, "feature_names_in_", None),
                                 f"{model_path.name} feature_names_in_")

    if names is None and bundle is not None:
        for key in FEATURE_KEYS:
            if key in bundle:
                names = checked_feature_list(bundle[key], f"{model_path.name} bundle[{key}]")
                break

    if names is None:
        manual_names = feature_map.get(model_path.name, feature_map.get(model_path.stem))
        names = checked_feature_list(manual_names, f"{model_path.name} feature map")

    if names is None:
        raise ValueError(
            "The saved model has no feature-name metadata. A feature count alone "
            "cannot identify which columns were used or their order. Provide "
            "--feature-map with the exact training features for this model."
        )

    expected_count = getattr(model, "n_features_in_", None)
    if expected_count is not None and len(names) != int(expected_count):
        raise ValueError(
            f"Metadata lists {len(names)} features, but model expects "
            f"{expected_count}. Check the saved training configuration."
        )
    return names


def resolve_model_paths(folder, filenames):
    if filenames:
        paths = [folder / name for name in filenames]
        missing = [str(path) for path in paths if not path.is_file()]
        if missing:
            raise FileNotFoundError("Missing model file(s): " + ", ".join(missing))
        return paths
    paths = sorted(folder.glob("*.joblib"))
    if not paths:
        raise FileNotFoundError(f"No .joblib models found in {folder}")
    return paths


def main():
    args = parse_args()
    if not args.data.is_file():
        raise FileNotFoundError(f"Test CSV not found: {args.data}")

    data = pd.read_csv(args.data)
    if data.empty:
        raise ValueError(f"Test CSV has no rows: {args.data}")
    if not data.columns.is_unique:
        raise ValueError("Test CSV has duplicate column names.")

    feature_map = load_feature_map(args.feature_map)
    model_paths = resolve_model_paths(args.models_dir, args.model)
    predictions = data.copy() if args.save_predictions else None
    failed = 0

    print(f"Loaded {len(data):,} test rows from {args.data}")
    print(f"Found {len(model_paths)} model(s). Target column: {args.target}")

    for model_path in model_paths:
        print(f"\n{'=' * 70}\nMODEL: {model_path.name}\n{'=' * 70}")
        try:
            saved = joblib.load(model_path)
            model, bundle = unwrap_model(saved)
            features = get_expected_features(model, bundle, model_path, feature_map)
            missing = [name for name in features if name not in data.columns]
            if missing:
                raise ValueError(
                    f"Missing required test columns: {missing}. "
                    "The model cannot safely predict until these are supplied."
                )

            # Do not pass the entire CSV: a model may have been trained with
            # fewer features, and sklearn requires its exact trained order.
            X_test = data.loc[:, features]
            print(f"Using {len(features)} training features (in saved order):")
            for index, feature in enumerate(features, start=1):
                print(f"  {index:2}. {feature}")

            y_pred = model.predict(X_test)
            print(f"Predicted {len(y_pred):,} rows successfully.")

            if predictions is not None:
                predictions[f"predicted_{model_path.stem}"] = y_pred

            if args.target in data.columns:
                actual = data[args.target]
                print(f"Accuracy: {accuracy_score(actual, y_pred):.4f}")
                print("\nClassification report:")
                print(classification_report(actual, y_pred, zero_division=0))
                labels = sorted(set(actual.dropna()) | set(y_pred), key=str)
                matrix = pd.DataFrame(confusion_matrix(actual, y_pred, labels=labels),
                                      index=pd.Index(labels, name="Actual"),
                                      columns=pd.Index(labels, name="Predicted"))
                print("Confusion matrix (rows=actual, columns=predicted):")
                print(matrix.to_string())
            else:
                print(f"No '{args.target}' column found; predictions generated without scores.")

        except (OSError, TypeError, ValueError, KeyError) as exc:
            failed += 1
            print(f"ERROR: {exc}", file=sys.stderr)

    if args.save_predictions is not None:
        if predictions is not None and any(c.startswith("predicted_") for c in predictions):
            args.save_predictions.parent.mkdir(parents=True, exist_ok=True)
            predictions.to_csv(args.save_predictions, index=False)
            print(f"\nPredictions saved to: {args.save_predictions}")
        else:
            print("\nNo predictions saved because all model tests failed.", file=sys.stderr)

    if failed:
        print(f"\n{failed} of {len(model_paths)} model(s) could not be tested.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
