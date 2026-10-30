from typing import Dict, Any, List, Union
import numpy as np
import pandas as pd
from app.processors.base_processor import BaseProcessor

class RainProcessor(BaseProcessor):
    """
    [BACKEND 2 TASK] - Feature Processor for Rain Models.
    
    Model source: Rain/train_rain_models.py
    Model files:
      - Rain/trained_models/gradient_boosting.joblib
      - Rain/trained_models/cart.joblib
    
    Expected features (in exact training order):
      1. temperature_2m_max
      2. relative_humidity_2m_mean
      3. dew_point_2m_mean
      4. cloud_cover_mean
      5. pressure_msl_mean
      6. wind_speed_10m_max
      7. shortwave_radiation_sum
      8. month
    """

    @property
    def required_features(self) -> List[str]:
        return [
            "temperature_2m_max",
            "relative_humidity_2m_mean",
            "dew_point_2m_mean",
            "cloud_cover_mean",
            "pressure_msl_mean",
            "wind_speed_10m_max",
            "shortwave_radiation_sum",
            "month",
        ]

    def transform(self, weather_data: Dict[str, Any]) -> pd.DataFrame:
        values = []
        for feat in self.required_features:
            if feat == "month":
                # Extract month from date string (YYYY-MM-DD) if not present
                val = weather_data.get("month")
                if val is None and "date" in weather_data:
                    val = pd.to_datetime(weather_data["date"], errors="raise").month
                month = int(float(val)) if val is not None else 1
                if not 1 <= month <= 12:
                    raise ValueError(f"month must be between 1 and 12, got {month}")
                values.append(float(month))
            else:
                val = weather_data.get(feat, 0.0)
                values.append(float(val) if val is not None else 0.0)
        return pd.DataFrame([values], columns=self.required_features)

rain_processor = RainProcessor()
