from sqlmodel import Session, select
from ..models.todo import Todo, TodoCreate, TodoUpdate
from ..models.user import User
from typing import List, Optional
from uuid import UUID


def create_todo(session: Session, todo: TodoCreate, user_id: UUID) -> Todo:
    """
    Create a new todo for the specified user
    """
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        user_id=user_id
    )

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


def get_todos_by_user(session: Session, user_id: UUID) -> List[Todo]:
    """
    Get all todos for a specific user
    """
    statement = select(Todo).where(Todo.user_id == user_id)
    results = session.exec(statement)
    return results.all()


def get_todo_by_id_and_user(session: Session, todo_id: UUID, user_id: UUID) -> Optional[Todo]:
    """
    Get a specific todo by its ID and ensure it belongs to the user
    """
    statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    result = session.exec(statement).first()
    return result


def update_todo_by_id_and_user(session: Session, todo_id: UUID, user_id: UUID, todo_update: TodoUpdate) -> Optional[Todo]:
    """
    Update a specific todo by its ID if it belongs to the user
    """
    db_todo = get_todo_by_id_and_user(session, todo_id, user_id)

    if db_todo is None:
        return None

    # Update the todo with provided fields
    update_data = todo_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_todo, field, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


def delete_todo_by_id_and_user(session: Session, todo_id: UUID, user_id: UUID) -> bool:
    """
    Delete a specific todo by its ID if it belongs to the user
    """
    db_todo = get_todo_by_id_and_user(session, todo_id, user_id)

    if db_todo is None:
        return False

    session.delete(db_todo)
    session.commit()

    return True


def toggle_todo_completion(session: Session, todo_id: UUID, user_id: UUID, completed: bool) -> Optional[Todo]:
    """
    Toggle the completion status of a specific todo if it belongs to the user
    """
    db_todo = get_todo_by_id_and_user(session, todo_id, user_id)

    if db_todo is None:
        return None

    db_todo.completed = completed
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo