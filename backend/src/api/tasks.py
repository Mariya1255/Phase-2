from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from uuid import UUID
from ..database.database import get_session
from ..middleware.auth_middleware import get_current_user, get_user_id_from_token
from ..models.task import Task, TaskCreate, TaskCreateRequest, TaskUpdate, TaskResponse, TaskStatus
from ..services.task_service import (
    create_task,
    get_tasks_by_user,
    get_task_by_id_and_user,
    update_task_by_user,
    delete_task_by_user,
    get_task_count_by_user
)

router = APIRouter()

@router.post("/", response_model=TaskResponse)
def create_user_task(
    task_request: TaskCreateRequest,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user
    """
    try:
        # Extract user_id from JWT token
        user_id = UUID(current_user["user_id"])

        # Create TaskCreate object with user_id from token
        task_create = TaskCreate(
            title=task_request.title,
            description=task_request.description,
            status=task_request.status or TaskStatus.PENDING,
            user_id=user_id
        )

        task = create_task(session, task_create)
        return task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the task: {str(e)}"
        )

@router.get("/", response_model=List[TaskResponse])
def get_user_tasks(
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user
    """
    try:
        user_id = UUID(current_user["user_id"])
        tasks = get_tasks_by_user(session, user_id)
        return tasks
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving tasks: {str(e)}"
        )

@router.get("/{task_id}", response_model=TaskResponse)
def get_user_task(
    task_id: UUID,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task for the authenticated user
    """
    try:
        user_id = UUID(current_user["user_id"])
        task = get_task_by_id_and_user(session, task_id, user_id)

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or not authorized"
            )

        return task
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving the task: {str(e)}"
        )

@router.put("/{task_id}", response_model=TaskResponse)
def update_user_task(
    task_id: UUID,
    task_update: TaskUpdate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task for the authenticated user
    """
    try:
        user_id = UUID(current_user["user_id"])
        task = update_task_by_user(session, task_id, user_id, task_update)

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or not authorized"
            )

        return task
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format or update data"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the task: {str(e)}"
        )

@router.delete("/{task_id}")
def delete_user_task(
    task_id: UUID,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task for the authenticated user
    """
    try:
        user_id = UUID(current_user["user_id"])
        success = delete_task_by_user(session, task_id, user_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or not authorized"
            )

        return {"message": "Task deleted successfully"}
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting the task: {str(e)}"
        )

@router.get("/stats")
def get_user_task_stats(
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get statistics about tasks for the authenticated user
    """
    try:
        user_id = UUID(current_user["user_id"])
        count = get_task_count_by_user(session, user_id)

        return {
            "user_id": str(user_id),
            "task_count": count
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving task stats: {str(e)}"
        )