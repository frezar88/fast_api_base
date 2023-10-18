import time
from typing import List

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.hotels.schemas import SHotels
from app.hotels.service import HotelsService

from fastapi_versioning import version

router = APIRouter(
    prefix="/hotel",
    tags=['Hotels']
)


@router.get("")
# @version(1)
@cache(expire=60)
async def get_all_hotels() -> List[SHotels]:
    time.sleep(5)
    hotels = await HotelsService.find_all()
    return hotels


