from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from ..models.user import User, UserCreate
from ..lib.jwt_utils import create_access_token
from passlib.context import CryptContext
from typing import Optional
from datetime import timedelta

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password, validating length to comply with bcrypt limitations
    """
    # Validate password length for bcrypt (max 72 characters)
    if len(password) > 72:
        raise ValueError("Password must not exceed 72 characters due to bcrypt limitations")
    return pwd_context.hash(password)


def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user by email and password
    """
    try:
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()

        if not user or not verify_password(password, user.password):
            return None

        return user
    except IntegrityError:
        # Handle database integrity errors during authentication
        return None
    except Exception:
        # Handle any other errors during authentication
        return None


def create_user(session: Session, user_create: UserCreate) -> User:
    """
    Create a new user with hashed password
    """
    try:
        # Hash the password
        hashed_password = get_password_hash(user_create.password)

        # Create the user
        user = User(
            email=user_create.email,
            password=hashed_password
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        return user
    except IntegrityError as ie:
        # Handle database integrity errors (like duplicate email)
        session.rollback()
        raise ValueError(f"Email already registered: {str(ie)}")
    except ValueError as ve:
        # Re-raise ValueError for validation issues (like password length)
        session.rollback()
        raise ve
    except Exception as e:
        # Rollback in case of any error during user creation
        session.rollback()
        raise e


def login_user(session: Session, email: str, password: str) -> dict:
    """
    Login a user and return access token
    """
    try:
        user = authenticate_user(session, email, password)

        if not user:
            raise ValueError("Invalid email or password")

        # Create access token
        access_token_expires = timedelta(minutes=30)  # 30 minutes expiry
        access_token = create_access_token(
            data={"sub": user.email, "user_id": str(user.id)},
            expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": str(user.id),  # Convert UUID to string to match expected format
                "email": user.email
            }
        }
    except ValueError:
        # Re-raise ValueError for invalid credentials
        raise
    except IntegrityError as ie:
        # Handle database integrity errors during login
        raise ValueError(f"Database error during authentication: {str(ie)}")
    except Exception as e:
        # Handle any other unexpected errors during login
        raise ValueError(f"An error occurred during authentication: {str(e)}")