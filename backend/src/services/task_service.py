from sqlmodel import Session, select
from typing import List, Optional
from ..models.task import Task, TaskCreate, TaskUpdate, TaskResponse
from ..models.user import User
from ..logging import log_auth_event
from uuid import UUID

def create_task(session: Session, task_create: TaskCreate) -> Task:
    """
    Create a new task for a user
    """
    # Verify that the user exists
    user_statement = select(User).where(User.id == task_create.user_id)
    user = session.exec(user_statement).first()

    if not user:
        # Log failed task creation attempt
        log_auth_event(
            event_type='failed_task_creation',
            user_id=str(task_create.user_id),
            email=getattr(user, 'email', 'unknown'),
            success=False,
            details={'reason': 'user_not_found'}
        )
        raise ValueError("User not found")

    # Create the task
    task = Task.from_orm(task_create) if hasattr(Task, 'from_orm') else Task(**task_create.dict())

    session.add(task)
    session.commit()
    session.refresh(task)

    # Log successful task creation
    log_auth_event(
        event_type='task_created',
        user_id=str(task_create.user_id),
        email=user.email,
        success=True,
        details={'task_id': str(task.id), 'task_title': task.title}
    )

    return task

def get_tasks_by_user(session: Session, user_id: UUID) -> List[Task]:
    """
    Get all tasks for a specific user
    """
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()

    # Log successful task retrieval
    log_auth_event(
        event_type='tasks_retrieved',
        user_id=str(user_id),
        success=True,
        details={'task_count': len(tasks)}
    )

    return tasks

def get_task_by_id_and_user(session: Session, task_id: UUID, user_id: UUID) -> Optional[Task]:
    """
    Get a specific task for a specific user (enforces user isolation)
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    # Log task retrieval attempt
    if task:
        log_auth_event(
            event_type='task_retrieved',
            user_id=str(user_id),
            success=True,
            details={'task_id': str(task_id)}
        )
    else:
        log_auth_event(
            event_type='task_access_denied',
            user_id=str(user_id),
            success=False,
            details={'task_id': str(task_id), 'reason': 'not_found_or_unauthorized'}
        )

    return task

def update_task_by_user(session: Session, task_id: UUID, user_id: UUID, task_update: TaskUpdate) -> Optional[Task]:
    """
    Update a task for a specific user (enforces user isolation)
    """
    task = get_task_by_id_and_user(session, task_id, user_id)

    if not task:
        # Log failed update attempt
        log_auth_event(
            event_type='task_update_failed',
            user_id=str(user_id),
            success=False,
            details={'task_id': str(task_id), 'reason': 'not_found_or_unauthorized'}
        )
        return None

    # Update the task with provided values
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    session.add(task)
    session.commit()
    session.refresh(task)

    # Log successful update
    log_auth_event(
        event_type='task_updated',
        user_id=str(user_id),
        success=True,
        details={'task_id': str(task_id), 'updates': list(update_data.keys())}
    )

    return task

def delete_task_by_user(session: Session, task_id: UUID, user_id: UUID) -> bool:
    """
    Delete a task for a specific user (enforces user isolation)
    """
    task = get_task_by_id_and_user(session, task_id, user_id)

    if not task:
        # Log failed deletion attempt
        log_auth_event(
            event_type='task_deletion_failed',
            user_id=str(user_id),
            success=False,
            details={'task_id': str(task_id), 'reason': 'not_found_or_unauthorized'}
        )
        return False

    session.delete(task)
    session.commit()

    # Log successful deletion
    log_auth_event(
        event_type='task_deleted',
        user_id=str(user_id),
        success=True,
        details={'task_id': str(task_id), 'task_title': task.title}
    )

    return True

def get_task_count_by_user(session: Session, user_id: UUID) -> int:
    """
    Get the total number of tasks for a specific user
    """
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()

    # Log successful count retrieval
    log_auth_event(
        event_type='task_count_retrieved',
        user_id=str(user_id),
        success=True,
        details={'task_count': len(tasks)}
    )

    return len(tasks)