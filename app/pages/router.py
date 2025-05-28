from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.handlers.v1.weather_forecast import get_city_weather_forecast

router = APIRouter(
    prefix='/pages',
    tags=['Pages']
)

templates = Jinja2Templates(directory='app/templates')


@router.get('/weather_forecast')
async def get_weather_forecast_page(
    request: Request,
    weather_forecast=Depends(get_city_weather_forecast)
):
    """Page with a list of weather forecast by period."""
    context = {
        'request': request,
        'weather_forecast': weather_forecast
    }
    return templates.TemplateResponse(
        name='weather_forecast.html',
        context=context
    )
