from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_weather_forecast_service
from app.exceptions import (CityNotFoundException,
                            FailedRetrieveForecastException)
from app.schemas import CityWeatherForecastSchema
from app.services import WeatherForecastService

router = APIRouter(
    prefix='/weather_forecast', tags=['weather_forecast']
)


@router.get(
    path='/',
    response_model=CityWeatherForecastSchema,
    description='Get weather forecast for the city.'
)
async def get_city_weather_forecast(
    weather_forecast_service: Annotated[
        WeatherForecastService,
        Depends(get_weather_forecast_service)
    ],
    city_name: str = 'Москва',
) -> CityWeatherForecastSchema:
    """Get weather forecast for the city."""
    try:
        return await weather_forecast_service.get_city_weather_forecast(
            city_name=city_name
        )
    except (CityNotFoundException, FailedRetrieveForecastException) as e:
        raise HTTPException(
            detail=e.detail,
            status_code=status.HTTP_404_NOT_FOUND
        )
