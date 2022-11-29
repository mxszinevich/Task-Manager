import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from db.models import Category
from db.repositories.categories import CategoriesRepository


@pytest.mark.asyncio
class TestCategoriesRoutes:
    async def test_create(self, test_cred_client: AsyncSession):
        data = {"name": "Категория1"}
        res = await test_cred_client.post("categories/", json=data)
        assert res.status_code == status.HTTP_200_OK
        res_json = res.json()
        assert res_json["name"] == "Категория1"
        assert res_json["id"]

    async def test_list(self, test_cred_client: AsyncSession, categories_generating):
        categories: list[Category] = await categories_generating(n=3)
        res = await test_cred_client.get("categories/")
        assert res.status_code == status.HTTP_200_OK
        assert res.json() == [
            {
                "name": category.name,
                "id": category.id,
            }
            for category in categories
        ]

    async def test_detail(self, test_cred_client: AsyncSession, category):
        res = await test_cred_client.get(f"/categories/{category.id}")
        assert res.status_code == status.HTTP_200_OK
        assert res.json() == {
            "name": category.name,
            "id": category.id,
        }

    async def test_delete(self, test_client, access_token, super_user, user_active, category, override_get_db_session):
        token_data = access_token(user_id=user_active.id)
        res = await test_client.delete(
            f"categories/{category.id}", headers={"Authorization": f"{token_data.type} {token_data.access_token}"}
        )
        assert res.status_code == status.HTTP_403_FORBIDDEN

        async for session in override_get_db_session():
            categories_repo = CategoriesRepository(session=session)
            assert (await categories_repo.count()) == 1

        token_data = access_token(user_id=super_user.id)
        res = await test_client.delete(
            f"categories/{category.id}", headers={"Authorization": f"{token_data.type} {token_data.access_token}"}
        )
        assert res.status_code == status.HTTP_204_NO_CONTENT

        async for session in override_get_db_session():
            categories_repo = CategoriesRepository(session=session)
            assert (await categories_repo.count()) == 0
