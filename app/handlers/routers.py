from fastapi import APIRouter

from app.handlers.v1 import weather_forecast_router

v1_router = APIRouter(prefix='/api/v1')
v1_router.include_router(weather_forecast_router)
