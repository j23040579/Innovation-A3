import os
import numpy as np
import pandas as pd

# Read File
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
RAW_DIR       = os.path.join(PROJECT_ROOT, "dataset", "raw")
PROCESSED_DIR = os.path.join(PROJECT_ROOT, "dataset", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

REGIONS = ["Yamagata", "Niigata"]

COLS = [
    "location_id", "time",
    "temperature_2m_max", "temperature_2m_min",
    "snowfall_sum",
    "relative_humidity_2m_max", "relative_humidity_2m_min",
    "wind_speed_10m_max", "wind_speed_10m_min",
]

# Rename columns
RENAME = {
    "temperature_2m_max": "max_temperature",
    "temperature_2m_min": "min_temperature",
    "relative_humidity_2m_max": "max_humidity",
    "relative_humidity_2m_min": "min_humidity",
    "wind_speed_10m_max": "max_wind_speed",
    "wind_speed_10m_min": "min_wind_speed",
}

METRICS = [
    "max_temperature", "min_temperature", "snowfall_sum",
    "max_humidity", "min_humidity",
    "max_wind_speed", "min_wind_speed",
]

# Keep November - April
WINTER_MONTHS = [11, 12, 1, 2, 3, 4]


def process_region(name):
    print(f"\n{'='*60}\nProcessing: {name}\n{'='*60}")

    in_path  = os.path.join(RAW_DIR, f"{name}.csv")
    out_path = os.path.join(PROCESSED_DIR, f"{name}_winter_avg.csv")

    df = pd.read_csv(in_path, skiprows=7, header=None, names=COLS)
    print("Raw shape:", df.shape)

    df = df.rename(columns=RENAME)
    df["time"] = pd.to_datetime(df["time"])
    df["location_id"] = df["location_id"].astype(int)

    # Drop Jan–Apr 2019
    df_winter = df[df["time"].dt.month.isin(WINTER_MONTHS)].copy()
    print("After winter filter:", df_winter.shape)

    df_winter = df_winter[
        ~((df_winter["time"].dt.year == 2019) & (df_winter["time"].dt.month <= 10))
    ].copy()
    print("After dropping 2019 Jan–Oct:", df_winter.shape)

    df_winter = df_winter[df_winter["location_id"].isin([0, 1, 2, 3])]
    df_avg = (
        df_winter.groupby("time", as_index=False)[METRICS]
        .mean().round(2)
    )
    print("Averaged shape:", df_avg.shape)


    # Log-transform the two skewed columns 
    df_avg["snowfall_sum_log"]   = np.log1p(df_avg["snowfall_sum"])
    df_avg["min_wind_speed_log"] = np.log1p(df_avg["min_wind_speed"])

    # Save
    df_avg.to_csv(out_path, index=False)
    print(f"Saved → {out_path}")


if __name__ == "__main__":
    for region in REGIONS:
        process_region(region)