from typing import Dict, Any, List, Union
import numpy as np
import pandas as pd
from app.processors.base_processor import BaseProcessor

class TemperatureProcessor(BaseProcessor):
    """
    [BACKEND 2 TASK] - Feature Processor for Maximum Temperature Regression Models.
    
    Model source: Temperature/train_temperature_models.py
    Model files:
      - Temperature/trained_models/hist_gradient_boosting_temp_max.joblib
      - Temperature/trained_models/gradient_boosting_temp_max.joblib
      - Temperature/trained_models/linear_regression_temp_max.joblib
    
    Expected features (in exact training order):
      1. shortwave_radiation_sum
      2. sunshine_duration
      3. daylight_duration
      4. cloud_cover_mean
      5. dew_point_2m_mean
      6. month
    """

    @property
    def required_features(self) -> List[str]:
        return [
            "shortwave_radiation_sum",
            "sunshine_duration",
            "daylight_duration",
            "cloud_cover_mean",
            "dew_point_2m_mean",
            "month",
        ]

    def transform(self, weather_data: Dict[str, Any]) -> pd.DataFrame:
        values = []
        for feat in self.required_features:
            if feat == "month":
                val = weather_data.get("month")
                if val is None and "date" in weather_data:
                    val = pd.to_datetime(weather_data["date"], errors="raise").month
                month = int(float(val)) if val is not None else 6
                if not 1 <= month <= 12:
                    raise ValueError(f"month must be between 1 and 12, got {month}")
                values.append(float(month))
            else:
                val = weather_data.get(feat, 0.0)
                values.append(float(val) if val is not None else 0.0)
        return pd.DataFrame([values], columns=self.required_features)

temperature_processor = TemperatureProcessor()
