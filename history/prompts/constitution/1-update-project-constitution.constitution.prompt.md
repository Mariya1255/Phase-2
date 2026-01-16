---
id: 1
title: Update Project Constitution
stage: constitution
date: 2026-01-12
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: icon
command: /sp.constitution
labels: [constitution, governance, setup]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```
/sp.constitution

Project: Todo Full-Stack Web Application (Phase-2)

Core principles:
- Spec-driven development (all behavior defined before implementation)
- Agentic workflow enforcement (spec → plan → tasks → execution)
- Security by design (authentication and authorization enforced at every layer)
- Data integrity and user isolation (strict ownership of tasks)
- Reproducibility (every feature traceable to a spec requirement)

Key standards:
- All functionality must map directly to an approved spec
- No manual coding; all implementation via Claude Code
- REST API must follow resource-based conventions and proper HTTP status codes
- Authentication must use Better Auth with JWT-based verification
- Backend must validate JWT tokens on every request
- Database queries must always be scoped to the authenticated user
- Frontend must attach JWT token to every API request
- Error handling must be explicit and consistent (401, 403, 404, 500)

Constraints:
- Technology stack is fixed and non-negotiable:
  - Frontend: Next.js 16+ (App Router)
  - Backend: Python FastAPI
  - ORM: SQLModel
  - Database: Neon Serverless PostgreSQL
  - Authentication: Better Auth + JWT
- All five Basic Level features must be implemented
- All API endpoints require authentication after login
- JWT secret must be shared via environment variable `BETTER_AUTH_SECRET`
- Stateless authentication only (no backend session storage)
- Multi-user support is mandatory

Success criteria:
- Users can sign up and sign in successfully
- Authenticated users can only access their own tasks
- All REST API endpoints function as specified
- Unauthorized requests return 401 Unauthorized
- Task ownership is enforced on every CRUD operation
- Data persists correctly in Neon PostgreSQL
- Frontend is responsive and fully functional
- Entire system passes spec-to-implementation traceability review
```

## Response snapshot

Updated the project constitution file at `.specify/memory/constitution.md` with the specified principles, standards, constraints, and success criteria. The constitution now includes six core principles, key standards for the tech stack and authentication, implementation constraints, and clear success criteria for the project. The file includes governance information and follows the required formatting.

## Outcome

- ✅ Impact: Updated project constitution with comprehensive governance principles for the Todo Full-Stack Web Application
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with new constitution content
- 🔁 Next prompts: Continue with spec-driven development workflow
- 🧠 Reflection: Constitution provides clear governance framework for the project

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): initial constitution setup
- Next experiment (smallest change to try): Proceed with spec creation based on constitution