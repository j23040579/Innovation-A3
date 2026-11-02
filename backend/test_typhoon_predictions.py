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
    def test_forecast_typhoon_profiles_do_not_claim_occurrence_risk(self):
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
        registry = ModelRegistry()
        registry.models["typhoon"] = model
        registry.model_names["typhoon"] = "Random Forest Pipeline (Typhoon)"
        for prefecture, date, expected_profile in [
            ("Tokyo", "2026-06-15", "High"),
            ("Yamanashi", "2026-08-15", "High"),
        ]:
            with self.subTest(prefecture=prefecture, date=date):
                weather = weather_service.get_daily_weather(prefecture, date)
                self.assertIsNotNone(weather)
                probabilities = model.predict_proba(typhoon_processor.transform(weather))[0]
                result = registry.predict("typhoon", weather, prefecture)
                self.assertEqual(result.risk_level, "Unassessed")
                self.assertFalse(result.threshold_exceeded)
                self.assertIsNone(result.probability)
                self.assertEqual(result.profile_match_class, expected_profile)
                self.assertEqual(
                    result.profile_match_probabilities,
                    {
                        str(label).lower(): round(float(probability), 3)
                        for label, probability in zip(model.classes_, probabilities)
                    },
                )
                self.assertIn("occurrence risk is unassessed", result.alert_message)
