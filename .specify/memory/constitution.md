<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 1.1.0
Modified principles: None (new constitution created based on user input)
Added sections: Core Principles (5 principles), Key Standards, Constraints, Success Criteria
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/spec-template.md ✅ updated
- .specify/templates/tasks-template.md ✅ updated
- .specify/templates/commands/*.md ⚠ pending review
Follow-up TODOs: None
-->

# Todo Full-Stack Web Application (Phase-2) Constitution

## Core Principles

### I. Spec-Driven Development
All behavior must be defined before implementation begins. Every feature and functionality must be traced back to an approved specification document before coding commences.

### II. Agentic Workflow Enforcement
Implementation must follow the strict sequence: spec → plan → tasks → execution. No skipping steps in the development process; each phase must be completed before moving to the next.

### III. Security by Design
Authentication and authorization must be enforced at every layer of the application. Security considerations are built into the architecture from the ground up, not added as an afterthought.

### IV. Data Integrity and User Isolation
Strict ownership of tasks and data must be maintained. Users can only access and modify their own data, with proper validation and enforcement at all system boundaries.

### V. Reproducibility
Every feature must be traceable to a spec requirement. All development work must be reproducible and verifiable through the documented specification-to-implementation pipeline.

### VI. No Manual Coding
All implementation must be performed using Claude Code and Spec-Kit Plus. Manual coding outside of the agentic workflow is prohibited.

## Key Standards

### Technology Stack Adherence
- Frontend: Next.js 16+ (App Router)
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth + JWT

### API Requirements
- All REST API endpoints must follow resource-based conventions
- Proper HTTP status codes must be used consistently
- All API endpoints require authentication after user login

### Authentication Standards
- Authentication must use Better Auth with JWT-based verification
- Backend must validate JWT tokens on every request
- Database queries must always be scoped to the authenticated user
- Frontend must attach JWT token to every API request
- JWT secret must be shared via environment variable `BETTER_AUTH_SECRET`

### Error Handling
- Error handling must be explicit and consistent
- Standardized error responses: 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Internal Server Error
- All error cases must be properly handled and tested

## Constraints

### Technology Stack
The technology stack is fixed and non-negotiable:
- Frontend: Next.js 16+ (App Router)
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth + JWT

### Feature Requirements
- All five Basic Level features must be implemented
- All API endpoints require authentication after login
- JWT secret must be shared via environment variable `BETTER_AUTH_SECRET`
- Stateless authentication only (no backend session storage)
- Multi-user support is mandatory

### Implementation Restrictions
- No manual coding; all implementation via Claude Code
- All functionality must map directly to an approved spec
- Backend must validate JWT tokens on every request
- Database queries must always be scoped to the authenticated user

## Success Criteria

### User Authentication
- Users can sign up and sign in successfully
- Authenticated users can only access their own tasks
- Unauthorized requests return 401 Unauthorized
- Task ownership is enforced on every CRUD operation

### API Functionality
- All REST API endpoints function as specified
- Data persists correctly in Neon PostgreSQL
- Backend properly validates JWT tokens and enforces user isolation

### Frontend Experience
- Frontend is responsive and fully functional
- All UI components work as expected
- User authentication flows work seamlessly

### System Quality
- Entire system passes spec-to-implementation traceability review
- All tests pass and code quality standards are met
- Security requirements are properly implemented

## Governance

All development activities must comply with this constitution. Any deviation from these principles requires explicit amendment to the constitution document. The development process must follow the spec-driven approach with proper documentation and traceability from requirements to implementation.

Code reviews must verify compliance with all constitutional principles. All features must be traceable to specification requirements, and all implementation must follow the agentic workflow.

**Version**: 1.1.0 | **Ratified**: 2026-01-12 | **Last Amended**: 2026-01-12