import logging
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
import joblib
import numpy as np

from app.core.config import settings
from app.schemas.prediction import HazardRiskResult
from app.processors import (
    flood_processor,
    rain_processor,
    snow_processor,
    temperature_processor,
    typhoon_processor,
    wind_processor,
)

logger = logging.getLogger(__name__)

class ModelRegistry:
    """
    [BACKEND 2 ARCHITECTURE] - Model Registry & Inference Engine.
    
    Loads trained .joblib models into memory once at server startup.
    Supports primary GradientBoosting models with automatic fallback to alternative
    architectures (CART, Linear Regression, etc.) if version mismatches occur.
    Coordinates between feature processors and model inference calls.
    """

    def __init__(self):
        self.models: Dict[str, Any] = {}
        self.model_names: Dict[str, str] = {}
        self.is_ready: bool = False
        self.root_dir = settings.PROJECT_ROOT_DIR

    def _load_with_fallbacks(self, hazard: str, candidates: List[Tuple[Path, str]]) -> bool:
        """
        Attempts to load the first working model file from the candidates list.
        """
        for rel_path, display_name in candidates:
            path = self.root_dir / rel_path
            if path.exists():
                try:
                    loaded = joblib.load(path)
                    self._validate_model_contract(hazard, loaded, path)
                    self.models[hazard] = loaded
                    self.model_names[hazard] = display_name
                    logger.info(f"Loaded {hazard.capitalize()} model: '{display_name}' from {path.name}")
                    return True
                except Exception as e:
                    logger.warning(f"Could not load candidate model {path.name} for {hazard}: {e}")
        return False

    def _processor_for(self, hazard: str):
        return {
            "flood": flood_processor,
            "rain": rain_processor,
            "snow": snow_processor,
            "temperature": temperature_processor,
            "typhoon": typhoon_processor,
            "wind": wind_processor,
        }[hazard]

    def _validate_model_contract(self, hazard: str, model: Any, path: Path) -> None:
        """Reject artifacts that cannot accept the processor's feature contract."""
        processor_features = set(self._processor_for(hazard).required_features)
        model_features = getattr(model, "feature_names_in_", None)
        if model_features is not None:
            missing = set(model_features) - processor_features
            if missing:
                raise ValueError(
                    f"{path.name} requires unsupported {hazard} features: {sorted(missing)}"
                )
            return

        expected_count = len(processor_features)
        actual_count = getattr(model, "n_features_in_", None)
        if actual_count is not None and hazard != "snow" and actual_count != expected_count:
            raise ValueError(
                f"{path.name} expects {actual_count} features, processor provides {expected_count}"
            )

    def _model_input(self, hazard: str, weather_data: Dict[str, Any]) -> Any:
        """Build a named DataFrame aligned to the loaded model's feature order."""
        frame = self._processor_for(hazard).transform(weather_data)
        expected = getattr(self.models[hazard], "feature_names_in_", None)
        if expected is not None:
            missing = [column for column in expected if column not in frame.columns]
            if missing:
                raise ValueError(f"Missing {hazard} model features: {missing}")
            return frame.loc[:, list(expected)]
        return frame

    @staticmethod
    def _probability(model: Any, model_input: Any) -> Optional[float]:
        if not hasattr(model, "predict_proba"):
            return None
        probabilities = np.asarray(model.predict_proba(model_input), dtype=float)
        return float(np.max(probabilities[0]))

    def load_all_models(self) -> None:
        """
        Loads the best performing models for each hazard from the project folders,
        with fallback options if version discrepancies or missing files occur.
        """
        logger.info("Attempting to load trained .joblib models from project directory...")
        self.models.clear()
        self.model_names.clear()
        self.is_ready = False
        loaded_count = 0

        # 1. Flood Model (Gradient Boosting -> CART -> ID3)
        if self._load_with_fallbacks("flood", [
            (Path("Flood") / "trained_models" / "gradient_boosting_flood.joblib", "Gradient Boosting (Flood Classifier)"),
            (Path("Flood") / "trained_models" / "cart_flood.joblib", "CART (Flood Classifier)"),
            (Path("Flood") / "trained_models" / "id3_flood.joblib", "ID3 Decision Tree (Flood Classifier)"),
        ]):
            loaded_count += 1

        # 2. Rain Model (Gradient Boosting -> CART)
        if self._load_with_fallbacks("rain", [
            (Path("Rain") / "trained_models" / "gradient_boosting.joblib", "Gradient Boosting (Rain Classifier)"),
            (Path("Rain") / "trained_models" / "cart.joblib", "CART (Rain Classifier)"),
        ]):
            loaded_count += 1

        # 3. Snow Model (Niigata RF -> Yamagata RF)
        if self._load_with_fallbacks("snow", [
            (Path("Heavy Snow") / "trained_models" / "niigata" / "random_forest.joblib", "Random Forest Classifier (Snow)"),
            (Path("Heavy Snow") / "trained_models" / "yamagata" / "random_forest.joblib", "Random Forest Classifier (Snow)"),
        ]):
            loaded_count += 1

        # 4. Temperature Model (HistGradientBoosting -> Gradient Boosting -> Linear Regression)
        if self._load_with_fallbacks("temperature", [
            (Path("Temperature") / "trained_models" / "hist_gradient_boosting_temp_max.joblib", "HistGradientBoosting Regressor (Temperature)"),
            (Path("Temperature") / "trained_models" / "gradient_boosting_temp_max.joblib", "Gradient Boosting Regressor (Temperature)"),
            (Path("Temperature") / "trained_models" / "linear_regression_temp_max.joblib", "Linear Regression (Temperature)"),
        ]):
            loaded_count += 1

        # 5. Wind Model (Gradient Boosting -> HistGradientBoosting -> Multiple Linear Regression)
        if self._load_with_fallbacks("wind", [
            (Path("Wind") / "trained_models" / "gradient_boosting.joblib", "Gradient Boosting Regressor (Wind)"),
            (Path("Wind") / "trained_models" / "hist_gradient_boosting.joblib", "HistGradientBoosting Regressor (Wind)"),
            (Path("Wind") / "trained_models" / "multiple_linear_regression.joblib", "Multiple Linear Regression (Wind)"),
        ]):
            loaded_count += 1

        # 6. Typhoon Model
        if self._load_with_fallbacks("typhoon", [
            (Path("Typhoon") / "trained_models" / "risk" / "final_test2" / "random_forest_model.joblib", "Random Forest Pipeline (Typhoon)"),
        ]):
            loaded_count += 1

        if loaded_count > 0:
            self.is_ready = True
            logger.info(f"ModelRegistry initialized with {loaded_count} active models.")
        else:
            logger.info("No joblib models were loaded; running in mock mode.")

    def predict(
        self, hazard: str, weather_data: Dict[str, Any], prefecture: str, town: Optional[str] = None
    ) -> HazardRiskResult:
        """
        Executes prediction using the appropriate processor and loaded model.
        """
        model = self.models.get(hazard)
        if model is None:
            raise KeyError(f"No loaded model for hazard: {hazard}")

        # --- FLOOD ---
        if hazard == "flood":
            X = self._model_input(hazard, weather_data)
            pred = model.predict(X)[0]
            prob = self._probability(model, X)
            return HazardRiskResult(
                hazard="flood",
                model_name=self.model_names.get("flood", "Gradient Boosting (Flood Classifier)"),
                risk_level=str(pred),
                probability=round(prob, 3) if prob is not None else None,
                unit="class",
                threshold_exceeded=str(pred) in ["Medium", "High"],
                alert_message="High flood probability detected" if str(pred) == "High" else "Normal river conditions",
                contributing_factors={"elevation": float(weather_data.get("elevation", 0))}
            )

        # --- RAIN ---
        elif hazard == "rain":
            X = self._model_input(hazard, weather_data)
            pred = model.predict(X)[0]
            prob = self._probability(model, X)
            is_rain = str(pred) not in ["No/Minimal Rain", "No Rain", "None"]
            return HazardRiskResult(
                hazard="rain",
                model_name=self.model_names.get("rain", "Gradient Boosting (Rain Classifier)"),
                risk_level=str(pred),
                probability=round(prob, 3) if prob is not None else None,
                unit="class",
                threshold_exceeded=is_rain,
                alert_message="Rain warning issued" if is_rain else "Clear weather expected"
            )

        # --- SNOW ---
        elif hazard == "snow":
            df_in = self._model_input(hazard, weather_data)
            pred = model.predict(df_in)[0]
            prob = self._probability(model, df_in)
            risk_labels = {0: "Low", 1: "Medium", 2: "High"}
            risk_str = risk_labels.get(pred, str(pred))
            return HazardRiskResult(
                hazard="snow",
                model_name=self.model_names.get("snow", "Random Forest Classifier (Snow)"),
                risk_level=risk_str,
                probability=round(prob, 3) if prob is not None else None,
                unit="class",
                threshold_exceeded=risk_str in ["Medium", "High"],
                alert_message="Heavy snowfall hazard alert" if risk_str == "High" else "Snowfall within safe levels"
            )

        # --- TEMPERATURE (REGRESSION) ---
        elif hazard == "temperature":
            X = self._model_input(hazard, weather_data)
            pred_temp = float(model.predict(X)[0])
            risk = "Critical" if pred_temp >= 36 else ("High" if pred_temp >= 33 else ("Medium" if pred_temp >= 28 else "Low"))
            return HazardRiskResult(
                hazard="temperature",
                model_name=self.model_names.get("temperature", "HistGradientBoosting Regressor"),
                risk_level=risk,
                predicted_value=round(pred_temp, 1),
                unit="°C",
                threshold_exceeded=pred_temp >= 33,
                alert_message="Extreme heat advisory" if pred_temp >= 33 else "Temperature is normal"
            )

        # --- WIND (REGRESSION) ---
        elif hazard == "wind":
            X = self._model_input(hazard, weather_data)
            pred_wind = float(model.predict(X)[0])
            risk = "Critical" if pred_wind > 65 else ("High" if pred_wind > 50 else ("Medium" if pred_wind > 35 else "Low"))
            return HazardRiskResult(
                hazard="wind",
                model_name=self.model_names.get("wind", "Gradient Boosting Regressor (Wind)"),
                risk_level=risk,
                predicted_value=round(pred_wind, 1),
                unit="km/h",
                threshold_exceeded=pred_wind > 50,
                alert_message="High wind speeds predicted" if pred_wind > 50 else "Wind conditions normal"
            )

        # --- TYPHOON ---
        elif hazard == "typhoon":
            df_in = self._model_input(hazard, weather_data)
            pred = model.predict(df_in)[0]
            prob = self._probability(model, df_in)
            return HazardRiskResult(
                hazard="typhoon",
                model_name=self.model_names.get("typhoon", "Random Forest Pipeline (Typhoon)"),
                risk_level=str(pred),
                probability=round(prob, 3) if prob is not None else None,
                unit="profile_class",
                threshold_exceeded=str(pred) in ["Medium", "High"],
                alert_message="Typhoon wind/pressure signature detected" if str(pred) in ["Medium", "High"] else "No typhoon threat"
            )

        raise NotImplementedError(f"Prediction logic for {hazard} is not yet implemented.")

model_registry = ModelRegistry()
