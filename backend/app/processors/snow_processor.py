from typing import Dict, Any, List, Union
import numpy as np
import pandas as pd
from app.processors.base_processor import BaseProcessor

class SnowProcessor(BaseProcessor):
    """
    [BACKEND 2 TASK] - Feature Processor for Heavy Snowfall Models.
    
    Model source: Heavy Snow/src/model_train.py
    Model files:
      - Heavy Snow/trained_models/niigata/random_forest.joblib
      - Heavy Snow/trained_models/yamagata/random_forest.joblib
    
    Expected features (in exact training order):
      1. max_temperature
      2. min_temperature
      3. max_humidity
      4. min_humidity
      5. max_wind_speed
      6. min_wind_speed_log (np.log1p of min wind speed)
    """

    @property
    def required_features(self) -> List[str]:
        return [
            "max_temperature",
            "min_temperature",
            "max_humidity",
            "min_humidity",
            "max_wind_speed",
            "min_wind_speed_log",
        ]

    def transform(self, weather_data: Dict[str, Any]) -> pd.DataFrame:
        # Map generic weather column names to the snow model feature names
        max_temp = float(weather_data.get("temperature_2m_max", 0.0) or 0.0)
        min_temp = float(weather_data.get("temperature_2m_min", 0.0) or 0.0)
        max_hum = float(weather_data.get("relative_humidity_2m_max", 80.0) or 80.0)
        min_hum = float(weather_data.get("relative_humidity_2m_min", 50.0) or 50.0)
        max_wind = float(weather_data.get("wind_speed_10m_max", 10.0) or 10.0)
        supplied_log = weather_data.get("min_wind_speed_log")
        if supplied_log is not None:
            min_wind_log = float(supplied_log)
        else:
            min_wind = float(weather_data.get("wind_speed_10m_min", 2.0) or 2.0)
            min_wind_log = float(np.log1p(max(0.0, min_wind)))

        vector = [max_temp, min_temp, max_hum, min_hum, max_wind, min_wind_log]
        return pd.DataFrame([vector], columns=self.required_features)

snow_processor = SnowProcessor()
