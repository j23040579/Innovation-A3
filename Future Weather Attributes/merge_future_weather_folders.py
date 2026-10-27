#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

KEYS = ["prefecture", "town", "date"]
STATION = ["latitude", "longitude", "elevation"]
IDENTIFIERS = ["location_id", "prefecture", "town", "latitude", "longitude", "elevation", "date", "year", "month", "day"]


FEATURES = [
    "temperature_2m_max", "temperature_2m_min", "wind_speed_10m_max",
    "wind_gusts_10m_max", "snowfall_sum", "rain_sum", "precipitation_hours",
    "precipitation_sum", "shortwave_radiation_sum", "sunshine_duration",
    "daylight_duration", "dew_point_2m_mean", "dew_point_2m_max",
    "surface_pressure_mean", "surface_pressure_max", "surface_pressure_min",
    "temperature_2m_mean", "relative_humidity_2m_mean",
    "relative_humidity_2m_max", "relative_humidity_2m_min",
    "dew_point_2m_min", "cloud_cover_mean", "cloud_cover_max", "cloud_cover_min",
    "pressure_msl_mean", "pressure_msl_max", "pressure_msl_min",
    "wind_speed_10m_mean", "wind_speed_10m_min", "wind_gusts_10m_mean",
    "wind_gusts_10m_min", "river_discharge", "river_discharge_p75",
    "river_discharge_mean", "river_discharge_median", "river_discharge_max",
    "wind_direction_10m_dominant",
]

SOURCE_FEATURES = {
    "Weather": FEATURES[0:8],
    "Daily_solar_dewpoint": FEATURES[8:13],
    "Daily_surface_pressure_wind_direction": FEATURES[13:16] + ["wind_direction_10m_dominant"],
    "Missing_group_1": FEATURES[16:24],
    "Missing_group_2": FEATURES[24:31],
    "Flood": FEATURES[31:36],
    "Daily_cloud_humid_pressure": [
        "relative_humidity_2m_mean", "relative_humidity_2m_max", "relative_humidity_2m_min",
        "cloud_cover_mean", "cloud_cover_max", "cloud_cover_min",
        "pressure_msl_mean", "pressure_msl_max", "pressure_msl_min",
    ],
}
# Accept a previously-combined missing-weather CSV in addition to split group files.
SOURCE_FEATURES["Missing_combined"] = SOURCE_FEATURES["Missing_group_1"] + SOURCE_FEATURES["Missing_group_2"]

REPORT = []


def log(message: str) -> None:
    print(message, flush=True)
    REPORT.append(message)


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def get_folder(root: Path, name: str, required: bool) -> Path | None:

    wanted = slug(name)
    candidates = [p for p in [root, *root.rglob("*")] if p.is_dir() and slug(p.name) == wanted]
    candidates.sort(key=lambda p: (len(p.relative_to(root).parts), str(p)))
    if not candidates:
        if required:
            raise FileNotFoundError(f"Required extracted folder '{name}' not found beneath {root}")
        return None
    if len(candidates) > 1:
        log(f"WARNING: More than one {name} folder found; using {candidates[0]}")
    return candidates[0]


def file_list(folder: Path) -> list[Path]:
    # Only CSVs are considered; archives are not opened, tested or searched.
    return sorted(p for p in folder.rglob("*.csv") if p.is_file()
                  and not any(part.startswith(".") for part in p.relative_to(folder).parts)
                  and not any(x in p.stem.lower() for x in ("_progress", "_failed", "failed_", "progress_")))


def csv_encoding(path: Path) -> str:
    with path.open("rb") as fh:
        bom = fh.read(4)
    if bom.startswith((b"\xff\xfe", b"\xfe\xff")):
        return "utf-16"
    return "utf-8-sig"


def rename_column(value: object) -> str:
    name = re.sub(r"\s*\([^)]*\)\s*$", "", str(value).strip())
    return {"time": "date", "city/town": "town", "Prefecture/Region": "prefecture", "Town": "town"}.get(name, name)


def station_text(value: object) -> str | pd.NA:
    if pd.isna(value):
        return pd.NA
    value = unicodedata.normalize("NFKC", str(value)).strip()
    value = re.sub(r"\s+", " ", value)
    return value if value else pd.NA


def normalize(df: pd.DataFrame, label: str, first_date: pd.Timestamp, last_date: pd.Timestamp) -> pd.DataFrame:
    df = df.rename(columns={col: rename_column(col) for col in df.columns})
    for key in KEYS:
        if key not in df:
            raise ValueError(f"{label} is missing required column '{key}'")
    for key in ["prefecture", "town"]:
        df[key] = df[key].map(station_text)
    # Normalize a few alternative romanizations encountered in Japan datasets.
    df["prefecture"] = df["prefecture"].replace({"Kōchi": "Kochi", "Kôchi": "Kochi", "Hyōgo": "Hyogo"})
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.normalize()
    invalid = df[KEYS].isna().any(axis=1)
    if invalid.any():
        log(f"WARNING: {label} has {int(invalid.sum()):,} records with invalid station/date keys; excluded")
        df = df.loc[~invalid].copy()
    return df.loc[df.date.between(first_date, last_date)].copy()


def read_two_section_csv(path: Path, dataset_name: str) -> pd.DataFrame:
    """Read Open-Meteo CSV with station metadata followed by daily measurements."""
    enc = csv_encoding(path)
    with path.open("r", encoding=enc, newline="") as fh:
        rows = csv.reader(fh)
        first = next(rows, None)
        if not first:
            raise ValueError(f"Empty file: {path}")
        meta_header = [rename_column(x) for x in first]
        meta_rows = []
        header_line = None
        for line, row in enumerate(rows, start=1):
            if len(row) >= 2 and row[0].strip() == "location_id" and row[1].strip() == "time":
                header_line = line
                break
            if any(x.strip() for x in row):
                meta_rows.append(row)
    if header_line is None:
        raise ValueError(f"No location_id,time daily header found: {path}")
    meta = pd.DataFrame(meta_rows, columns=meta_header)
    meta = meta.rename(columns={c: rename_column(c) for c in meta.columns})
    daily = pd.read_csv(path, encoding=enc, skiprows=header_line, low_memory=False)
    daily = daily.rename(columns={c: rename_column(c) for c in daily.columns})
    if "location_id" not in meta or "location_id" not in daily:
        raise ValueError(f"No station identifier found in {path}")
    
    meta["location_id"] = meta["location_id"].astype(str).str.strip()
    daily["location_id"] = daily["location_id"].astype(str).str.strip()
    keep = [x for x in ("location_id", "town", *STATION) if x in meta.columns]
    if meta["location_id"].duplicated().any():
        raise ValueError(f"Duplicate station metadata IDs in {path}")
    daily = daily.merge(meta[keep], on="location_id", how="left", validate="many_to_one")
    suffix = {"Daily_solar_dewpoint": "_solar_dewpoint", "Daily_surface_pressure_wind_direction": "_pressure_wind"}.get(dataset_name, "")
    prefecture = path.stem
    if suffix and prefecture.endswith(suffix):
        prefecture = prefecture[:-len(suffix)]
    daily.insert(0, "prefecture", prefecture)
    return daily


def dedupe(df: pd.DataFrame, label: str, cols: list[str]) -> pd.DataFrame:
    repeated = df.duplicated(KEYS, keep=False)
    if not repeated.any():
        return df
    num_rows = int(repeated.sum())
    
    relevant = [c for c in cols if c in df]
    if relevant:
        uniqueness = df.loc[repeated].groupby(KEYS, sort=False)[relevant].nunique(dropna=True)
        conflict = int(uniqueness.gt(1).any(axis=1).sum())
    else:
        conflict = 0
    log(f"WARNING: {label}: {num_rows:,} duplicate rows, {conflict:,} conflicting keys; keeping most complete per key")
    df = df.assign(__complete=df[[c for c in cols if c in df]].notna().sum(axis=1))
    return df.sort_values("__complete", ascending=False, kind="stable").drop_duplicates(KEYS).drop(columns="__complete")


def load_sections(folder: Path, source: str, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    paths = file_list(folder)
    if not paths:
        raise FileNotFoundError(f"No CSV files in {folder}")
    frames = []
    for i, path in enumerate(paths, 1):
        if i == 1 or i % 10 == 0 or i == len(paths):
            log(f"  {source}: loading {i}/{len(paths)} CSV files")
        df = normalize(read_two_section_csv(path, source), path.name, start, end)
        cols = [c for c in SOURCE_FEATURES[source] if c in df]
        if source == "Weather":
            cols = list(dict.fromkeys(["location_id", *STATION, *cols]))
            cols = [c for c in cols if c in df]
        frames.append(df[KEYS + cols].copy())
    result = pd.concat(frames, ignore_index=True)
    result = dedupe(result, source, SOURCE_FEATURES[source])
    log(f"  {source}: {len(result):,} unique daily rows")
    return result


def load_flat(path: Path, name: str, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    df = pd.read_csv(path, encoding=csv_encoding(path), low_memory=False)
    df = normalize(df, path.name, start, end)
    cols = [c for c in SOURCE_FEATURES[name] if c in df.columns]
    if not cols:
        raise ValueError(f"No recognized {name} fields in {path}")
    df = df[KEYS + cols].copy()
    return dedupe(df, name, cols)


def combine_missing(folder: Path | None, cloud_folder: Path | None, start: pd.Timestamp,
                    end: pd.Timestamp) -> list[tuple[str, pd.DataFrame]]:
    sources = []
    if folder is not None:
        paths = file_list(folder)
        for category, match in [
            ("Missing_group_1", lambda s: s.startswith("group_1_") and "2021_2026" in s),
            ("Missing_group_2", lambda s: s.startswith("group_2_") and "2021_2026" in s),
            ("Missing_combined", lambda s: s.startswith("japan_missing_weather") or s.startswith("japan_daily_weather_missing")),
        ]:
            chosen = [p for p in paths if match(p.stem.lower())]
            if chosen:
                frames = [load_flat(p, category, start, end) for p in chosen]
                data = dedupe(pd.concat(frames, ignore_index=True), category, SOURCE_FEATURES[category])
                log(f"  {category}: {len(data):,} rows from {len(chosen)} CSV(s)")
                sources.append((category, data))
        if not sources:
            log(f"WARNING: Missing_weather_dataset found, but no group_1/group_2 or japan_missing_weather CSV was recognized")
    if cloud_folder is not None:
        flat_files = file_list(cloud_folder)
        if flat_files:
            frames = [load_flat(p, "Daily_cloud_humid_pressure", start, end) for p in flat_files]
            data = dedupe(pd.concat(frames, ignore_index=True), "Daily_cloud_humid_pressure", SOURCE_FEATURES["Daily_cloud_humid_pressure"])
            log(f"  Daily_cloud_humid_pressure: {len(data):,} rows from {len(flat_files)} CSV(s) (fallback only)")
            sources.append(("Daily_cloud_humid_pressure", data))
    return sources


def merge_source(base: pd.DataFrame, incoming: pd.DataFrame, name: str) -> pd.DataFrame:
    
    attr = [c for c in incoming if c not in KEYS]
    missing = [c for c in attr if c not in base]
    overlapping = [c for c in attr if c in base]
    prior = len(base)
    joined = base.merge(incoming, how="left", on=KEYS, suffixes=("", "__incoming"),
                        validate="one_to_one", indicator="__matched")
    matched = int((joined["__matched"] == "both").sum())
    joined.drop(columns=["__matched"], inplace=True)
    filled = 0
    for col in overlapping:
        temporary = f"{col}__incoming"
        if temporary not in joined:
            continue
        filled += int((joined[col].isna() & joined[temporary].notna()).sum())
        joined[col] = joined[col].combine_first(joined[temporary])
        joined.drop(columns=temporary, inplace=True)
    if len(joined) != prior:
        raise RuntimeError(f"{name} merge multiplied rows")
    log(f"Merged {name}: {matched:,}/{prior:,} base rows matched; {len(missing)} new attributes; {filled:,} fallback values")
    return joined


def make_continuous(df: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    """Create exactly one daily record for every base station, including missing dates."""
    stations = df.sort_values("date")[KEYS[:2] + [c for c in ("location_id", *STATION) if c in df]]
    station_meta = stations.groupby(KEYS[:2], dropna=False, as_index=False).first()
    for col in STATION:
        if col not in station_meta:
            raise ValueError(f"Base Weather is missing required location metadata: {col}")
    for col in STATION:
        # Track station coordinate drift; the LSTM requires constant metadata.
        drift = int((df.groupby(KEYS[:2])[col].nunique(dropna=True) > 1).sum())
        if drift:
            log(f"WARNING: {drift} stations have changing '{col}'; using first value for all historical days")
    calendar = pd.date_range(start, end, freq="D")
    pairs = pd.MultiIndex.from_frame(station_meta[KEYS[:2]])
    full = pd.MultiIndex.from_product([range(len(pairs)), calendar], names=["_station_id", "date"])
    location = station_meta[KEYS[:2]].reset_index(drop=True).copy()
    location["_station_id"] = location.index
    scaffold = full.to_frame(index=False).merge(location, on="_station_id").drop(columns="_station_id")
    missing_days = len(scaffold) - len(df)
    log(f"Continuous calendar: {len(pairs):,} stations × {len(calendar):,} days = {len(scaffold):,} records; {missing_days:,} absent base dates inserted")
    weather = df.drop(columns=[c for c in ("location_id", *STATION) if c in df])
    result = scaffold.merge(weather, on=KEYS, how="left", validate="one_to_one")
    return result.merge(station_meta, on=KEYS[:2], how="left", validate="many_to_one")


def impute_for_lstm(data: pd.DataFrame, train_end: pd.Timestamp, ffill_days: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Only historical training observations may supply median fallback values."""
    df = data.sort_values(KEYS).reset_index(drop=True).copy()
    for col in FEATURES + STATION:
        df[col] = pd.to_numeric(df[col], errors="coerce").replace([np.inf, -np.inf], np.nan)
    if df[STATION].isna().any().any():
        raise ValueError("Some base stations have missing coordinates/elevation; cannot generate model-ready input")
    
    missing_before = df[FEATURES].isna().sum()
    
    df[FEATURES] = df.groupby(KEYS[:2], sort=False)[FEATURES].ffill(
        limit=ffill_days
        )
    
    filled_forward = missing_before - df[FEATURES].isna().sum()

    training = data.date <= train_end

    historical = data.loc[
        training, KEYS[:2] + FEATURES
    ].copy()
    for col in FEATURES:
        historical[col] = pd.to_numeric(historical[col], errors="coerce").replace([np.inf, -np.inf], np.nan)
    if historical.empty:
        raise ValueError("No observations in training period, cannot compute imputation medians")
    
    station_medians = historical.groupby(KEYS[:2])[FEATURES].median()


    global_medians = historical[FEATURES].median()

    completely_absent = global_medians[global_medians.isna()].index.tolist()
    if completely_absent:
        raise ValueError(f"Required model features are empty in historical training period: {completely_absent}")
    station_index = pd.MultiIndex.from_frame(df[KEYS[:2]])
    remaining_after_forward = df[FEATURES].isna().sum()
    for col in FEATURES:
        
        mapped = pd.Series(station_medians[col].reindex(station_index).to_numpy(), index=df.index)
        df[col] = df[col].fillna(mapped).fillna(global_medians[col])

    missing_after = df[FEATURES].isna().sum()
    if missing_after.any():
        raise ValueError(f"Nonfinite data after preparation: {missing_after[missing_after.gt(0)].to_dict()}")
    summary = pd.DataFrame({
        "attribute": FEATURES, "missing_in_raw": missing_before.reindex(FEATURES).to_numpy(),
        "forward_filled": filled_forward.reindex(FEATURES).to_numpy(),
        "median_filled": (remaining_after_forward - missing_after).reindex(FEATURES).to_numpy(),
        "missing_after": missing_after.reindex(FEATURES).to_numpy(),
    })
    # Hard invariants from the forecast notebook.
    if df.duplicated(KEYS).any():
        raise ValueError("Duplicate station-day rows remain")
    for (pref, town), group in df.groupby(KEYS[:2], sort=False):
        if not group.date.diff().dropna().eq(pd.Timedelta(days=1)).all():
            raise ValueError(f"Nonconsecutive days for {pref}/{town}")
    if not np.isfinite(df[FEATURES + STATION].to_numpy(dtype=np.float64)).all():
        raise ValueError("Notebook numeric contract not satisfied")
    df["year"] = df.date.dt.year
    df["month"] = df.date.dt.month
    df["day"] = df.date.dt.day
    col_order = [x for x in IDENTIFIERS if x in df] + FEATURES
    return df[col_order], summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Merge Japan historical daily CSVs from Data/Open-Meteo, preparing the LSTM dataset for Future Weather Attributes.")
    project_dir = Path(__file__).resolve().parent
    default_source_root = project_dir.parent / "Data" / "Open-Meteo"
    parser.add_argument("--root", type=Path, default=default_source_root,
                        help="Extracted historical CSV source root (default: ../Data/Open-Meteo)")
    parser.add_argument("--notebook-root", type=Path, default=None,
                        help="Future Weather Attributes project folder (default: directory containing this script)")
    parser.add_argument("--start-date", default="2021-01-01")
    parser.add_argument("--end-date", default="2026-01-31", help="Last observed historical day, inclusive")
    parser.add_argument("--train-end", default="2025-09-30", help="Only dates through this can supply fallback median values")
    parser.add_argument("--ffill-days", type=int, default=7, help="Maximum forward-fill gap before using training medians")
    parser.add_argument("--raw-only", action="store_true", help="Do not impute or write LSTM-ready dataset")
    return parser.parse_args()


def main() -> None:
    a = parse_args()
    if a.ffill_days < 1:
        raise ValueError("--ffill-days must be >= 1")
    root = a.root.resolve()
    if not root.is_dir():
        raise FileNotFoundError(
            f"Historical CSV source directory not found: {root}\n"
            "Extract the source folders under Data/Open-Meteo, or pass --root PATH."
        )
    start, end, train_end = map(pd.Timestamp, [a.start_date, a.end_date, a.train_end])
    if end < start:
        raise ValueError("--end-date must not precede --start-date")
    output = root / "Combined_daily_dataset"
    output.mkdir(exist_ok=True)
    log(f"Scanning extracted CSV folders under: {root}")
    log("Archives are never used; only .csv files inside extracted folders are read.")
    log(f"Historical period: {start.date()} to {end.date()}")

    folder_names = ["Weather", "Daily_solar_dewpoint", "Daily_surface_pressure_wind_direction", "Flood"]
    folders = {name: get_folder(root, name, True) for name in folder_names}
    missing_folder = get_folder(root, "Missing_weather_dataset", False)
    cloud_folder = get_folder(root, "Daily_cloud_humid_pressure", False)
    base = load_sections(folders["Weather"], "Weather", start, end)
    for source in ["Daily_solar_dewpoint", "Daily_surface_pressure_wind_direction"]:
        base = merge_source(base, load_sections(folders[source], source, start, end), source)

    for source, data in combine_missing(missing_folder, cloud_folder, start, end):
        base = merge_source(base, data, source)
        
    base = merge_source(base, load_sections(folders["Flood"], "Flood", start, end), "Flood")
    absent = [name for name in FEATURES if name not in base.columns]

    if absent:
        raise ValueError(f"Cannot build the LSTM's 37-attribute schema. Missing columns: {absent}. Check extracted Group 1/2 CSVs.")
    
    base = make_continuous(base, start, end)
    town_count = base[KEYS[:2]].drop_duplicates().shape[0]
    log(f"Distinct prefecture/town stations in Weather base: {town_count:,}")
    if town_count != 255:
        log(f"WARNING: Expected around 255 known station pairs, but found {town_count:,}; check inputs")
    base = base.sort_values(KEYS).reset_index(drop=True)
    for col in FEATURES:
        base[col] = pd.to_numeric(base[col], errors="coerce").replace([np.inf, -np.inf], np.nan)
    base["year"], base["month"], base["day"] = base.date.dt.year, base.date.dt.month, base.date.dt.day
    base = base[[c for c in IDENTIFIERS if c in base] + FEATURES]
    raw_file = output / "japan_complete_daily_2021_2026.csv"
    base.to_csv(raw_file, index=False, encoding="utf-8-sig", date_format="%Y-%m-%d")
    log(f"Saved RAW merged dataset: {raw_file} ({len(base):,} rows, {len(base.columns)} columns)")
    raw_miss = base[FEATURES].isna().sum().sort_values(ascending=False)
    log(f"Missing RAW attribute values: {int(raw_miss.sum()):,}")
    log("Raw missing counts per attribute: " + ", ".join(f"{key}={value}" for key, value in raw_miss.items()))

    if not a.raw_only:
        notebook_root = a.notebook_root.resolve() if a.notebook_root else Path(__file__).resolve().parent
        target_dir = notebook_root / "dataset" / "LSTM_processed"
        target_dir.mkdir(parents=True, exist_ok=True)
        cleaned, summary = impute_for_lstm(base, train_end, a.ffill_days)
        path = target_dir / "japan_daily_lstm_processed.csv"
        cleaned.to_csv(path, index=False, encoding="utf-8-sig", date_format="%Y-%m-%d")
        summary.to_csv(output / "imputation_summary.csv", index=False, encoding="utf-8-sig")
        log(f"Saved LSTM-ready input: {path}")
        log(f"LSTM-ready validation: {len(cleaned):,} rows, {len(FEATURES)} weather features, no missing values, consecutive days")
        imputed = int(summary[["forward_filled", "median_filled"]].sum().sum())
        total = len(cleaned) * len(FEATURES)
        log(f"Imputed {imputed:,}/{total:,} feature cells ({100 * imputed/total:.3f}%). See imputation_summary.csv")
        if imputed / total > 0.05:
            log("WARNING: More than 5% of feature observations were filled; inspect missing data before training.")
    else:
        log("--raw-only: LSTM-ready imputation/output skipped")
    report = output / "merge_report.txt"
    report.write_text("\n".join(REPORT) + "\n", encoding="utf-8")
    log(f"Saved report: {report}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError, pd.errors.ParserError) as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        sys.exit(1)
