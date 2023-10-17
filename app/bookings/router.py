from datetime import date
from typing import List

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from app.bookings.schemas import SBookings
from app.bookings.service import BookingService
from app.exceptions import RoomCannotBeBookException
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("", response_model=List[SBookings])
async def get_bookings(user: Users = Depends(get_current_user)) -> List[SBookings]:
    return await BookingService.find_all(user_id=user.id)


@router.post("")
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
):
    booking = await BookingService.add(
        user_id=user.id, room_id=room_id, date_from=date_from, date_to=date_to
    )
    if not booking:
        raise RoomCannotBeBookException
    booking_dict1 = jsonable_encoder(booking)

    send_booking_confirmation_email.delay(booking_dict1, user.email)
    return booking
