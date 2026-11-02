from typing import List
from fastapi import APIRouter, HTTPException
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.weather_query_service import weather_service, canonicalize_prefecture
from app.services.inference_service import inference_service

router = APIRouter(prefix="/predict", tags=["Disaster Prediction"])

@router.get(
    "/hazards",
    response_model=List[str],
    summary="List supported disaster prediction hazards",
    description="Returns the identifiers of all meteorological hazards handled by the models."
)
def get_supported_hazards():
    return inference_service.AVAILABLE_HAZARDS

@router.get(
    "/snow-coverage",
    response_model=List[str],
    summary="List prefectures with loaded snow models",
    description="Returns prefectures with a region-specific snow model artifact loaded by the inference service."
)
def get_snow_coverage():
    return inference_service.snow_supported_prefectures

@router.post(
    "",
    response_model=PredictionResponse,
    summary="Predict disaster risks for a prefecture and date",
    description="Fetches meteorological features from the future dataset and evaluates disaster risk models."
)
def predict_disaster_risks(request: PredictionRequest):
    # 1. Fetch raw weather features for the requested prefecture and date
    weather_dict = weather_service.get_daily_weather(
        prefecture=request.prefecture,
        date=request.date,
        town=request.town
    )

    if not weather_dict:
        raise HTTPException(
            status_code=404,
            detail=f"No forecast weather record is available for prefecture '{request.prefecture}' "
                   f"on date '{request.date}'. The configured forecast dataset does not contain this prefecture/date."
        )

    # 2. Run inference engine (or mock fallback if Backend 2 is not yet plugged in)
    prediction_result = inference_service.run_predictions(
        prefecture=canonicalize_prefecture(request.prefecture),
        date=request.date,
        weather_features=weather_dict,
        requested_hazards=request.hazards,
        town=request.town
    )

    return prediction_result
