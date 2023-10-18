from datetime import date

from sqlalchemy import and_, func, insert, or_, select
from sqlalchemy.exc import SQLAlchemyError

from app.base_service.base_service import BaseService
from app.bookings.models import Bookings
from app.database import async_session_maker
from app.hotels.models import Rooms
from app.logger import logger


class BookingService(BaseService):
    model = Bookings

    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        try:
            async with async_session_maker() as session:
                booked_rooms = (
                    select(Bookings)
                    .where(
                        and_(
                            Bookings.room_id == 1,
                            or_(
                                and_(
                                    Bookings.date_from >= date_from,
                                    Bookings.date_from <= date_to,
                                ),
                                and_(
                                    Bookings.date_from <= date_from,
                                    Bookings.date_from > date_from,
                                ),
                            ),
                        )
                    )
                    .cte("booked_rooms")
                )

                get_rooms_left = (
                    select(
                        (Rooms.quantity - func.count(booked_rooms.c.room_id)).label(
                            "rooms_left"
                        )
                    )
                    .select_from(Rooms)
                    .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                    .where(Rooms.id == 1)
                    .group_by(Rooms.quantity, booked_rooms.c.room_id)
                )

                # print(rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))
                rooms_left = await session.execute(get_rooms_left)
                rooms_left = rooms_left.scalar_one()
                if int(rooms_left) > 0:
                    get_price = select(Rooms.price).filter_by(id=room_id)
                    price = await session.execute(get_price)
                    price = price.scalars().one()
                    add_booking = (
                        insert(Bookings)
                        .values(
                            room_id=room_id,
                            user_id=user_id,
                            date_from=date_from,
                            date_to=date_to,
                            price=price,
                        )
                        .returning(Bookings)
                    )

                    new_booking = await session.execute(add_booking)
                    await session.commit()
                    return new_booking.scalar_one()
                else:
                    return None
        except (SQLAlchemyError, Exception) as e:
            msg = ''
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc:"
            elif isinstance(e, Exception):
                msg = "Unknown Exc:"
            extra = {
                "user_id": user_id,
                "room_id": room_id,
                "date_from": date_from,
                "date_to": date_to,
            }
            logger.error(msg, extra=extra, exc_info=True)
