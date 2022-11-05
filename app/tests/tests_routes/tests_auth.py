import pytest
from starlette import status

from db.models import User

pytestmark = pytest.mark.asyncio


async def test_get_access_token(test_client, user_registration_data: dict, user_active_in_db: User):
    user_registration_data = user_registration_data()

    data = {
        "email": user_registration_data["email"],
        "password": user_registration_data["password"],
    }
    res = await test_client.post("auth/", json=data)
    assert res.status_code == status.HTTP_200_OK
    res_json = res.json()
    assert "access_token" in res_json
    assert res_json["type"] == "Bearer"


async def test_get_access_token_with_invalid_data(test_client, user_registration_data, user_active_in_db: User):
    user_registration_data = user_registration_data()
    data = {
        "email": user_registration_data["email"],
        "password": "invalid_password",
    }
    res = await test_client.post("auth/", json=data)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
    assert res.json() == {"detail": "Неверный пароль"}

    data = {
        "email": "test@test.com",
        "password": user_registration_data["password"],
    }
    res = await test_client.post("auth/", json=data)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
    assert res.json() == {"detail": "Неверный email"}
