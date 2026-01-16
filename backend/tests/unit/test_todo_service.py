import pytest
from sqlmodel import Session
from unittest.mock import Mock, MagicMock
from uuid import UUID, uuid4
from backend.src.services.todo_service import (
    create_todo, get_todos_by_user, get_todo_by_id_and_user,
    update_todo_by_id_and_user, delete_todo_by_id_and_user, toggle_todo_completion
)
from backend.src.models.todo import Todo, TodoCreate, TodoUpdate


def test_create_todo_success():
    """Test successful todo creation"""
    # Mock session
    mock_session = Mock(spec=Session)

    # Mock todo creation
    todo_create = TodoCreate(
        title="Test Todo",
        description="Test Description",
        completed=False
    )

    user_id = uuid4()

    # Call the function
    result = create_todo(mock_session, todo_create, user_id)

    # Verify the todo was created with the correct attributes
    assert result.title == "Test Todo"
    assert result.description == "Test Description"
    assert result.completed == False
    assert result.user_id == user_id

    # Verify session methods were called
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()


def test_get_todos_by_user():
    """Test getting todos by user"""
    # Mock session
    mock_session = Mock(spec=Session)

    # Mock todo objects
    mock_todo1 = Todo(
        id=uuid4(),
        title="Todo 1",
        description="Description 1",
        completed=False,
        user_id=uuid4()
    )
    mock_todo2 = Todo(
        id=uuid4(),
        title="Todo 2",
        description="Description 2",
        completed=True,
        user_id=uuid4()
    )

    # Mock query result
    mock_query_result = Mock()
    mock_query_result.all.return_value = [mock_todo1, mock_todo2]

    mock_session.exec.return_value = mock_query_result

    user_id = uuid4()
    result = get_todos_by_user(mock_session, user_id)

    # Verify the result
    assert len(result) == 2
    assert result[0] == mock_todo1
    assert result[1] == mock_todo2

    # Verify exec was called
    mock_session.exec.assert_called_once()


def test_get_todo_by_id_and_user_found():
    """Test getting a todo by ID and user when found"""
    # Mock session
    mock_session = Mock(spec=Session)

    # Mock todo object
    mock_todo = Todo(
        id=uuid4(),
        title="Existing Todo",
        description="Description",
        completed=False,
        user_id=uuid4()
    )

    # Mock query result
    mock_query_result = Mock()
    mock_query_result.first.return_value = mock_todo

    mock_session.exec.return_value = mock_query_result

    user_id = uuid4()
    todo_id = mock_todo.id
    result = get_todo_by_id_and_user(mock_session, todo_id, user_id)

    # Verify the result
    assert result == mock_todo


def test_get_todo_by_id_and_user_not_found():
    """Test getting a todo by ID and user when not found"""
    # Mock session
    mock_session = Mock(spec=Session)

    # Mock query result to return None
    mock_query_result = Mock()
    mock_query_result.first.return_value = None

    mock_session.exec.return_value = mock_query_result

    user_id = uuid4()
    todo_id = uuid4()
    result = get_todo_by_id_and_user(mock_session, todo_id, user_id)

    # Verify the result is None
    assert result is None