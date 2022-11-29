from fastapi import APIRouter, Depends
from starlette import status

from api.dependencies.users import get_active_user, get_superuser
from common import BadRequestException, NotFoundException
from db.models import Category, User
from db.repositories.categories import CategoriesRepository
from shemas import CategoryCreate, CategoryDetail

router = APIRouter()


@router.get("/", summary="Список категорий", response_model=list[CategoryDetail])
async def categories_list(
    cat_repo: CategoriesRepository = Depends(),
    user: User = Depends(get_active_user),
):
    return await cat_repo.filters()


@router.post("/", summary="Создание категории", response_model=CategoryDetail)
async def category_create(
    category: CategoryCreate,
    cat_repo: CategoriesRepository = Depends(),
    user: User = Depends(get_active_user),
):
    category_check: Category | None = await cat_repo.get_object(name=category.name)
    if category_check is not None:
        raise BadRequestException(detail="Категория с таким именем уже существует")
    return await cat_repo.create(category)


@router.get("/{category_id}", summary="Детализация категории", response_model=CategoryDetail)
async def category_detail(
    category_id: int,
    cat_repo: CategoriesRepository = Depends(),
    user: User = Depends(get_active_user),
):
    category: Category | None = await cat_repo.get_object(id=category_id)
    if category is None:
        raise NotFoundException(id=category_id)
    return category


@router.delete("/{category_id}", summary="Удаление категории", status_code=status.HTTP_204_NO_CONTENT)
async def category_delete(
    category_id: int, cat_repo: CategoriesRepository = Depends(), user: User = Depends(get_superuser)
):
    await cat_repo.delete(id=category_id)
