# Quickstart Guide: Authentication & Security Layer

## Prerequisites

- Node.js 18+ for Next.js frontend
- Python 3.11+ for FastAPI backend
- Neon Serverless PostgreSQL database
- Environment variable `BETTER_AUTH_SECRET` configured

## Setup Instructions

### 1. Environment Variables

Add to your `.env` files:

```bash
# Backend (.env in backend/)
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here
DATABASE_URL=your-neon-postgres-connection-string
```

```bash
# Frontend (.env in frontend/)
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000/api/auth
NEXTAUTH_SECRET=your-super-secret-jwt-key-here
```

### 2. Install Dependencies

**Backend:**
```bash
cd backend
pip install fastapi uvicorn sqlmodel pyjwt better-exceptions
```

**Frontend:**
```bash
cd frontend
npm install @better-auth/react @better-auth/client
```

### 3. Initialize Better Auth in Frontend

Create `frontend/src/lib/auth.js`:

```javascript
import { createAuthClient } from "@better-auth/client";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000/api/auth",
  // Additional configuration
});
```

### 4. Configure FastAPI JWT Middleware

Create `backend/src/middleware/auth_middleware.py`:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from typing import Dict, Optional
from config import settings

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    """Verify JWT token and return user payload"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.better_auth_secret, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

def get_current_user(payload: Dict = Depends(verify_token)):
    """Extract current user from token payload"""
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    return {"user_id": user_id, "email": payload.get("email")}
```

### 5. Protect API Routes

```python
from fastapi import APIRouter, Depends
from middleware.auth_middleware import get_current_user

router = APIRouter()

@router.get("/protected-endpoint")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello user {current_user['user_id']}"}
```

## Running the Application

1. Start the database (Neon PostgreSQL)
2. Start the backend: `cd backend && uvicorn main:app --reload`
3. Start the frontend: `cd frontend && npm run dev`
4. Access the application at `http://localhost:3000`

## Testing Authentication

1. Navigate to `/signup` to create a new account
2. Use credentials to sign in at `/signin`
3. JWT token will be automatically attached to API requests
4. Access protected routes with valid authentication