# ADR-1: Full-Stack Architecture with JWT-Based Authentication

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2026-01-13
- **Feature:** 1-todo-web-app
- **Context:** Need to transform a console-based todo app into a secure, multi-user web application with proper authentication, authorization, and data isolation between users.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

Implement a full-stack web application architecture with separate frontend (Next.js) and backend (FastAPI) services connected via RESTful API with JWT-based authentication. The architecture includes:

- Frontend: Next.js 16+ with App Router for responsive UI
- Backend: Python FastAPI for REST API endpoints
- Authentication: Better Auth with JWT tokens for stateless authentication
- Data Layer: Neon Serverless PostgreSQL with SQLModel ORM
- Security: JWT validation middleware enforcing user data isolation
- Deployment: Separate services for independent scaling

## Consequences

### Positive

- Clear separation of concerns between frontend and backend
- Stateless authentication allowing horizontal scaling
- Proper user data isolation with foreign key constraints
- Modern tech stack with strong community support
- Independent deployment and scaling of frontend/backend
- Security by design with JWT validation on all protected endpoints

### Negative

- Increased complexity with multiple services to maintain
- Network latency between frontend and backend
- More complex development setup with multiple environments
- Potential for distributed system issues
- Additional infrastructure costs for separate services

## Alternatives Considered

Alternative Monolithic Architecture: Single application handling both frontend and backend
- Why rejected: Would not allow independent scaling and creates tight coupling between components

Alternative Server-Side Rendering Only: Using a framework like Next.js with server-side auth
- Why rejected: Would require session management on the server side, violating the stateless requirement

Alternative Microservices: Breaking into even smaller services (separate auth service, todo service, etc.)
- Why rejected: Over-engineering for this use case; adds unnecessary complexity without proportional benefits

## References

- Feature Spec: ../specs/1-todo-web-app/spec.md
- Implementation Plan: ../specs/1-todo-web-app/plan.md
- Related ADRs:
- Evaluator Evidence: ../history/prompts/1-todo-web-app/2-implementation-plan-todo-fullstack-app.plan.prompt.md