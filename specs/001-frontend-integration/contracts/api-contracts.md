# API Contract Specifications: Frontend Application & Full-Stack Integration

## Authentication API Contracts

### POST /api/auth/signup
**Purpose:** Register a new user account

**Request:**
- Method: POST
- Endpoint: `/api/auth/signup`
- Content-Type: `application/json`
- Headers: None required
- Body:
```json
{
  "email": "user@example.com",
  "password": "secure_password_123"
}
```

**Response (200 OK):**
```json
{
  "user": {
    "id": "uuid-string",
    "email": "user@example.com"
  },
  "token": "jwt-token-string"
}
```

**Response (400 Bad Request):**
```json
{
  "detail": "Error message describing the issue"
}
```

### POST /api/auth/signin
**Purpose:** Authenticate an existing user

**Request:**
- Method: POST
- Endpoint: `/api/auth/signin`
- Content-Type: `application/json`
- Headers: None required
- Body:
```json
{
  "email": "user@example.com",
  "password": "secure_password_123"
}
```

**Response (200 OK):**
```json
{
  "user": {
    "id": "uuid-string",
    "email": "user@example.com"
  },
  "token": "jwt-token-string"
}
```

**Response (401 Unauthorized):**
```json
{
  "detail": "Invalid credentials or other auth error"
}
```

### POST /api/auth/signout
**Purpose:** Sign out the current user (stateless JWT - mainly for frontend cleanup)

**Request:**
- Method: POST
- Endpoint: `/api/auth/signout`
- Headers: None required
- Body: None

**Response (200 OK):**
```json
{
  "success": true
}
```

## Task Management API Contracts

### GET /api/tasks
**Purpose:** Retrieve all tasks for the authenticated user

**Request:**
- Method: GET
- Endpoint: `/api/tasks`
- Headers: `Authorization: Bearer {jwt_token}`

**Response (200 OK):**
```json
[
  {
    "id": "uuid-string",
    "title": "Task title",
    "description": "Task description",
    "status": "pending",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z",
    "user_id": "user-uuid-string"
  }
]
```

**Response (401 Unauthorized):** When token is invalid
**Response (403 Forbidden):** When attempting to access other users' tasks

### POST /api/tasks
**Purpose:** Create a new task for the authenticated user

**Request:**
- Method: POST
- Endpoint: `/api/tasks`
- Headers: `Authorization: Bearer {jwt_token}`
- Content-Type: `application/json`
- Body:
```json
{
  "title": "New task title",
  "description": "New task description"
}
```

**Response (200 OK):**
```json
{
  "id": "uuid-string",
  "title": "New task title",
  "description": "New task description",
  "status": "pending",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "user_id": "user-uuid-string"
}
```

**Response (401 Unauthorized):** When token is invalid
**Response (400 Bad Request):** When request data is invalid

### GET /api/tasks/{task_id}
**Purpose:** Retrieve a specific task for the authenticated user

**Request:**
- Method: GET
- Endpoint: `/api/tasks/{task_id}` (where task_id is a UUID)
- Headers: `Authorization: Bearer {jwt_token}`

**Response (200 OK):**
```json
{
  "id": "uuid-string",
  "title": "Task title",
  "description": "Task description",
  "status": "pending",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "user_id": "user-uuid-string"
}
```

**Response (401 Unauthorized):** When token is invalid
**Response (404 Not Found):** When task doesn't exist or doesn't belong to user

### PUT /api/tasks/{task_id}
**Purpose:** Update a specific task for the authenticated user

**Request:**
- Method: PUT
- Endpoint: `/api/tasks/{task_id}` (where task_id is a UUID)
- Headers: `Authorization: Bearer {jwt_token}`
- Content-Type: `application/json`
- Body:
```json
{
  "title": "Updated task title",
  "description": "Updated task description",
  "status": "in_progress"
}
```

**Response (200 OK):**
```json
{
  "id": "uuid-string",
  "title": "Updated task title",
  "description": "Updated task description",
  "status": "in_progress",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-02T00:00:00Z",  // Updated timestamp
  "user_id": "user-uuid-string"
}
```

**Response (401 Unauthorized):** When token is invalid
**Response (404 Not Found):** When task doesn't exist or doesn't belong to user

### DELETE /api/tasks/{task_id}
**Purpose:** Delete a specific task for the authenticated user

**Request:**
- Method: DELETE
- Endpoint: `/api/tasks/{task_id}` (where task_id is a UUID)
- Headers: `Authorization: Bearer {jwt_token}`

**Response (200 OK):**
```json
{
  "message": "Task deleted successfully"
}
```

**Response (401 Unauthorized):** When token is invalid
**Response (404 Not Found):** When task doesn't exist or doesn't belong to user

## Protected API Contracts

### GET /api/protected/protected-data
**Purpose:** Access protected data requiring authentication

**Request:**
- Method: GET
- Endpoint: `/api/protected/protected-data`
- Headers: `Authorization: Bearer {jwt_token}`

**Response (200 OK):**
```json
{
  "message": "This is protected data",
  "user_id": "user-uuid-string",
  "email": "user@example.com"
}
```

**Response (401 Unauthorized):** When token is invalid