import sys
import unittest
from pathlib import Path

import joblib

BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent
sys.path.insert(0, str(BACKEND_DIR))

from app.processors.typhoon_processor import typhoon_processor
from app.services.model_registry import ModelRegistry
from app.services.weather_query_service import WeatherQueryService


class TyphoonPredictionTests(unittest.TestCase):
    def test_typhoon_profile_posteriors_map_to_distinct_levels(self):
        self.assertEqual(
            ModelRegistry._typhoon_risk_level([0.80, 0.10, 0.10], ["High", "Low", "Medium"]),
            "Medium",
        )
        self.assertEqual(
            ModelRegistry._typhoon_risk_level([0.92, 0.04, 0.04], ["High", "Low", "Medium"]),
            "High",
        )
        self.assertEqual(
            ModelRegistry._typhoon_risk_level([0.40, 0.30, 0.30], ["High", "Low", "Medium"]),
            "Low",
        )

    def test_forecast_typhoon_levels_use_probability_support(self):
        model_path = (
            PROJECT_ROOT
            / "Typhoon"
            / "trained_models"
            / "risk"
            / "final_test2"
            / "random_forest_model.joblib"
        )
        if not model_path.exists():
            self.skipTest("saved typhoon model is not present")

        model = joblib.load(model_path)
        weather_service = WeatherQueryService()
        weather_service.load_dataset()
        for prefecture, date, expected_level in [
            ("Tokyo", "2026-06-15", "High"),
            ("Yamanashi", "2026-08-15", "Low"),
        ]:
            with self.subTest(prefecture=prefecture, date=date):
                weather = weather_service.get_daily_weather(prefecture, date)
                self.assertIsNotNone(weather)
                probabilities = model.predict_proba(typhoon_processor.transform(weather))[0]
                self.assertEqual(
                    ModelRegistry._typhoon_risk_level(probabilities, model.classes_),
                    expected_level,
                )
