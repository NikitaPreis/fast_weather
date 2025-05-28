from app.settings.configs.base import BaseConfig


class AppConfig(BaseConfig):
    """App settings."""
    debug: bool = False
    title: str = 'fast-weather'
    description: str = 'Fast Weather.'
    UNKNOWN_ERROR_MESSAGE: str = 'Unknown error.'

    @property
    def cors_middleware_allow_origins(self) -> list[str]:
        return [
            'http://localhost:3000',
        ]

    @property
    def cors_middleware_allow_credentials(self) -> bool:
        return True

    @property
    def cors_middleware_allow_methods(self) -> list[str]:
        return ['GET', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE']

    @property
    def cors_middleware_allow_allow_headers(self) -> list[str]:
        return [
            'Content-Type',
            'Access-Control-Allow-Headers',
            'Access-Control-Allow-Origin',
            'Authorization'
        ]
