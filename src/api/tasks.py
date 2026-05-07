from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.services.task_service import TaskService

router = APIRouter()
task_service = TaskService()


class TaskCreateRequest(BaseModel):
    title: str
    description: str


@router.get("/tasks")
def get_tasks():
    """
    ������� ������ ��� �����
    """
    return list(task_service.tasks.values())


@router.post("/tasks")
def create_task(request: TaskCreateRequest):
    """
    ������� ���� ������
    """
    if not request.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    task = task_service.create_task(
        title=request.title,
        description=request.description
    )
    return task
