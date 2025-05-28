from typing import Annotated

import httpx
from fastapi import Depends

from app.clients import OpenMeteoClient
from app.services import WeatherForecastService
from app.settings import Settings


def get_settings() -> Settings:
    """Get app settings (config)."""
    return Settings.load()


async def get_async_client() -> httpx.AsyncClient:
    """Get async client."""
    return httpx.AsyncClient()


async def get_forecast_client(
    async_client: Annotated[httpx.AsyncClient, Depends(get_async_client)],
    settings: Annotated[Settings, Depends(get_settings)]
) -> OpenMeteoClient:
    """Get weather forecast client."""
    return OpenMeteoClient(settings=settings, async_client=async_client)


async def get_weather_forecast_service(
    forecast_client: Annotated[OpenMeteoClient, Depends(get_forecast_client)]
) -> WeatherForecastService:
    """Get weather forecast service."""
    return WeatherForecastService(forecast_client=forecast_client)
