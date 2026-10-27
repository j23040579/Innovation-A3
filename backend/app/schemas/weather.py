from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class PrefectureInfo(BaseModel):
    prefecture: str
    towns: List[str]

class MetadataPrefecturesResponse(BaseModel):
    count: int
    prefectures: List[PrefectureInfo]

class MetadataDateRangeResponse(BaseModel):
    min_date: str
    max_date: str
    total_days: int

class DailyWeatherMetrics(BaseModel):
    temperature_2m_max: Optional[float] = None
    temperature_2m_min: Optional[float] = None
    temperature_2m_mean: Optional[float] = None
    wind_speed_10m_max: Optional[float] = None
    wind_speed_10m_min: Optional[float] = None
    wind_speed_10m_mean: Optional[float] = None
    wind_gusts_10m_max: Optional[float] = None
    wind_gusts_10m_mean: Optional[float] = None
    wind_direction_10m_dominant: Optional[float] = None
    snowfall_sum: Optional[float] = None
    rain_sum: Optional[float] = None
    precipitation_sum: Optional[float] = None
    precipitation_hours: Optional[float] = None
    relative_humidity_2m_mean: Optional[float] = None
    relative_humidity_2m_max: Optional[float] = None
    relative_humidity_2m_min: Optional[float] = None
    dew_point_2m_mean: Optional[float] = None
    dew_point_2m_max: Optional[float] = None
    dew_point_2m_min: Optional[float] = None
    surface_pressure_mean: Optional[float] = None
    surface_pressure_max: Optional[float] = None
    surface_pressure_min: Optional[float] = None
    pressure_msl_mean: Optional[float] = None
    pressure_msl_max: Optional[float] = None
    pressure_msl_min: Optional[float] = None
    pressure_change: Optional[float] = None
    cloud_cover_mean: Optional[float] = None
    cloud_cover_max: Optional[float] = None
    cloud_cover_min: Optional[float] = None
    shortwave_radiation_sum: Optional[float] = None
    sunshine_duration: Optional[float] = None
    daylight_duration: Optional[float] = None
    river_discharge: Optional[float] = None
    river_discharge_mean: Optional[float] = None
    river_discharge_max: Optional[float] = None
    elevation: Optional[float] = None

class DailyWeatherResponse(BaseModel):
    prefecture: str
    town: Optional[str] = None
    date: str
    is_prefecture_average: bool = False
    metrics: Dict[str, Any]

class TimeSeriesDataPoint(BaseModel):
    date: str
    temperature_max: Optional[float] = None
    temperature_min: Optional[float] = None
    temperature_mean: Optional[float] = None
    rain_sum: Optional[float] = None
    precipitation_sum: Optional[float] = None
    snowfall_sum: Optional[float] = None
    wind_speed_max: Optional[float] = None
    wind_gusts_max: Optional[float] = None
    relative_humidity_mean: Optional[float] = None
    surface_pressure_mean: Optional[float] = None
    cloud_cover_mean: Optional[float] = None
    river_discharge: Optional[float] = None

class TimeSeriesResponse(BaseModel):
    prefecture: str
    town: Optional[str] = None
    start_date: str
    end_date: str
    total_data_points: int
    series: List[TimeSeriesDataPoint]

class MapOverviewItem(BaseModel):
    prefecture: str
    date: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    temperature_mean: Optional[float] = None
    rain_sum: Optional[float] = None
    snowfall_sum: Optional[float] = None
    wind_speed_max: Optional[float] = None
    primary_risk_level: Optional[str] = "Low"  # Low, Medium, High

class MapOverviewResponse(BaseModel):
    date: str
    count: int
    items: List[MapOverviewItem]
