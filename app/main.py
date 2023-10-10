from datetime import date

from fastapi import FastAPI, Query, Depends
from typing import Optional
from pydantic import BaseModel
from app.bookings.router import router as router_bookings
from app.users.router import router as router_users
from app.pages.router import router as router_page
from app.hotels.router import router as router_hotels

app = FastAPI()

app.include_router(router_bookings)
app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_page)



