from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Optional
from uuid import UUID
from ..utils.jwt import verify_token


security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, str]:
    """
    Get the current user from the JWT token in the Authorization header
    """
    token = credentials.credentials

    user_data = verify_token(token)

    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_data


def get_user_id_from_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UUID:
    """
    Extract user ID from the JWT token in the Authorization header and validate it
    """
    token = credentials.credentials

    user_data = verify_token(token)

    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Validate that user_id exists and is a valid UUID
    user_id_str = user_data.get("user_id")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_id = UUID(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID format in token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id


def validate_user_in_payload(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    """
    Validate that the JWT token contains valid user information
    """
    token = credentials.credentials

    user_data = verify_token(token)

    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Validate required fields in token payload
    required_fields = ["user_id", "email"]
    for field in required_fields:
        if field not in user_data or not user_data[field]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Missing required field '{field}' in token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    # Validate user_id format
    try:
        UUID(user_data["user_id"])
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID format in token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_data