"""Open-Meteo/Wheather forecast schemas."""
import datetime as dt

from pydantic import BaseModel


class CityGeocodingSchema(BaseModel):
    """Schema for sending request to external geocoding API."""
    name: str
    count: int = 1
    language: str = 'ru'


class CityCoordinatesSchema(BaseModel):
    """Schema with geographic coordinates of city."""
    name: str
    latitude: float
    longitude: float


class HourlyUnitsSchema(BaseModel):
    """Schema with units for weather forecast."""
    temperature_2m: str
    relative_humidity_2m: str
    rain: str
    snowfall: str
    cloud_cover: str
    visibility: str


class HourlyWeatherSchema(BaseModel):
    """Weather forecast for specific geographic coordinates and datetime."""
    time: dt.datetime
    temperature_2m: float
    relative_humidity_2m: float
    rain: float
    snowfall: float
    cloud_cover: float
    visibility: float


class CityWeatherForecastSchema(BaseModel):
    """City weather forecast for a certain period of time."""
    name: str
    start_date: dt.date
    end_date: dt.date
    hourly_units: HourlyUnitsSchema
    hourly_weather: list[HourlyWeatherSchema]
