import logging
from typing import Dict, List, Optional, Any
from app.schemas.prediction import HazardRiskResult, PredictionResponse

logger = logging.getLogger(__name__)

class InferenceService:
    """
    Bridge between Backend 1 (API Orchestration) and Backend 2 (Inference Engine).
    
    If Backend 2's model registry and processors are available and loaded,
    this service invokes them. Otherwise, it generates structured, realistic mock predictions
    matching the exact schema, allowing the Frontend team to develop without waiting.
    """

    AVAILABLE_HAZARDS = ["flood", "rain", "snow", "temperature", "typhoon", "wind"]

    def __init__(self):
        self._backend2_ready = False
        self._model_registry = None

    def initialize_backend2(self, model_registry=None):
        """Called if Backend 2's model registry is initialized."""
        if model_registry and getattr(model_registry, "is_ready", False):
            self._model_registry = model_registry
            self._backend2_ready = True
            logger.info("Backend 2 Model Registry connected successfully.")
        else:
            self._backend2_ready = False
            logger.info("Running with Backend 1 mock inference engine.")

    def run_predictions(
        self,
        prefecture: str,
        date: str,
        weather_features: Dict[str, Any],
        requested_hazards: Optional[List[str]] = None,
        town: Optional[str] = None
    ) -> PredictionResponse:
        """
        Executes prediction for all requested hazards.
        """
        hazards = [h.lower() for h in (requested_hazards or self.AVAILABLE_HAZARDS)]
        hazards = [h for h in hazards if h in self.AVAILABLE_HAZARDS]

        results: List[HazardRiskResult] = []
        highest_severity_rank = 0
        severity_rank_map = {"Low": 0, "Medium": 1, "High": 2, "Critical": 3}

        for hazard in hazards:
            result = self._predict_single_hazard(hazard, weather_features, prefecture, town)
            results.append(result)
            rank = severity_rank_map.get(result.risk_level, 0)
            if rank > highest_severity_rank:
                highest_severity_rank = rank

        rank_to_severity = {0: "Low", 1: "Medium", 2: "High", 3: "Critical"}
        overall_risk = rank_to_severity[highest_severity_rank]

        # Extract a clean, user-friendly weather summary for the cards
        summary = {
            "temperature_max": round(float(weather_features.get("temperature_2m_max", 0)), 1),
            "temperature_min": round(float(weather_features.get("temperature_2m_min", 0)), 1),
            "rain_sum_mm": round(float(weather_features.get("rain_sum", 0)), 1),
            "snowfall_sum_cm": round(float(weather_features.get("snowfall_sum", 0)), 1),
            "wind_speed_max_kmh": round(float(weather_features.get("wind_speed_10m_max", 0)), 1),
            "relative_humidity_pct": round(float(weather_features.get("relative_humidity_2m_mean", 0)), 1),
            "surface_pressure_hpa": round(float(weather_features.get("surface_pressure_mean", 0)), 1),
            "river_discharge": round(float(weather_features.get("river_discharge", 0)), 2),
        }

        return PredictionResponse(
            prefecture=prefecture,
            town=town,
            date=date,
            overall_risk_level=overall_risk,
            weather_summary=summary,
            risks=results,
            execution_mode="inference" if self._backend2_ready else "mock"
        )

    def _predict_single_hazard(
        self, hazard: str, weather: Dict[str, Any], prefecture: str, town: Optional[str]
    ) -> HazardRiskResult:
        """
        Dispatches to real ML model (Backend 2) if ready, or evaluates realistic mock rule.
        """
        # If Backend 2 models are plugged in:
        if self._backend2_ready and self._model_registry:
            try:
                return self._model_registry.predict(hazard, weather, prefecture, town)
            except Exception as e:
                logger.warning(f"Backend 2 inference for {hazard} failed, falling back to mock: {e}")

        # Fallback Mock Logic: derives intelligent risk scores from weather features
        rain = float(weather.get("rain_sum", 0) or 0)
        snow = float(weather.get("snowfall_sum", 0) or 0)
        temp_max = float(weather.get("temperature_2m_max", 20) or 20)
        wind_max = float(weather.get("wind_speed_10m_max", 15) or 15)
        wind_gust = float(weather.get("wind_gusts_10m_max", 25) or 25)
        pressure = float(weather.get("surface_pressure_mean", 1013) or 1013)
        river = float(weather.get("river_discharge", 0) or 0)

        if hazard == "flood":
            prob = min(0.95, max(0.05, (rain * 0.015) + (river * 0.02)))
            risk = "High" if prob > 0.65 else ("Medium" if prob > 0.35 else "Low")
            return HazardRiskResult(
                hazard="flood",
                model_name="Gradient Boosting (Flood Classifier)",
                risk_level=risk,
                probability=round(prob, 3),
                unit="probability",
                threshold_exceeded=prob > 0.5,
                alert_message="Potential river overflow risk" if prob > 0.5 else "Flood conditions normal",
                contributing_factors={"rain_sum_past_days": rain, "river_discharge": river}
            )

        elif hazard == "rain":
            prob = min(0.98, max(0.02, rain / 60.0))
            risk = "High" if rain > 50 else ("Medium" if rain > 15 else "Low")
            return HazardRiskResult(
                hazard="rain",
                model_name="CART / Gradient Boosting (Rain Classifier)",
                risk_level=risk,
                probability=round(prob, 3),
                predicted_value=round(rain, 1),
                unit="mm",
                threshold_exceeded=rain > 30,
                alert_message="Heavy downpour warning" if rain > 30 else "Normal precipitation",
                contributing_factors={"rain_sum": rain, "cloud_cover_mean": float(weather.get("cloud_cover_mean", 50))}
            )

        elif hazard == "snow":
            prob = min(0.95, max(0.01, snow / 30.0))
            risk = "High" if snow > 20 else ("Medium" if snow > 5 else "Low")
            return HazardRiskResult(
                hazard="snow",
                model_name="Random Forest (Snowfall Risk Predictor)",
                risk_level=risk,
                probability=round(prob, 3),
                predicted_value=round(snow, 1),
                unit="cm",
                threshold_exceeded=snow > 15,
                alert_message="Heavy snowfall and blizzard conditions possible" if snow > 15 else "Snow conditions manageable",
                contributing_factors={"snowfall_sum": snow, "temperature_min": float(weather.get("temperature_2m_min", 0))}
            )

        elif hazard == "temperature":
            # Regression target: temperature_2m_max
            risk = "Critical" if temp_max >= 36 else ("High" if temp_max >= 33 else ("Medium" if temp_max >= 28 else "Low"))
            return HazardRiskResult(
                hazard="temperature",
                model_name="HistGradientBoosting Regressor",
                risk_level=risk,
                predicted_value=round(temp_max, 1),
                unit="°C",
                threshold_exceeded=temp_max >= 33,
                alert_message="Heat stroke alert: extreme high temperatures expected" if temp_max >= 33 else "Temperatures within comfortable range",
                contributing_factors={"temperature_2m_max": temp_max, "dew_point_2m_mean": float(weather.get("dew_point_2m_mean", 15))}
            )

        elif hazard == "wind":
            risk = "High" if wind_max > 60 else ("Medium" if wind_max > 35 else "Low")
            return HazardRiskResult(
                hazard="wind",
                model_name="Gradient Boosting Regressor (Wind Speed)",
                risk_level=risk,
                predicted_value=round(wind_max, 1),
                unit="km/h",
                threshold_exceeded=wind_max > 50,
                alert_message="Gale warning: high wind velocities detected" if wind_max > 50 else "Wind speeds within safe parameters",
                contributing_factors={"surface_pressure_mean": pressure, "wind_speed_10m_max": wind_max}
            )

        elif hazard == "typhoon":
            is_cyclonic = pressure < 1000 and wind_gust > 55
            prob = min(0.95, max(0.05, ((1015 - pressure) * 0.03) + (wind_gust * 0.008)))
            risk = "High" if is_cyclonic or prob > 0.65 else ("Medium" if prob > 0.35 else "Low")
            return HazardRiskResult(
                hazard="typhoon",
                model_name="Random Forest Pipeline (Typhoon Risk Profile)",
                risk_level=risk,
                probability=round(prob, 3),
                unit="probability",
                threshold_exceeded=risk in ["Medium", "High"],
                alert_message="Tropical cyclone profile matched: potential typhoon impact" if risk in ["Medium", "High"] else "No active typhoon signals",
                contributing_factors={"surface_pressure_min": pressure, "wind_gusts_10m_max": wind_gust}
            )

        # Fallback default
        return HazardRiskResult(
            hazard=hazard,
            model_name="Unknown Model",
            risk_level="Low",
            threshold_exceeded=False
        )

inference_service = InferenceService()
