from typing import Union

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from app.hotels.router import get_all_hotels

router = APIRouter(
    prefix='/pages',
    tags=["Страницы"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get('/hotels')
async def get_hotels_page(
        request: Request,
        hotels: Union[list, None] = Depends(get_all_hotels)
):
    return templates.TemplateResponse(name='hotels.html', context={"request": request, "hotels": hotels})
