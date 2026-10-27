from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class PredictionRequest(BaseModel):
    prefecture: str = Field(..., description="Japan prefecture name, e.g. 'Tokyo', 'Niigata'")
    date: str = Field(..., description="Target date in 'YYYY-MM-DD' format (within 2026-02-01 to 2027-01-31)")
    town: Optional[str] = Field(None, description="Optional specific town. If omitted, uses prefecture average.")
    hazards: Optional[List[str]] = Field(
        None, 
        description="List of hazards to predict: ['flood', 'rain', 'snow', 'temperature', 'typhoon', 'wind']. If None, all are predicted."
    )

class HazardRiskResult(BaseModel):
    hazard: str = Field(..., description="Disaster name, e.g. 'flood', 'rain', 'typhoon'")
    model_name: str = Field(..., description="Name of the model used for inference")
    risk_level: str = Field(..., description="Categorical risk: 'Low', 'Medium', 'High', 'Critical'")
    probability: Optional[float] = Field(None, description="Class probability between 0.0 and 1.0 (if classification)")
    predicted_value: Optional[float] = Field(None, description="Continuous predicted quantity (if regression, e.g. max temp °C)")
    unit: Optional[str] = Field(None, description="Measurement unit, e.g. '°C', 'km/h', 'probability'")
    threshold_exceeded: bool = Field(False, description="True if hazard triggers warning threshold")
    alert_message: Optional[str] = Field(None, description="Actionable alert recommendation")
    contributing_factors: Optional[Dict[str, float]] = Field(None, description="Key input features and values considered")

class PredictionResponse(BaseModel):
    prefecture: str
    town: Optional[str] = None
    date: str
    overall_risk_level: str = Field(..., description="Highest severity risk among evaluated hazards")
    weather_summary: Dict[str, Any] = Field(..., description="Core meteorological indicators for context cards")
    risks: List[HazardRiskResult] = Field(..., description="Prediction results per requested hazard")
    execution_mode: str = Field("mock", description="'mock' (Backend 1 placeholder) or 'inference' (Backend 2 live ML model)")
