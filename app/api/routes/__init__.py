from fastapi import APIRouter

from .auth import router as auth_router
from .categories import router as categories_router
from .tasks import router as tasks_router
from .users import router as users_router

router = APIRouter()


router.include_router(users_router, prefix="/users", tags=["Users"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
router.include_router(categories_router, prefix="/categories", tags=["Categories"])
