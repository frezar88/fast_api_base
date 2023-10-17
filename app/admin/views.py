from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels, Rooms
from app.users.models import Users


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email, Users.booking]
    column_details_exclude_list = [Users.hashed_password]
    form_excluded_columns = [Users.booking]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.c] + [
        Bookings.user,
        Bookings.room,
    ]
    name = "Бронь"
    name_plural = "Брони"
    icon = "fa-regular fa-handshake"
    form_excluded_columns = [Bookings.user, Bookings.room]


class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.c]
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"
    form_excluded_columns = [Hotels.room]


class RoomsAdmin(ModelView, model=Rooms):
    column_list = [c.name for c in Rooms.__table__.c] + [Rooms.hotel]
    name = "Комната"
    name_plural = "Комнаты"
    icon = "fa-solid fa-bed"
    form_excluded_columns = [Rooms.hotel, Rooms.booking]
