import pytest

from app.users.service import UserService


@pytest.mark.parametrize('user_id,email,exists', [
    (1, "fedor@moloko.ru", True),
    (2, "sharik@moloko.ru", True),
    (22, "", False),
])
async def test_find_user_by_id(user_id, email, exists):
    user = await UserService.find_by_id(user_id)

    if exists:
        assert user
        assert user.email == email
        assert user.id == user_id
    else:
        assert not user
