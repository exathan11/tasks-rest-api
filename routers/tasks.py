from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import Response

from ..models.schemas import TaskCreate, TaskResponse, TaskUpdate
from ..services.taskService import TaskService


def get_task_service():
    task_service = TaskService()
    return task_service


router = APIRouter(tags=["tasks"], dependencies=[Depends(get_task_service)])


@router.get("/tasks", response_model=list[TaskResponse])
def get_tasks(
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> list[TaskResponse]:
    found_tasks = task_service.get_tasks()
    res = [
        TaskResponse(id=task.id, name=task.name, status=task.status)
        for task in found_tasks
    ]

    return res


@router.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
def add_task(
    task_create: TaskCreate,
    task_service: Annotated[TaskService, Depends(get_task_service)],
):
    created_task = task_service.add_task(task_create.name)
    res_task = TaskResponse(
        id=created_task.id, name=created_task.name, status=created_task.status
    )

    return res_task


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task_by_id(
    task_id: int, task_service: Annotated[TaskService, Depends(get_task_service)]
):
    found_task = task_service.get_task_by_id(task_id=task_id)
    if found_task is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"A task with id {task_id} was not found"
        )

    res_task = TaskResponse(
        id=found_task.id, name=found_task.name, status=found_task.status
    )

    return res_task


@router.put(
    "/tasks/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskResponse
)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    response: Response,
    task_service: Annotated[TaskService, Depends(get_task_service)],
):
    task_updated, updated_task = task_service.update_task(
        id=task_id, name=task_update.name, status=task_update.status
    )

    if task_updated is None:
        response.status_code = status.HTTP_201_CREATED

    res_task = TaskResponse(
        id=updated_task.id, name=updated_task.name, status=updated_task.status
    )
    return res_task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    response: Response,
    task_service: Annotated[TaskService, Depends(get_task_service)],
):
    if not task_service.delete_task(task_id):
        response.status_code = status.HTTP_404_NOT_FOUND

    return
