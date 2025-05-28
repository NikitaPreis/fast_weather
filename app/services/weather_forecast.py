from dataclasses import dataclass

from app.clients import OpenMeteoClient
from app.schemas import (CityCoordinatesSchema, CityWeatherForecastSchema)


@dataclass
class WeatherForecastService:
    forecast_client: OpenMeteoClient

    async def get_city_weather_forecast(
        self, city_name: str
    ) -> CityWeatherForecastSchema:
        """Get weather forecast for the city."""
        city_coordinates: CityCoordinatesSchema = (
            await self.forecast_client.get_city_geo_cordinates(
                city_name=city_name
            )
        )

        weather_forecast: CityWeatherForecastSchema = (
            await self.forecast_client.get_forecast(
                city_coordinates=city_coordinates
            )
        )

        return weather_forecast
