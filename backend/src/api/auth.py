from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from ..database.database import get_session
from ..models.user import UserCreate, UserResponse
from ..services.auth import create_user, login_user
from typing import Dict, Any

router = APIRouter()


@router.post("/signup", response_model=Dict[str, Any])
def signup(user: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user
    """
    try:
        created_user = create_user(session, user)

        # Login the user after successful registration
        login_result = login_user(session, user.email, user.password)

        return {
            "user": {
                "id": str(created_user.id),
                "email": created_user.email
            },
            "token": login_result["access_token"]
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration"
        )


@router.post("/signin", response_model=Dict[str, Any])
def signin(user: UserCreate, session: Session = Depends(get_session)):
    """
    Authenticate a user and return access token
    """
    try:
        login_result = login_user(session, user.email, user.password)

        return {
            "user": login_result["user"],
            "token": login_result["access_token"]
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during authentication"
        )


@router.post("/signout")
def signout():
    """
    Sign out a user (placeholder - stateless JWT doesn't require server-side logout)
    """
    return {"success": True}