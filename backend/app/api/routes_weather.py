from typing import Optional
from fastapi import APIRouter, Query, HTTPException
from app.schemas.weather import DailyWeatherResponse, TimeSeriesResponse, MapOverviewResponse, MapOverviewItem
from app.services.weather_query_service import weather_service

router = APIRouter(prefix="/weather", tags=["Weather Data"])

@router.get(
    "/daily",
    response_model=DailyWeatherResponse,
    summary="Get single-day weather attributes",
    description="Query detailed meteorological parameters for a prefecture on a specific date (e.g. 2026-06-15)."
)
def get_daily_weather(
    prefecture: str = Query(..., description="Japan prefecture name, e.g. Tokyo, Osaka, Niigata"),
    date: str = Query(..., description="Date formatted as YYYY-MM-DD"),
    town: Optional[str] = Query(None, description="Optional specific town name")
):
    weather = weather_service.get_daily_weather(prefecture, date, town)
    if not weather:
        raise HTTPException(
            status_code=404,
            detail=f"No weather records found for prefecture '{prefecture}' on date '{date}'. "
                   f"Please verify spelling and ensure date falls within the valid date range."
        )

    is_avg = weather.get("is_prefecture_average", False)
    clean_metrics = {k: v for k, v in weather.items() if k not in ["prefecture", "date", "town", "is_prefecture_average"]}

    return DailyWeatherResponse(
        prefecture=prefecture.capitalize(),
        town=town,
        date=date,
        is_prefecture_average=is_avg,
        metrics=clean_metrics
    )

@router.get(
    "/timeseries",
    response_model=TimeSeriesResponse,
    summary="Get time-series weather series for D3.js charts",
    description="Fetches a sequence of daily metrics (temp, rainfall, wind, humidity, pressure) across a date window."
)
def get_weather_timeseries(
    prefecture: str = Query(..., description="Japan prefecture name"),
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date (YYYY-MM-DD)"),
    town: Optional[str] = Query(None, description="Optional specific town")
):
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="start_date must be less than or equal to end_date")

    series = weather_service.get_timeseries(prefecture, start_date, end_date, town)
    if not series:
        raise HTTPException(
            status_code=404,
            detail=f"No time-series data found for '{prefecture}' between {start_date} and {end_date}."
        )

    return TimeSeriesResponse(
        prefecture=prefecture.capitalize(),
        town=town,
        start_date=start_date,
        end_date=end_date,
        total_data_points=len(series),
        series=series
    )

@router.get(
    "/map-overview",
    response_model=MapOverviewResponse,
    summary="Get all prefectures for a single day (D3 Japan Map)",
    description="Returns coordinates, key weather metrics, and initial risk levels for all prefectures on a chosen date."
)
def get_map_overview(
    date: str = Query(..., description="Date formatted as YYYY-MM-DD")
):
    items = weather_service.get_map_overview(date)
    if not items:
        raise HTTPException(
            status_code=404,
            detail=f"No records found for date '{date}'. Please ensure date is within the available forecast window."
        )

    return MapOverviewResponse(
        date=date,
        count=len(items),
        items=[MapOverviewItem(**item) for item in items]
    )
