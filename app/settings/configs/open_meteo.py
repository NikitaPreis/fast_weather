from app.settings.configs.base import BaseConfig


class OpenMeteoConfig(BaseConfig):
    """
    Open-Meteo API client settings.
    """
    OPEN_METEO_URL: str = 'https://api.open-meteo.com/'
    GEOCODING_URL: str = 'https://geocoding-api.open-meteo.com/'

    @property
    def forecast_url(self):
        """Url for weather forecast endpoints."""
        return f'{self.OPEN_METEO_URL}v1/forecast'

    @property
    def geocoding_search_url(self):
        """Url for geocoding endpoints."""
        return f'{self.GEOCODING_URL}v1/search?'
