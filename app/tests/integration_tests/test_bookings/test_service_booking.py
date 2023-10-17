from datetime import datetime

from app.bookings.service import BookingService


async def test_add_and_get_booking():
    new_booking = await BookingService.add(
        user_id=3,
        room_id=4,
        date_from=datetime.strptime("2023-03-15", "%Y-%m-%d"),
        date_to=datetime.strptime("2023-04-10", "%Y-%m-%d"),
    )

    assert new_booking.id == 7
    assert new_booking.user_id == 3
    assert new_booking.room_id == 4

    new_booking = await BookingService.find_by_id(new_booking.id)

    assert new_booking is not None
