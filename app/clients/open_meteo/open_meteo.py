"""Open-Meteo client."""
import datetime as dt
from dataclasses import dataclass

import httpx

from app.exceptions import (CityNotFoundException,
                            FailedRetrieveForecastException,
                            WeatherForecastClientException)
from app.schemas import (CityCoordinatesSchema, CityGeocodingSchema,
                         CityWeatherForecastSchema, HourlyUnitsSchema,
                         HourlyWeatherSchema)
from app.settings import Settings


@dataclass
class OpenMeteoClient:
    """
    Client for receiving weather forecasts.

    Source API: https://open-meteo.com/.
    """
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_forecast(
        self,
        city_coordinates: CityCoordinatesSchema,
        start_date: dt.date = None,
        end_date: dt.date = None
    ) -> CityWeatherForecastSchema:
        """
        Get weather forecast for city by geo coordinates and time period.

        Args:
            1) city_coordinates (pydantic.BaseModel)
            - name: str (City full name);
            - latitude: float (Geocoordinate);
            - longitude: float (Geocoordinate).

            2) start_date: datetime.date
               (Start of the period that limits the selection by date.);
            3) end_date: datetime.date

              (End of the period that limits the selection by date).
        """
        if start_date is None or end_date is None:
            start_date = (dt.datetime.now()).date()
            end_date = (start_date + dt.timedelta(hours=24))

        params = {
            "latitude": city_coordinates.latitude,
            "longitude": city_coordinates.longitude,
            "hourly": [
                "temperature_2m",
                "relative_humidity_2m",
                "rain",
                "snowfall",
                "cloud_cover",
                "visibility"
            ],
            "timezone": "Europe/Moscow",
            "start_date": start_date,
            "end_date": end_date
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=self.settings.open_meteo.forecast_url,
                params=params
            )

        weather_forecast_data = response.json()

        try:
            await self._check_status_code_is_ok(
                status_code=response.status_code
            )
        except WeatherForecastClientException:
            raise FailedRetrieveForecastException

        hourly_units = HourlyUnitsSchema(
            **weather_forecast_data['hourly_units']
        )

        hourly_weather_schema_list: list[HourlyWeatherSchema] = (
            self._get_hourly_weather_list(
                hourly_data=weather_forecast_data['hourly']
            )
        )

        return CityWeatherForecastSchema(
            name=city_coordinates.name,
            start_date=start_date,
            end_date=end_date,
            hourly_units=hourly_units,
            hourly_weather=hourly_weather_schema_list
        )

    async def get_city_geo_cordinates(
        self,
        city_name: str
    ) -> CityCoordinatesSchema:
        """Get city geo cordinates by name."""

        geocoding_request_schema = CityGeocodingSchema(
            name=city_name
        )

        params = {
            'name': geocoding_request_schema.name,
            'count': geocoding_request_schema.count,
            'language': geocoding_request_schema.language
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=self.settings.open_meteo.geocoding_search_url,
                params=params
            )

        try:
            await self._check_status_code_is_ok(
                status_code=response.status_code
            )

            city_data: dict[str, str | float] = response.json()['results'][0]
            return CityCoordinatesSchema(
                name=city_name,
                latitude=city_data['latitude'],
                longitude=city_data['longitude']
            )
        except WeatherForecastClientException:
            raise CityNotFoundException

    def _get_hourly_weather_list(
        self,
        hourly_data: dict[str, str | float | int | list]
    ) -> list[HourlyWeatherSchema]:
        """
        Create list with hourly weather data objects.

        Collect the data into a list of objects,
        so each object contains all the information that
        describes the weather at a specific point in time.
        """

        hourly_weather_schema_list = []

        for i in range(0, len(hourly_data['time'])):
            hourly_weather_schema = HourlyWeatherSchema(
                time=hourly_data['time'][i],  # time_list
                temperature_2m=hourly_data.get(
                    'temperature_2m'
                )[i],  # temperature_list
                relative_humidity_2m=hourly_data.get(
                    'relative_humidity_2m'
                )[i],  # humidity_list
                rain=hourly_data['rain'][i],  # rain_list
                snowfall=hourly_data['snowfall'][i],  # snowfall_list
                cloud_cover=hourly_data['cloud_cover'][i],  # cloud_cover_list
                visibility=hourly_data['visibility'][i]  # visibility_list
            )
            hourly_weather_schema_list.append(hourly_weather_schema)

        return hourly_weather_schema_list

    async def _check_status_code_is_ok(
        self,
        status_code: str
    ) -> None:
        """Check that status code is ok."""
        if status_code != httpx.codes.OK:
            raise WeatherForecastClientException
