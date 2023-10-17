import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("email,password,status_code", [
    ("kot@pes.com", "testPass", 200),
    ("kot@pes.com", "2121", 409),
    ("pes@pes.com", "321321", 200),
    ("dsadsadas", "fdsfds", 422),
    ("", "", 422),
])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": email,
        "password": password
    })

    assert response.status_code == status_code


@pytest.mark.parametrize("email,password,status_code", [
    ("test@test.ru", "test", 200),
    ("fedor@moloko.ru", "hashed_password", 200),
    ("fedor4@moloko.ru", "hashed_password", 403),
    ("", "", 422),
    ("fds@dsadsa.com", "", 403),

])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/login", json={
        "email": email,
        "password": password
    })
    assert response.status_code == status_code
