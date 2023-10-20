import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code,registration",
    [
        (5, "2030-05-01", "2030-05-15", 200, 1),
        (5, "2030-05-01", "2030-05-15", 200, 2),
        (5, "2030-05-01", "2030-05-15", 200, 3),
        (5, "2030-05-01", "2030-05-15", 200, 4),
    ],
)
async def test_test_add_and_get_booking(
    room_id,
    date_from,
    date_to,
    status_code,
    registration,
    authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.post(
        "v1/bookings",
        params={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    assert response.status_code == status_code

    response = await authenticated_ac.get("v1/bookings")

    assert len(response.json()) == registration
