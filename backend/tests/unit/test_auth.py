import pytest
from sqlmodel import create_engine, Session
from unittest.mock import Mock, patch
from backend.src.services.auth import authenticate_user, create_user
from backend.src.models.user import User, UserCreate


def test_authenticate_user_success():
    """Test successful user authentication"""
    # Mock session
    mock_session = Mock(spec=Session)

    # Mock user
    mock_user = User(
        id="test-id",
        email="test@example.com",
        password="$2b$12$LQv3c9N9E8Kh3RJ8q./4E.tS66VWt4JkkjGf3a3O6L8fY7Z3Y4ZPK"  # bcrypt hash for "password"
    )

    # Mock query result
    mock_query_result = Mock()
    mock_query_result.first.return_value = mock_user

    mock_session.exec.return_value = mock_query_result

    # Patch the verify_password function to return True
    with patch('backend.src.services.auth.verify_password', return_value=True):
        result = authenticate_user(mock_session, "test@example.com", "password")

    assert result == mock_user


def test_authenticate_user_wrong_password():
    """Test authentication with wrong password"""
    # Mock session
    mock_session = Mock(spec=Session)

    # Mock user
    mock_user = User(
        id="test-id",
        email="test@example.com",
        password="$2b$12$LQv3c9N9E8Kh3RJ8q./4E.tS66VWt4JkkjGf3a3O6L8fY7Z3Y4ZPK"  # bcrypt hash for "password"
    )

    # Mock query result
    mock_query_result = Mock()
    mock_query_result.first.return_value = mock_user

    mock_session.exec.return_value = mock_query_result

    # Patch the verify_password function to return False
    with patch('backend.src.services.auth.verify_password', return_value=False):
        result = authenticate_user(mock_session, "test@example.com", "wrongpassword")

    assert result is None


def test_create_user_success():
    """Test successful user creation"""
    # Mock session
    mock_session = Mock(spec=Session)

    # Mock user creation
    user_create = UserCreate(
        email="newuser@example.com",
        password="password"
    )

    # Mock query result to indicate no existing user
    mock_query_result = Mock()
    mock_query_result.first.return_value = None

    mock_session.exec.return_value = mock_query_result

    # Patch get_password_hash to return a mock hash
    with patch('backend.src.services.auth.get_password_hash', return_value='hashed_password'):
        result = create_user(mock_session, user_create)

    # Assert that the user was created
    assert result.email == "newuser@example.com"
    assert result.password == "hashed_password"

    # Verify session.add, session.commit, and session.refresh were called
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()