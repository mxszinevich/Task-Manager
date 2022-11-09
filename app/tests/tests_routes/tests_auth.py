import pytest
from starlette import status

pytestmark = pytest.mark.asyncio


async def test_get_access_token(test_client, user_factory):
    user = await user_factory(password="password")
    data = {
        "email": user.email,
        "password": "password",
    }
    res = await test_client.post("auth/", json=data)
    assert res.status_code == status.HTTP_200_OK
    res_json = res.json()
    assert "access_token" in res_json
    assert res_json["type"] == "Bearer"


async def test_get_access_token_with_invalid_data(test_client, user_factory):
    user = await user_factory(is_active=True, password="password")
    data = {
        "email": user.email,
        "password": "invalid_password",
    }
    res = await test_client.post("auth/", json=data)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
    assert res.json() == {"detail": "Неверный пароль"}

    data = {
        "email": "test@test.com",
        "password": "password",
    }
    res = await test_client.post("auth/", json=data)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
    assert res.json() == {"detail": "Неверный email"}
