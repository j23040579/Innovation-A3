from fastapi import APIRouter, HTTPException
from app.schemas.weather import MetadataPrefecturesResponse, MetadataDateRangeResponse, PrefectureInfo
from app.services.weather_query_service import weather_service

router = APIRouter(prefix="/metadata", tags=["Metadata"])

@router.get(
    "/prefectures",
    response_model=MetadataPrefecturesResponse,
    summary="List all supported Japan prefectures and towns",
    description="Returns all 59 prefecture regions and their available town observation locations from the dataset."
)
def get_prefectures():
    pref_map = weather_service.get_prefectures_and_towns()
    prefectures_list = [
        PrefectureInfo(prefecture=pref, towns=towns)
        for pref, towns in sorted(pref_map.items())
    ]
    return MetadataPrefecturesResponse(
        count=len(prefectures_list),
        prefectures=prefectures_list
    )

@router.get(
    "/date-range",
    response_model=MetadataDateRangeResponse,
    summary="Get valid forecast date bounds",
    description="Returns the earliest and latest available date strings (YYYY-MM-DD) for prediction queries."
)
def get_date_range():
    min_date, max_date, total_days = weather_service.get_date_range()
    return MetadataDateRangeResponse(
        min_date=min_date,
        max_date=max_date,
        total_days=total_days
    )
