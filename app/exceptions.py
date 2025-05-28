"""Exceptions."""


class CityNotFoundException(Exception):
    detail = 'City is not found.'


class FailedRetrieveForecastException(Exception):
    detail = 'Failed to retrieve weather forecast for the city.'


class WeatherForecastClientException(Exception):
    detail = 'Failed to retrieve weather forecast from external source.'
