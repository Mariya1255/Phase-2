from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from uuid import UUID

from backend.src.database.database import get_session
from backend.src.middleware.auth_middleware import get_user_id_from_token
from backend.src.models.todo import Todo, TodoCreate, TodoUpdate, TodoResponse
from backend.src.services.todo_service import (
    create_todo, get_todos_by_user, get_todo_by_id_and_user,
    update_todo_by_id_and_user, delete_todo_by_id_and_user, toggle_todo_completion
)

router = APIRouter()


@router.get("/", response_model=List[TodoResponse])
def get_todos(
    current_user_id: str = Depends(get_user_id_from_token),
    session: Session = Depends(get_session)
):
    """
    Get all todos for the authenticated user
    """
    user_id = UUID(current_user_id)
    todos = get_todos_by_user(session, user_id)
    return todos


@router.post("/", response_model=TodoResponse)
def create_todo_endpoint(
    todo: TodoCreate,
    current_user_id: str = Depends(get_user_id_from_token),
    session: Session = Depends(get_session)
):
    """
    Create a new todo for the authenticated user
    """
    user_id = UUID(current_user_id)
    db_todo = create_todo(session, todo, user_id)
    return db_todo


@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(
    todo_id: UUID,
    current_user_id: str = Depends(get_user_id_from_token),
    session: Session = Depends(get_session)
):
    """
    Get a specific todo by ID for the authenticated user
    """
    user_id = UUID(current_user_id)
    db_todo = get_todo_by_id_and_user(session, todo_id, user_id)

    if db_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found or does not belong to user"
        )

    return db_todo


@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: UUID,
    todo_update: TodoUpdate,
    current_user_id: str = Depends(get_user_id_from_token),
    session: Session = Depends(get_session)
):
    """
    Update a specific todo by ID for the authenticated user
    """
    user_id = UUID(current_user_id)
    db_todo = update_todo_by_id_and_user(session, todo_id, user_id, todo_update)

    if db_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found or does not belong to user"
        )

    return db_todo


@router.patch("/{todo_id}/complete")
def update_todo_completion(
    todo_id: UUID,
    completed: bool,
    current_user_id: str = Depends(get_user_id_from_token),
    session: Session = Depends(get_session)
):
    """
    Toggle completion status of a specific todo for the authenticated user
    """
    user_id = UUID(current_user_id)
    db_todo = toggle_todo_completion(session, todo_id, user_id, completed)

    if db_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found or does not belong to user"
        )

    return {"todo": {"id": str(db_todo.id), "completed": db_todo.completed, "updated_at": db_todo.updated_at}}


@router.delete("/{todo_id}")
def delete_todo(
    todo_id: UUID,
    current_user_id: str = Depends(get_user_id_from_token),
    session: Session = Depends(get_session)
):
    """
    Delete a specific todo by ID for the authenticated user
    """
    user_id = UUID(current_user_id)
    success = delete_todo_by_id_and_user(session, todo_id, user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found or does not belong to user"
        )

    return {"success": True}