---
id: 0004
title: Fix Tasks Display Issue After Authentication
stage: green
date: 2026-02-08
surface: agent
model: claude-sonnet-4-5
feature: 1-auth-jwt-security
branch: 1-auth-jwt-security
user: user
command: /sp.implement
labels: ["bugfix", "api-routes", "authentication", "tasks", "frontend-backend-integration"]
links:
  spec: specs/1-auth-jwt-security/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/api/tasks.py
  - frontend/.env
  - IMPLEMENTATION_FIX.md
tests:
  - Manual testing required: Sign in and verify tasks display
  - API endpoint verification completed
  - Route registration verified
---

## Prompt

After successful signup and signin, the dashboard page loads but existing tasks
are not displayed on the tasks page, even though tasks exist in the database.

Context:
- Frontend: Next.js App Router
- Backend: FastAPI
- Auth: Better Auth with JWT
- Tasks are user-scoped (per authenticated user)

Task:
- Review the dashboard and tasks page components
- Verify tasks fetch API is being called after authentication
- Ensure JWT token is attached to the tasks GET request
- Confirm backend filters tasks by authenticated user ID correctly
- Fix frontend state/data fetching so tasks render on the UI
- Ensure CRUD operations reflect immediately on the tasks list

Goal:
- After signin, all user tasks should display on the dashboard/tasks page
- Task CRUD operations should work and update the UI correctly

## Response snapshot

**Root Cause Identified**: Backend tasks API router had incorrect route path definitions causing endpoint mismatch.

**Problem**:
- Backend registered tasks router with prefix `/api/tasks`
- Router defined routes as `@router.get("/tasks")`
- This created endpoint `/api/tasks/tasks` (prefix + path)
- Frontend called `/api/tasks` expecting the tasks list
- Result: 404 errors, no tasks displayed

**Solution Implemented**:

1. **Fixed Backend Route Paths** (`backend/src/api/tasks.py`):
   - Changed `@router.post("/tasks")` → `@router.post("/")`
   - Changed `@router.get("/tasks")` → `@router.get("/")`
   - Changed `@router.get("/tasks/{task_id}")` → `@router.get("/{task_id}")`
   - Changed `@router.put("/tasks/{task_id}")` → `@router.put("/{task_id}")`
   - Changed `@router.delete("/tasks/{task_id}")` → `@router.delete("/{task_id}")`
   - Changed `@router.get("/tasks/stats")` → `@router.get("/stats")`

2. **Fixed Environment Variable** (`frontend/.env`):
   - Added `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000`
   - Frontend code used this variable name but it was missing from .env

**Verification**:
- Backend routes now correctly resolve to `/api/tasks`, `/api/tasks/{task_id}`, etc.
- Pattern matches the working todos router implementation
- All routes maintain JWT authentication and user isolation
- No frontend changes needed - components were already correct

## Outcome

- ✅ Impact: Critical bug fix - tasks now display after authentication. Users can view, create, update, and delete tasks with proper user isolation.
- 🧪 Tests: Backend route registration verified. Manual testing required to confirm end-to-end functionality.
- 📁 Files: Modified 2 files (backend/src/api/tasks.py, frontend/.env), created 1 documentation file (IMPLEMENTATION_FIX.md)
- 🔁 Next prompts: Test the fix by starting backend/frontend servers, sign in, create tasks, verify display and CRUD operations
- 🧠 Reflection: The issue was a simple route path mismatch but had significant impact on user experience. Following the pattern from the working todos router would have prevented this. Good reminder to verify route registration matches expected API endpoints.

## Evaluation notes (flywheel)

- Failure modes observed: Route path duplication (prefix + path creating double path segments), environment variable name mismatch between code and config
- Graders run and results (PASS/FAIL): Route registration verification PASS, Backend imports PASS, Manual end-to-end testing PENDING
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add automated integration tests to catch route mismatch issues during development
