from fastapi import APIRouter, Depends
from starlette import status

from api.dependencies.users import get_active_user
from api.filters.tasks import TaskListQuery
from common import NotFoundException
from db.models import Task, User
from db.repositories.tasks import TasksRepository
from shemas import TaskCreateIn, TaskCreateOut
from shemas.tasks import TaskDetail, TaskUpdate

router = APIRouter()


@router.post("/", summary="Создание задачи", response_model=TaskCreateOut)
async def task_create(
    task: TaskCreateIn, user: User = Depends(get_active_user), task_repo: TasksRepository = Depends()
):
    return await task_repo.create(task.copy(update={"user_id": user.id}))


@router.get("/", summary="Список задач", response_model=list[TaskDetail])
async def task_list(
    filters: TaskListQuery = Depends(), user: User = Depends(get_active_user), task_repo: TasksRepository = Depends()
):
    return await task_repo.filters(user_id=user.id, **filters.dict(exclude_none=True))


@router.get("/filters", summary="Фильтры задач", status_code=status.HTTP_200_OK)
async def get_tasks_filters(user: User = Depends(get_active_user), task_repo: TasksRepository = Depends()):
    return await task_repo.get_filters()


@router.get("/{task_id}", summary="Детализация задачи", response_model=TaskDetail)
async def task_detail(task_id: int, user: User = Depends(get_active_user), task_repo: TasksRepository = Depends()):
    task: Task = await task_repo.get_task_full_data(id=task_id, user_id=user.id)
    if task is None:
        raise NotFoundException(id=task_id)
    return task


@router.delete("/{task_id}", summary="Удаление задачи", status_code=status.HTTP_204_NO_CONTENT)
async def task_delete(task_id: int, user: User = Depends(get_active_user), task_repo: TasksRepository = Depends()):
    params = {"id": task_id}
    if not user.is_superuser:
        params.update(user_id=user.id)
    task: Task | None = await task_repo.get_object(**params)

    if task is None:
        raise NotFoundException(id=task_id)

    await task_repo.delete(id=task_id)


@router.patch("/{task_id}", summary="Обновление задачи", response_model=TaskDetail)
async def task_update(
    task_id: int, task: TaskUpdate, user: User = Depends(get_active_user), task_repo: TasksRepository = Depends()
):
    task_in_db: Task | None = await task_repo.get_object(id=task_id, user_id=user.id)

    if task_in_db is None:
        raise NotFoundException(id=task_id)

    await task_repo.update(filter_params={"id": task_id}, update_values=task.dict(exclude_none=True))
    return task_in_db
