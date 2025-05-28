import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    """Base settings."""
    ENV_FILE: str = '.env'

    # Get base dir of project.
    BASE_DIR: str = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '...')
    )

    # Set env_file for project.
    model_config = SettingsConfigDict(
        env_file=f"{BASE_DIR}/{ENV_FILE}",
        extra='ignore',
        env_file_encoding='utf-8'
    )
