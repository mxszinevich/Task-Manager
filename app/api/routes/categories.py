from fastapi import APIRouter, Depends

from api.dependencies.users import get_active_user
from common import BadRequestException, NotFoundException
from db.models import Category, User
from db.repositories.categories import CategoriesRepository
from shemas import CategoryCreate, CategoryDetail

router = APIRouter()


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
