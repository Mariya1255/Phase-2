from fastapi import APIRouter, Depends
from ..middleware.auth_middleware import get_current_user

router = APIRouter()

@router.get("/protected-data")
def get_protected_data(current_user: dict = Depends(get_current_user)):
    """
    Example of a protected endpoint that requires a valid JWT token
    """
    return {
        "message": f"Hello {current_user['email']}, this is protected data!",
        "user_id": current_user["user_id"],
        "email": current_user["email"]
    }

@router.get("/dashboard")
def get_dashboard(current_user: dict = Depends(get_current_user)):
    """
    Protected dashboard endpoint
    """
    return {
        "dashboard": "accessible",
        "user": current_user["email"],
        "user_id": current_user["user_id"]
    }