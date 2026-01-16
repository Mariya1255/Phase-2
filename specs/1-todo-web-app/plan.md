# Implementation Plan: Todo Full-Stack Web Application (Phase-2)

**Branch**: `1-todo-web-app` | **Date**: 2026-01-13 | **Spec**: [specs/1-todo-web-app/spec.md](../specs/1-todo-web-app/spec.md)
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

## Summary

A full-stack web application that transforms a console-based todo app into a secure, multi-user web application using Next.js frontend, FastAPI backend, Neon PostgreSQL database, and Better Auth with JWT authentication. The system will enforce user isolation, provide RESTful API endpoints for todo operations, and deliver a responsive web interface for task management.

## Technical Context

**Language/Version**: Python 3.11 (Backend), JavaScript/TypeScript (Frontend), Next.js 16+
**Primary Dependencies**: FastAPI, SQLModel, Neon Serverless PostgreSQL, Better Auth, JWT
**Storage**: Neon Serverless PostgreSQL database with SQLModel ORM
**Testing**: pytest for backend, Jest/React Testing Library for frontend
**Target Platform**: Web application (multi-user, cross-platform)
**Project Type**: Full-stack web application with separate frontend and backend
**Performance Goals**: <200ms p95 API response time, Support 100 concurrent users
**Constraints**: JWT-based authentication required on all API endpoints, User data isolation mandatory, Stateless authentication
**Scale/Scope**: Multi-user support with proper data isolation, Responsive web interface

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Spec-Driven Development: Implementation follows spec → plan → tasks → execution sequence
- ✅ Agentic Workflow Enforcement: Following strict sequence with Claude Code only
- ✅ Security by Design: JWT authentication and user isolation built into architecture
- ✅ Data Integrity and User Isolation: Strict ownership enforcement planned
- ✅ Reproducibility: Full traceability from spec to implementation
- ✅ No Manual Coding: All implementation via Claude Code and Spec-Kit Plus
- ✅ Technology Stack Adherence: Using Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth
- ✅ Authentication Standards: JWT-based with BETTER_AUTH_SECRET environment variable
- ✅ API Requirements: RESTful endpoints with proper HTTP status codes
- ✅ Error Handling: Standardized error responses planned

## Project Structure

### Documentation (this feature)
```text
specs/1-todo-web-app/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)
```text
backend/
├── src/
│   ├── models/
│   │   ├── user.py          # User data model with SQLModel
│   │   └── todo.py          # Todo data model with SQLModel
│   ├── services/
│   │   ├── auth.py          # Authentication business logic
│   │   └── todo_service.py  # Todo business logic
│   ├── api/
│   │   ├── auth.py          # Authentication API routes
│   │   └── todos.py         # Todo API routes
│   ├── database/
│   │   └── database.py      # Database connection and setup
│   ├── middleware/
│   │   └── auth_middleware.py # JWT validation middleware
│   └── main.py              # FastAPI application entry point
├── requirements.txt         # Python dependencies
├── alembic/
│   ├── versions/            # Database migration files
│   └── env.py               # Alembic configuration
└── tests/
    ├── unit/
    ├── integration/
    └── conftest.py

frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx       # Root layout
│   │   ├── page.tsx         # Home page
│   │   ├── auth/
│   │   │   ├── sign-up/
│   │   │   │   └── page.tsx
│   │   │   └── sign-in/
│   │   │       └── page.tsx
│   │   └── dashboard/
│   │       ├── page.tsx
│   │       └── todos/
│   │           └── [id]/
│   │               └── page.tsx
│   ├── components/
│   │   ├── TodoList/
│   │   │   ├── TodoList.tsx
│   │   │   └── TodoItem.tsx
│   │   ├── TodoForm/
│   │   │   └── TodoForm.tsx
│   │   ├── Auth/
│   │   │   └── AuthForm.tsx
│   │   └── ui/              # Reusable UI components
│   ├── lib/
│   │   ├── auth.ts          # Authentication utilities
│   │   ├── api.ts           # API client with JWT handling
│   │   └── types.ts         # TypeScript type definitions
│   ├── hooks/
│   │   └── useAuth.ts       # Authentication hook
│   └── styles/
│       └── globals.css      # Global styles
├── public/
├── package.json
├── tsconfig.json
└── next.config.js

.env                          # Environment variables
docker-compose.yml            # Docker configuration
README.md                     # Project documentation
```

**Structure Decision**: Full-stack web application with separate backend (FastAPI) and frontend (Next.js) directories to maintain clear separation of concerns while enabling proper authentication flow and API communication. This structure allows for independent scaling and development of each component while maintaining proper security boundaries.

## Phase 0: Research & Unknown Resolution

### Research Tasks
1. **Better Auth JWT Configuration**: Research how to configure Better Auth to issue JWT tokens and extract user information from tokens
2. **FastAPI JWT Middleware**: Research JWT token validation in FastAPI, including proper error handling and user identification
3. **SQLModel Best Practices**: Research optimal data modeling with SQLModel and Neon PostgreSQL, including relationships, indexes, and validation
4. **Next.js 16+ Auth Integration**: Research Better Auth integration with Next.js App Router, including session management and protected routes
5. **Environment Configuration**: Research secure sharing of JWT secret between services and proper environment variable management
6. **Database Connection Pooling**: Research optimal database connection handling with Neon Serverless PostgreSQL in FastAPI
7. **Authentication Flow**: Research the complete authentication flow from signup to API access with JWT tokens
8. **CORS Configuration**: Research proper CORS setup to allow frontend-backend communication while maintaining security
9. **API Rate Limiting**: Research rate limiting strategies for the API endpoints
10. **Password Hashing**: Research best practices for password hashing with Better Auth and additional security measures

### Research Outcomes (to be completed in research.md)
- Decision: [what was chosen]
- Rationale: [why chosen]
- Alternatives considered: [what else evaluated]
- Security implications: [security considerations for each decision]
- Performance impact: [performance implications of each decision]

## Phase 1: Design & Contracts

### Data Model Design

#### User Entity
- **Fields**:
  - id (UUID, primary key, auto-generated)
  - email (string, unique, indexed, required, validated email format)
  - created_at (datetime, auto-generated)
  - updated_at (datetime, auto-generated)
- **Constraints**: Email uniqueness, proper indexing for authentication lookups
- **Relationships**: One-to-many with Todo entities (user_id foreign key)

#### Todo Entity
- **Fields**:
  - id (UUID, primary key, auto-generated)
  - title (string, required, max 255 chars)
  - description (text, optional, max 1000 chars)
  - completed (boolean, default false)
  - user_id (UUID, foreign key, references User.id, indexed)
  - created_at (datetime, auto-generated)
  - updated_at (datetime, auto-generated)
- **Constraints**: Foreign key relationship with User, proper indexing on user_id for efficient queries
- **Relationships**: Many-to-one with User entity

#### Indexes and Performance
- Primary keys on all entities
- Unique index on User.email for fast authentication
- Index on Todo.user_id for efficient user-specific queries
- Composite indexes where needed for complex queries

### API Contract Design

#### Authentication Endpoints
- **POST `/api/auth/signup`**
  - Request: `{email: string, password: string}`
  - Response: `{user: {id, email}, token: string}` on success, `400 Bad Request` on validation error, `409 Conflict` if email exists
  - Purpose: Register new user and return JWT token

- **POST `/api/auth/signin`**
  - Request: `{email: string, password: string}`
  - Response: `{user: {id, email}, token: string}` on success, `401 Unauthorized` on invalid credentials
  - Purpose: Authenticate existing user and return JWT token

- **POST `/api/auth/signout`**
  - Request: Authorization header with Bearer token
  - Response: `{success: true}` on success, `401 Unauthorized` on invalid token
  - Purpose: Invalidate user session (if needed for stateful session management)

#### Todo Management Endpoints
- **GET `/api/todos`**
  - Request: Authorization header with Bearer token
  - Response: `{todos: [{id, title, description, completed, created_at, updated_at}]}` on success, `401 Unauthorized` on invalid token
  - Purpose: Retrieve all todos for authenticated user

- **POST `/api/todos`**
  - Request: `{title: string, description?: string}` with Authorization header
  - Response: `{todo: {id, title, description, completed, user_id, created_at, updated_at}}` on success, `400 Bad Request` on validation error, `401 Unauthorized` on invalid token
  - Purpose: Create a new todo for authenticated user

- **GET `/api/todos/{id}`**
  - Request: Authorization header with Bearer token
  - Response: `{todo: {id, title, description, completed, user_id, created_at, updated_at}}` on success, `401 Unauthorized` on invalid token, `404 Not Found` if todo doesn't exist or doesn't belong to user
  - Purpose: Retrieve a specific todo for authenticated user

- **PUT `/api/todos/{id}`**
  - Request: `{title?: string, description?: string, completed?: boolean}` with Authorization header
  - Response: `{todo: {id, title, description, completed, user_id, updated_at}}` on success, `400 Bad Request` on validation error, `401 Unauthorized` on invalid token, `404 Not Found` if todo doesn't exist or doesn't belong to user
  - Purpose: Update a specific todo for authenticated user

- **PATCH `/api/todos/{id}/complete`**
  - Request: `{completed: boolean}` with Authorization header
  - Response: `{todo: {id, completed, updated_at}}` on success, `401 Unauthorized` on invalid token, `404 Not Found` if todo doesn't exist or doesn't belong to user
  - Purpose: Toggle completion status of a specific todo

- **DELETE `/api/todos/{id}`**
  - Request: Authorization header with Bearer token
  - Response: `{success: true}` on success, `401 Unauthorized` on invalid token, `404 Not Found` if todo doesn't exist or doesn't belong to user
  - Purpose: Delete a specific todo for authenticated user

### Security Design
- JWT token validation middleware on all protected endpoints
- User ID extraction from JWT claims for data isolation
- Proper HTTP status codes (200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, 500 Internal Server Error)
- Input validation and sanitization at API boundary
- SQL injection prevention through SQLModel parameterized queries
- Rate limiting on authentication endpoints to prevent brute force attacks
- Password strength validation (if implemented separately from Better Auth)

### Error Handling Design
- Consistent error response format: `{error: string, message: string, code?: string}`
- Proper HTTP status codes for different error conditions
- Detailed error messages for client debugging while protecting sensitive information
- Logging of errors for operational monitoring

## Phase 2: Implementation Planning (tasks.md)

The implementation will be broken down into small, testable tasks covering:

### Phase 2A: Backend Infrastructure
1. Set up FastAPI project structure and dependencies
2. Configure SQLModel with Neon PostgreSQL connection
3. Implement User and Todo data models with proper relationships
4. Create database migration system with Alembic
5. Implement JWT authentication middleware
6. Set up CORS and security headers

### Phase 2B: Authentication System
1. Integrate Better Auth for user registration/login
2. Configure JWT token generation and validation
3. Implement user registration endpoint with validation
4. Implement user login endpoint with JWT issuance
5. Create authentication middleware for protected routes
6. Implement proper error handling for auth failures

### Phase 2C: API Endpoints
1. Implement GET `/api/todos` endpoint with user filtering
2. Implement POST `/api/todos` endpoint with user association
3. Implement GET `/api/todos/{id}` endpoint with ownership check
4. Implement PUT `/api/todos/{id}` endpoint with ownership validation
5. Implement PATCH `/api/todos/{id}/complete` endpoint
6. Implement DELETE `/api/todos/{id}` endpoint with ownership check
7. Add proper request validation and response formatting

### Phase 2D: Frontend Development
1. Set up Next.js 16+ project with App Router
2. Create authentication UI components (signup/signin)
3. Implement protected route handling
4. Create todo management dashboard UI
5. Build todo list and form components
6. Implement JWT token management in frontend
7. Create API service layer with proper error handling

### Phase 2E: Integration and Testing
1. Integrate frontend with backend API
2. Implement comprehensive error handling and user feedback
3. Create unit tests for backend endpoints
4. Create integration tests for authentication flow
5. Perform security testing for user isolation
6. Conduct performance testing for expected load
7. Prepare deployment configuration

## Development Workflow

1. **Environment Setup**: Configure development environment with proper dependencies
2. **Database Schema**: Create and test database schema with migrations
3. **Authentication**: Implement and test authentication system first
4. **API Development**: Build and test API endpoints with proper security
5. **Frontend Development**: Create UI components and integrate with API
6. **Integration Testing**: Test complete user flows and security boundaries
7. **Performance Validation**: Ensure system meets performance requirements
8. **Documentation**: Create quickstart guide and API documentation

## Success Criteria for Implementation

- ✅ All authentication endpoints function correctly with JWT tokens
- ✅ Users can only access their own todos (data isolation verified)
- ✅ All API endpoints return proper HTTP status codes
- ✅ Frontend provides responsive and intuitive user experience
- ✅ System handles error conditions gracefully
- ✅ Performance requirements are met (<200ms p95 response time)
- ✅ Security requirements are satisfied (proper authentication/authorization)
- ✅ Code follows established architecture patterns and best practices

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multi-service architecture | Clear separation of frontend/backend concerns | Single repo would mix concerns and complicate deployment |
| JWT-based auth | Stateless authentication required by spec | Session-based would require backend session storage |
| Separate auth middleware | Security by design principle | Inline auth checks would duplicate code and create vulnerabilities |
| Comprehensive testing approach | Quality and security requirements | Minimal testing would not ensure proper security isolation |
| Database migration system | Production readiness and schema evolution | Direct schema changes would not support version control |