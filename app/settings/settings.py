from pydantic import Field
from pydantic_settings import BaseSettings

from app.settings.configs import AppConfig, OpenMeteoConfig


class Settings(BaseSettings):
    """Main settings."""
    app: AppConfig = Field(default_factory=AppConfig)
    open_meteo: OpenMeteoConfig = Field(default_factory=OpenMeteoConfig)

    @classmethod
    def load(cls) -> 'Settings':
        return cls()
