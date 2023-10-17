from datetime import datetime
from typing import Union

from fastapi import Depends, Request
from jose import JWTError, jwt

from app.config import settings
from app.exceptions import (
    InvalidTokenFormatException,
    TokenAbsentException,
    TokenExpiredException,
    UserIsNotPresentException,
)
from app.users.service import UserService


def get_token(request: Request):
    token = request.cookies.get('booking_access_token')
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise InvalidTokenFormatException

    expire: Union[str, None] = payload.get('exp')
    if (not expire) or (int(expire) < int(datetime.utcnow().timestamp())):
        raise TokenExpiredException
    user_id_str: Union[str, None] = payload.get('sub')
    user_id: Union[int, None] = int(user_id_str) if user_id_str else None
    if not user_id:
        raise UserIsNotPresentException
    user = await UserService.find_one_or_none(id=user_id)
    if not user:
        raise UserIsNotPresentException
    return user
