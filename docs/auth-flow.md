# Authentication Flow Documentation

## Overview
This document describes the authentication flow implemented in the application, including user registration, login, JWT token handling, and protected resource access.

## Architecture
- **Frontend**: Next.js 16+ with App Router
- **Backend**: FastAPI with JWT-based authentication
- **Authentication Library**: Custom implementation with JWT tokens (aligned with Better Auth concepts)
- **Database**: Neon Serverless PostgreSQL

## User Registration Flow
1. User navigates to `/signup` page
2. User enters email and password
3. Frontend validates input and sends request to `/api/auth/signup`
4. Backend creates user with hashed password
5. Backend generates JWT token and returns it with user info
6. Frontend stores JWT in localStorage
7. User is redirected to dashboard

## User Login Flow
1. User navigates to `/signin` page
2. User enters email and password
3. Frontend validates input and sends request to `/api/auth/signin`
4. Backend verifies credentials and generates JWT token
5. Backend returns JWT token with user info
6. Frontend stores JWT in localStorage
7. User is redirected to dashboard

## JWT Token Structure
The JWT tokens contain the following claims:
- `sub`: Subject (user's email)
- `user_id`: User's unique identifier (UUID)
- `exp`: Expiration timestamp
- `iat`: Issued at time

## Protected Resource Access
1. Frontend includes JWT token in `Authorization: Bearer <token>` header
2. Backend middleware (`auth_middleware.py`) intercepts requests
3. JWT token is validated using the shared secret
4. User identity is extracted from token payload
5. Request proceeds if token is valid, returns 401 if invalid

## User Isolation and Data Protection
1. All user-specific data includes a `user_id` field
2. API endpoints verify that requested resources belong to authenticated user
3. Database queries are filtered by `user_id` to prevent unauthorized access
4. Users can only access their own data

## Security Measures
- Passwords are hashed using bcrypt
- JWT tokens are signed with a secret key stored in environment variables
- All authentication endpoints require HTTPS in production
- Token expiration limits session duration
- User ID validation prevents malformed token attacks

## Error Handling
- Invalid credentials return 401 Unauthorized
- Expired tokens return 401 Unauthorized
- Malformed tokens return 401 Unauthorized
- Insufficient permissions return 403 Forbidden
- Internal errors return 500 Internal Server Error

## Frontend Components
- `frontend/src/lib/auth.js`: Authentication utilities
- `frontend/src/app/signup/page.tsx`: Registration page
- `frontend/src/app/signin/page.tsx`: Login page
- `frontend/src/app/dashboard/page.tsx`: Protected dashboard
- `frontend/src/services/api.ts`: API service with token handling
- `frontend/src/lib/api-client.ts`: API client wrapper

## Backend Components
- `backend/src/api/auth.py`: Authentication endpoints
- `backend/src/services/auth.py`: Authentication business logic
- `backend/src/utils/jwt.py`: JWT token utilities
- `backend/src/middleware/auth_middleware.py`: Authentication middleware
- `backend/src/models/user.py`: User data model
- `backend/src/models/task.py`: Task data model with user relationship
- `backend/src/services/task_service.py`: Task business logic with user isolation
- `backend/src/api/tasks.py`: Task endpoints with user validation