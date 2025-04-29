from fastapi import APIRouter, HTTPException
from prometheus_client import Counter
from typing import List
from fastapi_cache.decorator import cache

from app.schemas import STask
from app.service import TaskService
from app.services.rabbitmq import publish_task

router = APIRouter()

TASKS_CREATED = Counter("tasks_created", "Number of tasks created")
TASKS_DELETED = Counter("tasks_deleted", "Number of tasks deleted")

@router.post("/tasks/")
async def create_new_task(number: int, title: str, description: str) -> STask:
    existing_task = await TaskService.get_by_number(number=number)
    if existing_task:
        raise HTTPException(status_code=400, detail="Task with this number already exists")
    TASKS_CREATED.inc()
    await publish_task(number=number, title=title, description=description)
    return await TaskService.add(number=number, title=title, description=description)

@router.get("/tasks/")
@cache(expire=30)
async def get_all_tasks() -> List[STask]:
    tasks = await TaskService.find_all()
    return tasks

@router.get("/tasks/task")
@cache(expire=30)
async def get_by_number(number: int) -> STask:
    is_existing = await TaskService.get_by_number(number=number)
    if not is_existing:
        raise HTTPException(status_code=404, detail="Task not found")
    return is_existing

@router.delete("/tasks/{task_id}")
async def remove_task(number: int) -> dict[str, str]:
    TASKS_DELETED.inc()
    is_existing = await TaskService.get_by_number(number=number)
    if not is_existing:
        raise HTTPException(status_code=404, detail="Task not found")
    await TaskService.delete(number=number)
    return {"message": f"Task #{number} deleted successfully"}


