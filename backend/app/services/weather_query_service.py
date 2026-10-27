import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import pandas as pd
import numpy as np

from app.core.config import settings

logger = logging.getLogger(__name__)

class WeatherQueryService:
    """
    Backend 1 Core Query Engine.
    Loads and indexes the pre-generated future dataset into memory on startup.
    Provides sub-millisecond lookups for single days, time-series intervals, and map overviews.
    """

    def __init__(self, dataset_path: Optional[Path] = None):
        self.dataset_path = dataset_path or settings.WEATHER_DATASET_PATH
        self.df: Optional[pd.DataFrame] = None
        self._indexed_df: Optional[pd.DataFrame] = None
        self._prefectures_map: Dict[str, List[str]] = {}
        self._min_date: str = ""
        self._max_date: str = ""
        self._is_loaded: bool = False

    def load_dataset(self) -> None:
        """Loads and prepares the dataset. Called during FastAPI startup event."""
        if self._is_loaded:
            return

        if not self.dataset_path.exists():
            # Check alternative forecast directories if the baseline_v1 path doesn't exist
            alt_candidates = [
                settings.PROJECT_ROOT_DIR / "Future Weather Attributes" / "Forecast" / "baseline_v1" / "future_daily_weather_attributes.csv",
                settings.PROJECT_ROOT_DIR / "Future Weather Attributes" / "Forecast" / "60lookback" / "future_daily_weather_attributes.csv",
                settings.PROJECT_ROOT_DIR / "Future Weather Attributes" / "Forecast" / "lstm_gru_all_attributes" / "future_daily_weather_attributes.csv",
            ]
            found = False
            for alt in alt_candidates:
                if alt.exists():
                    self.dataset_path = alt
                    found = True
                    break
            if not found:
                raise FileNotFoundError(
                    f"Weather dataset could not be found at {self.dataset_path}. "
                    f"Please verify 'Future Weather Attributes/Forecast/'."
                )

        logger.info(f"Loading future weather dataset from: {self.dataset_path}")
        df = pd.read_csv(self.dataset_path)

        # Standardize date format to 'YYYY-MM-DD' string
        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

        # Standardize prefecture column casing (capitalize first letter, e.g. 'mie' -> 'Mie')
        df["prefecture"] = df["prefecture"].astype(str).str.strip().str.capitalize()
        if "town" in df.columns:
            df["town"] = df["town"].astype(str).str.strip()

        # Cache min/max dates
        self._min_date = str(df["date"].min())
        self._max_date = str(df["date"].max())

        # Build prefectures and towns mapping
        pref_groups = df.groupby("prefecture")["town"].unique() if "town" in df.columns else {}
        self._prefectures_map = {
            pref: sorted(list(towns)) for pref, towns in pref_groups.items()
        }

        # Keep original and create indexed multi-index for fast .loc lookups
        self.df = df
        self._indexed_df = df.set_index(["prefecture", "date"]).sort_index()

        self._is_loaded = True
        logger.info(
            f"Weather dataset loaded successfully! Total rows: {len(df):,}, "
            f"Prefectures: {len(self._prefectures_map)}, Date range: {self._min_date} to {self._max_date}"
        )

    @property
    def is_loaded(self) -> bool:
        return self._is_loaded

    def get_prefectures_and_towns(self) -> Dict[str, List[str]]:
        """Returns all available prefectures and their towns."""
        return self._prefectures_map

    def get_date_range(self) -> Tuple[str, str, int]:
        """Returns (min_date, max_date, total_days)."""
        if not self._is_loaded:
            return "", "", 0
        min_dt = pd.to_datetime(self._min_date)
        max_dt = pd.to_datetime(self._max_date)
        total_days = (max_dt - min_dt).days + 1
        return self._min_date, self._max_date, total_days

    def get_daily_weather(
        self, prefecture: str, date: str, town: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieves weather metrics for a prefecture and date.
        If town is given, selects that exact town.
        If town is omitted, returns the mean metrics across all towns in that prefecture.
        """
        norm_pref = prefecture.strip().capitalize()
        try:
            records = self._indexed_df.loc[(norm_pref, date)]
        except KeyError:
            return None

        if isinstance(records, pd.Series):
            # Single town in prefecture
            data_dict = records.to_dict()
            data_dict["is_prefecture_average"] = False
            return data_dict

        # Multiple towns exist
        if town:
            norm_town = town.strip().lower()
            town_matches = records[records["town"].str.lower() == norm_town]
            if not town_matches.empty:
                data_dict = town_matches.iloc[0].to_dict()
                data_dict["is_prefecture_average"] = False
                return data_dict

        # Return mean of numerical columns as representative prefecture value
        numeric_cols = records.select_dtypes(include=[np.number]).columns
        mean_series = records[numeric_cols].mean()
        data_dict = mean_series.to_dict()
        data_dict["prefecture"] = norm_pref
        data_dict["date"] = date
        data_dict["town"] = None
        data_dict["is_prefecture_average"] = True
        return data_dict

    def get_timeseries(
        self,
        prefecture: str,
        start_date: str,
        end_date: str,
        town: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Returns a time series for D3.js line/bar charts within [start_date, end_date].
        """
        norm_pref = prefecture.strip().capitalize()
        mask = (
            (self.df["prefecture"] == norm_pref)
            & (self.df["date"] >= start_date)
            & (self.df["date"] <= end_date)
        )
        if town:
            mask = mask & (self.df["town"].str.lower() == town.strip().lower())

        sub_df = self.df[mask]
        if sub_df.empty:
            return []

        # If town was not specified and multiple towns exist per date, group by date and take mean
        if not town:
            numeric_cols = sub_df.select_dtypes(include=[np.number]).columns
            grouped = sub_df.groupby("date")[numeric_cols].mean().reset_index()
            grouped.sort_values("date", inplace=True)
            result_df = grouped
        else:
            result_df = sub_df.sort_values("date")

        series_data = []
        for _, row in result_df.iterrows():
            series_data.append({
                "date": row["date"],
                "temperature_max": round(float(row.get("temperature_2m_max", 0)), 2),
                "temperature_min": round(float(row.get("temperature_2m_min", 0)), 2),
                "temperature_mean": round(float(row.get("temperature_2m_mean", 0)), 2),
                "rain_sum": round(float(row.get("rain_sum", 0)), 2),
                "precipitation_sum": round(float(row.get("precipitation_sum", 0)), 2),
                "snowfall_sum": round(float(row.get("snowfall_sum", 0)), 2),
                "wind_speed_max": round(float(row.get("wind_speed_10m_max", 0)), 2),
                "wind_gusts_max": round(float(row.get("wind_gusts_10m_max", 0)), 2),
                "relative_humidity_mean": round(float(row.get("relative_humidity_2m_mean", 0)), 2),
                "surface_pressure_mean": round(float(row.get("surface_pressure_mean", 0)), 2),
                "cloud_cover_mean": round(float(row.get("cloud_cover_mean", 0)), 2),
                "river_discharge": round(float(row.get("river_discharge", 0)), 2),
            })
        return series_data

    def get_map_overview(self, date: str) -> List[Dict[str, Any]]:
        """
        Returns one summary row per prefecture for a given date.
        Ideal for Frontend 2 to render the entire Japan map choropleth in a single API call!
        """
        day_df = self.df[self.df["date"] == date]
        if day_df.empty:
            return []

        # Group by prefecture to get representative coordinates and weather
        items = []
        for pref, group in day_df.groupby("prefecture"):
            lat = float(group["latitude"].mean()) if "latitude" in group else None
            lon = float(group["longitude"].mean()) if "longitude" in group else None
            temp_mean = float(group["temperature_2m_mean"].mean()) if "temperature_2m_mean" in group else None
            rain = float(group["rain_sum"].mean()) if "rain_sum" in group else 0.0
            snow = float(group["snowfall_sum"].mean()) if "snowfall_sum" in group else 0.0
            wind = float(group["wind_speed_10m_max"].mean()) if "wind_speed_10m_max" in group else 0.0

            # Simple rule-based initial risk score for the map before detailed model prediction
            risk = "Low"
            if rain > 50 or wind > 60 or snow > 20:
                risk = "High"
            elif rain > 20 or wind > 40 or snow > 5:
                risk = "Medium"

            items.append({
                "prefecture": pref,
                "date": date,
                "latitude": round(lat, 4) if lat is not None else None,
                "longitude": round(lon, 4) if lon is not None else None,
                "temperature_mean": round(temp_mean, 2) if temp_mean is not None else None,
                "rain_sum": round(rain, 2),
                "snowfall_sum": round(snow, 2),
                "wind_speed_max": round(wind, 2),
                "primary_risk_level": risk,
            })
        return items

    def get_historical_window(
        self, prefecture: str, target_date: str, days_lookback: int = 7, town: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Helper for Backend 2: fetches the last N days leading up to target_date.
        Crucial for Flood model which requires 3-day and 7-day rolling sums and discharge means.
        """
        norm_pref = prefecture.strip().capitalize()
        target_dt = pd.to_datetime(target_date)
        start_dt = target_dt - pd.Timedelta(days=days_lookback)
        start_str = start_dt.strftime("%Y-%m-%d")

        mask = (
            (self.df["prefecture"] == norm_pref)
            & (self.df["date"] >= start_str)
            & (self.df["date"] <= target_date)
        )
        if town:
            mask = mask & (self.df["town"].str.lower() == town.strip().lower())

        sub = self.df[mask].sort_values("date")
        return sub

# Singleton instance for dependency injection across routers
weather_service = WeatherQueryService()
