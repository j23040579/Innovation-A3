# Heavy Snow — Project Guide

This project processes daily weather observations for Niigata and Yamagata, creates exploratory plots, and evaluates three snowfall-risk models (Low, Medium, High).

## Existing folder structure

No files need to be moved. Paths in the Python scripts are resolved relative to their own location, so they do not depend on the terminal's current working directory.

| Location | Contents |
| --- | --- |
| `dataset/raw/Niigata.csv`, `dataset/raw/Yamagata.csv` | Original daily weather observations |
| `dataset/processed/` | Processed `Niigata_winter_avg.csv` and `Yamagata_winter_avg.csv` |
| `data_process.py` | Preprocess the raw CSVs into `dataset/processed/` |
| `data_analysis_niigata.py`, `data_analysis_yamagata.py` | Read processed CSVs and write images to `plots/` |
| `plots/` | Existing boxplot and log-transformation PNGs |
| `src/model_train.py` | Read both processed CSVs and evaluate the three models |
| `trained_models/niigata/`, `trained_models/yamagata/` | Existing saved models (`.joblib`), training/testing CSVs and result summaries |
| `experiment_logs/<prefecture>/baseline_v1/` | Existing experiment configurations and model-comparison CSVs |

## Run from a terminal

Open PowerShell or another terminal **inside the `Heavy Snow` folder**, where `data_process.py` and this README are located.

### 1. Install dependencies (first time only)

```powershell
python -m pip install numpy pandas matplotlib seaborn scikit-learn joblib
```

### 2. Preprocess the raw datasets (optional)

The two processed CSV files are already included. Re-running this step recreates them at their current paths.

```powershell
python -B data_process.py
```

Inputs: `dataset/raw/Niigata.csv` and `dataset/raw/Yamagata.csv`.

Outputs: `dataset/processed/Niigata_winter_avg.csv` and `dataset/processed/Yamagata_winter_avg.csv`.

### 3. Regenerate the data-analysis plots (optional)

```powershell
python -B data_analysis_niigata.py
python -B data_analysis_yamagata.py
```

These scripts read from `dataset/processed/` and write four PNGs into `plots/`.

### 4. Train and evaluate the models

```powershell
python -B src/model_train.py
```

This runs Linear Regression with tuned classification thresholds, balanced Logistic Regression, and balanced Random Forest for **both** Niigata and Yamagata. Metrics, confusion matrices, and feature importance are printed in the terminal. The script performs cross-validation and hyperparameter search where defined; it can take some time.

User is also able to change the test split to get other results.

**Important:** The included `src/model_train.py` currently **does not save newly trained models, training/testing CSVs, or experiment logs**. The artifacts already present under `trained_models/` and `experiment_logs/` were produced by an earlier training pipeline and will not be updated by running this script. The current script also uses six features and a random 80/20 split, while the saved experiment configurations describe an earlier four-feature, winter-year-based experiment. Do not assume its terminal metrics reproduce those saved results.

The command `python -B model_training.py` is **not valid for this ZIP**, because no `model_training.py` exists. There is also no `--no-cv` command-line option in `src/model_train.py`.

## File path notes

- `data_process.py` reads `dataset/raw/` and writes `dataset/processed/`.
- Both `data_analysis_*.py` scripts read `dataset/processed/` and write `plots/`.
- `src/model_train.py` resolves the project root from its location in `src/` and reads **`dataset/processed/`**, not `data/processed/`.
- The `dataset` fields in the existing `experiment_config.json` files use forward-slash relative paths, which work on Windows and other operating systems when resolved from the project root.
- The `-B` option prevents Python from generating bytecode cache files. Only load `.joblib` files from trusted sources.
