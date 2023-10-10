from typing import List

from fastapi import APIRouter
from app.hotels.service import HotelsService
from app.hotels.schemas import SHotels

router = APIRouter(
    prefix="/hotel",
    tags=['Hotels']
)


@router.get("")
async def get_all_hotels() -> List[SHotels]:
    hotels = await HotelsService.find_all()
    return hotels
