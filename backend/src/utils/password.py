from passlib.context import CryptContext

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