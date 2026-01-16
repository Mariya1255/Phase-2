# ADR-2: Technology Stack Selection for Full-Stack Application

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2026-01-13
- **Feature:** 1-todo-web-app
- **Context:** Need to select appropriate technologies for building a modern, scalable, and maintainable full-stack web application with proper security and performance characteristics.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

Select the following integrated technology stack for the full-stack application:

- Frontend Framework: Next.js 16+ with App Router
- Backend Framework: Python FastAPI
- Database ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT
- Testing: pytest for backend, Jest/React Testing Library for frontend
- Deployment: Containerized services (potential for cloud deployment)

## Consequences

### Positive

- Next.js provides excellent developer experience with server-side rendering and routing
- FastAPI offers automatic API documentation and type validation
- SQLModel provides elegant SQL database interaction with Pydantic integration
- Neon Serverless PostgreSQL offers automatic scaling and reduced operational overhead
- Better Auth provides battle-tested authentication with JWT support
- Strong typing throughout the stack with TypeScript and Python type hints
- Modern tooling with excellent ecosystem support

### Negative

- Learning curve for team members unfamiliar with these technologies
- Potential vendor lock-in to specific platforms (Neon, Vercel-style deployment)
- Possible performance overhead of abstraction layers
- Dependency on third-party authentication provider
- Need for coordination between different language ecosystems (JavaScript/TypeScript and Python)

## Alternatives Considered

Alternative Stack A: Django + React + PostgreSQL
- Why rejected: Would mix Python backend with JavaScript frontend but lacks some modern conveniences of FastAPI and Next.js

Alternative Stack B: Node.js backend (Express/NestJS) + React + MongoDB
- Why rejected: Would use different database technology and potentially less efficient backend framework than FastAPI for this use case

Alternative Stack C: Ruby on Rails + React + PostgreSQL
- Why rejected: Would use different backend language and framework, potentially slower development for the team

## References

- Feature Spec: ../specs/1-todo-web-app/spec.md
- Implementation Plan: ../specs/1-todo-web-app/plan.md
- Related ADRs:
- Evaluator Evidence: ../history/prompts/1-todo-web-app/2-implementation-plan-todo-fullstack-app.plan.prompt.md