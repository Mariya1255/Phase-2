import pytest
from fastapi.testclient import TestClient
from backend.src.main import app
from backend.src.database.database import engine, get_session
from sqlmodel import Session, SQLModel, create_engine
from unittest.mock import AsyncMock, patch
from backend.src.models.user import User


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    with TestClient(app) as test_client:
        yield test_client


def test_signup_new_user(client):
    """Test signing up a new user"""
    # Mock the database session
    with patch('backend.src.api.auth.get_session') as mock_get_session:
        # Create a mock session
        mock_session = AsyncMock()

        # Mock the query to return None (user doesn't exist)
        mock_exec_result = AsyncMock()
        mock_exec_result.first.return_value = None

        mock_session.exec.return_value = mock_exec_result

        # Configure the mock get_session to return our mock session
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock the user creation and login
        from backend.src.models.user import UserResponse
        mock_user = UserResponse(
            id="test-id",
            email="test@example.com",
            created_at="2023-01-01T00:00:00",
            updated_at="2023-01-01T00:00:00"
        )

        with patch('backend.src.services.auth.create_user', return_value=mock_user), \
             patch('backend.src.services.auth.login_user', return_value={
                 "access_token": "fake-token",
                 "token_type": "bearer",
                 "user": {"id": "test-id", "email": "test@example.com"}
             }):

            response = client.post(
                "/api/auth/signup",
                json={"email": "test@example.com", "password": "password123"}
            )

            assert response.status_code == 200
            data = response.json()
            assert "token" in data
            assert data["user"]["email"] == "test@example.com"


def test_signin_existing_user(client):
    """Test signing in an existing user"""
    with patch('backend.src.api.auth.get_session') as mock_get_session:
        # Create a mock session
        mock_session = AsyncMock()

        # Configure the mock get_session to return our mock session
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock the login
        with patch('backend.src.services.auth.login_user', return_value={
            "access_token": "fake-token",
            "token_type": "bearer",
            "user": {"id": "test-id", "email": "test@example.com"}
        }):

            response = client.post(
                "/api/auth/signin",
                json={"email": "test@example.com", "password": "password123"}
            )

            assert response.status_code == 200
            data = response.json()
            assert "token" in data
            assert data["user"]["email"] == "test@example.com"


def test_signout(client):
    """Test signing out a user"""
    response = client.post("/api/auth/signout")

    assert response.status_code == 200
    data = response.json()
    assert data == {"success": True}