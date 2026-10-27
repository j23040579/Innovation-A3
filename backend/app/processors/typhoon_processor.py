from typing import Dict, Any, List
import pandas as pd
import numpy as np
from app.processors.base_processor import BaseProcessor

class TyphoonProcessor(BaseProcessor):
    """
    [BACKEND 2 TASK] - Feature Processor for Typhoon Risk Profile Models.
    
    Model source: Typhoon/train_typhoon_models.py
    Model files:
      - Typhoon/trained_models/risk/final_test2/random_forest_model.joblib
      - Typhoon/trained_models/risk/final_test2/gradient_boosting_model.joblib
      - Typhoon/trained_models/risk/final_test2/cart_model.joblib
      - Typhoon/trained_models/risk/final_test2/svm_model.joblib
    
    Note: The saved joblib model is a complete sklearn Pipeline that includes
    the ColumnTransformer (StandardScaler + Sine/Cosine for wind direction).
    It expects a DataFrame with the 28 column names below.
    """

    @property
    def required_features(self) -> List[str]:
        return [
            "temperature_2m_mean",
            "temperature_2m_max",
            "temperature_2m_min",
            "relative_humidity_2m_mean",
            "relative_humidity_2m_max",
            "relative_humidity_2m_min",
            "dew_point_2m_mean",
            "dew_point_2m_max",
            "dew_point_2m_min",
            "precipitation_sum",
            "rain_sum",
            "precipitation_hours",
            "cloud_cover_mean",
            "cloud_cover_max",
            "cloud_cover_min",
            "pressure_msl_max",
            "pressure_msl_min",
            "surface_pressure_mean",
            "surface_pressure_max",
            "surface_pressure_min",
            "wind_speed_10m_mean",
            "wind_speed_10m_max",
            "wind_speed_10m_min",
            "wind_gusts_10m_mean",
            "wind_gusts_10m_max",
            "wind_gusts_10m_min",
            "wind_direction_10m_dominant",
            "shortwave_radiation_sum",
        ]

    def transform(self, weather_data: Dict[str, Any]) -> pd.DataFrame:
        """
        Creates a 1-row pandas DataFrame matching the 28 feature names
        expected by the Typhoon Pipeline.
        """
        row_dict = {}
        for feat in self.required_features:
            val = weather_data.get(feat, 0.0)
            row_dict[feat] = [float(val) if val is not None else 0.0]
        return pd.DataFrame(row_dict)

typhoon_processor = TyphoonProcessor()
