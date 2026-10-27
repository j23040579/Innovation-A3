from typing import Dict, Any, List, Union
import numpy as np
import pandas as pd
from app.processors.base_processor import BaseProcessor

class WindProcessor(BaseProcessor):
    """
    [BACKEND 2 TASK] - Feature Processor for Wind Speed Models.
    
    Model source: Wind/train_wind_models.py
    Model files:
      - Wind/trained_models/hist_gradient_boosting.joblib
      - Wind/trained_models/gradient_boosting.joblib
      - Wind/trained_models/multiple_linear_regression.joblib
    
    Expected features (in exact training order):
      1. surface_pressure_mean
      2. surface_pressure_max
      3. surface_pressure_min
      4. pressure_change
      5. wind_direction_10m_dominant
    """

    @property
    def required_features(self) -> List[str]:
        return [
            "surface_pressure_mean",
            "surface_pressure_max",
            "surface_pressure_min",
            "pressure_change",
            "wind_direction_10m_dominant",
        ]

    def transform(self, weather_data: Dict[str, Any]) -> pd.DataFrame:
        values = []
        for feat in self.required_features:
            val = weather_data.get(feat, 0.0)
            values.append(float(val) if val is not None else 0.0)
        return pd.DataFrame([values], columns=self.required_features)

wind_processor = WindProcessor()
