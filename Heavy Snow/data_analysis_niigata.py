import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("white")

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DIR = os.path.join(PROJECT_ROOT, "dataset", "processed")
OUTDIR        = os.path.join(PROJECT_ROOT, "plots")
os.makedirs(OUTDIR, exist_ok=True)

# ===============================================================
# 1. LOAD THE PROCESSED WINTER DATA
# ===============================================================
df_avg = pd.read_csv(
    os.path.join(PROCESSED_DIR, "Niigata_winter_avg.csv"),
    parse_dates=["time"]
)

# Original metrics (kept for reference)
metrics = [
    "max_temperature", "min_temperature", "snowfall_sum",
    "max_humidity", "min_humidity",
    "max_wind_speed", "min_wind_speed",
]

# ===============================================================
# 2. BOX PLOTS — distribution overview (Tukey fences shown)
# ===============================================================
fig, axes = plt.subplots(2, 4, figsize=(18, 8))
axes = axes.flatten()
for i, col in enumerate(metrics):
    sns.boxplot(y=df_avg[col], ax=axes[i], color="skyblue")
    axes[i].set_title(col, fontsize=10)
    axes[i].set_ylabel("")
axes[-1].axis("off")
plt.suptitle("Niigata — Box Plots: Distribution Overview", fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "niigata_boxplots.png"), dpi=150)
plt.close()

# ===============================================================
# 3. IQR EXTREME-VALUE COUNT — before vs after log transform
# ===============================================================
def iqr_outliers(s):
    q1, q3 = s.quantile([0.25, 0.75])
    iqr = q3 - q1
    return s[(s < q1 - 1.5 * iqr) | (s > q3 + 1.5 * iqr)]

print("\n--- Niigata IQR Extreme-Value Summary (Tukey 1.5xIQR) ---")
for col in metrics:
    extreme = iqr_outliers(df_avg[col])
    print(f"{col:22s}  {len(extreme):4d}  ({len(extreme)/len(df_avg)*100:.2f}%)")

print("\n--- Log Transform Comparison (IQR extreme-value counts) ---")
for raw, log in [("snowfall_sum", "snowfall_sum_log"),
                 ("min_wind_speed", "min_wind_speed_log")]:
    ext_raw = iqr_outliers(df_avg[raw])
    ext_log = iqr_outliers(df_avg[log])
    print(f"{raw:22s}  raw: {len(ext_raw):4d} ({len(ext_raw)/len(df_avg)*100:.2f}%)"
          f"   log: {len(ext_log):4d} ({len(ext_log)/len(df_avg)*100:.2f}%)")

# ===============================================================
# 4. Before vs After Log Transform — histogram comparison
# ===============================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 8))

sns.histplot(df_avg["snowfall_sum"], kde=True, ax=axes[0, 0], color="blue")
axes[0, 0].set_title("Niigata Snowfall — raw (skewed)")

sns.histplot(df_avg["snowfall_sum_log"], kde=True, ax=axes[0, 1], color="darkblue")
axes[0, 1].set_title("Niigata Snowfall — log1p (more symmetric)")

sns.histplot(df_avg["min_wind_speed"], kde=True, ax=axes[1, 0], color="green")
axes[1, 0].set_title("Niigata Min Wind — raw (skewed)")

sns.histplot(df_avg["min_wind_speed_log"], kde=True, ax=axes[1, 1], color="darkgreen")
axes[1, 1].set_title("Niigata Min Wind — log1p (more symmetric)")

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "niigata_log_transform_check.png"), dpi=150)
plt.close()

print("\nAll images saved successfully!")