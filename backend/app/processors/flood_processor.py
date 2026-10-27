from typing import Dict, Any, List, Union
import numpy as np
import pandas as pd
from app.processors.base_processor import BaseProcessor

class FloodProcessor(BaseProcessor):
    """
    [BACKEND 2 TASK] - Feature Processor for Flood Models.
    
    Model source: Flood/train_flood_models.py
    Model files:
      - Flood/trained_models/gradient_boosting_flood.joblib
      - Flood/trained_models/cart_flood.joblib
      - Flood/trained_models/id3_flood.joblib
    
    Expected features (in exact training order):
      1. rain_sum_past_3day
      2. rain_sum_past_7day
      3. max_daily_rain_past_7day
      4. precipitation_hours_past_7day
      5. river_discharge_previous_day
      6. river_discharge_mean_7day
      7. river_discharge_median_7day
      8. river_discharge_max_7day
      9. discharge_ratio
      10. elevation
    """

    @property
    def required_features(self) -> List[str]:
        return [
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
        ]

    def transform(self, weather_data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extracts and aligns features into a pandas DataFrame [1, 10] matching training names.
        If 7-day rolling metrics are not already pre-calculated in the dictionary,
        fallback estimates or weather_service.get_historical_window() can be utilized.
        """
        values = []
        for feat in self.required_features:
            val = weather_data.get(feat, 0.0)
            values.append(float(val) if val is not None else 0.0)
        return pd.DataFrame([values], columns=self.required_features)

flood_processor = FloodProcessor()
