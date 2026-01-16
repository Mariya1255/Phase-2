# ADR-4: Data Architecture and Modeling with SQLModel and Neon PostgreSQL

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2026-01-13
- **Feature:** 1-todo-web-app
- **Context:** Need to design a robust data architecture that supports user isolation, efficient querying, proper relationships, and scalability while maintaining data integrity.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

Implement a data architecture using:

- Database: Neon Serverless PostgreSQL for managed, scalable SQL database
- ORM: SQLModel for Python-based database interaction with Pydantic integration
- Primary Keys: UUIDs for enhanced security and distributed system compatibility
- Relationships: Foreign key constraints between User and Todo entities
- Indexing: Strategic indexes on frequently queried fields (email, user_id)
- Data Isolation: Enforcement through foreign key relationships and application logic
- Migration Strategy: Alembic for database schema versioning and evolution

## Consequences

### Positive

- UUID primary keys prevent enumeration attacks and support distributed systems
- Foreign key constraints ensure referential integrity at database level
- Strategic indexing improves query performance
- SQLModel provides type safety and validation
- Neon's serverless features provide automatic scaling
- Alembic enables safe schema evolution
- Clear data ownership through foreign key relationships

### Negative

- UUIDs have slightly higher storage and performance overhead compared to integers
- Additional complexity of migration management
- Learning curve for SQLModel if team is unfamiliar
- Dependency on Neon-specific features
- Potential for more complex queries due to UUID usage
- Need for careful index management to maintain performance

## Alternatives Considered

Alternative NoSQL: Using MongoDB or similar document database
- Why rejected: Would lose ACID properties and complex relationship handling needed for user isolation

Alternative Integer IDs: Using auto-incrementing integer primary keys
- Why rejected: Would be more susceptible to enumeration attacks and less suitable for distributed systems

Alternative Direct SQL: Writing raw SQL queries instead of using ORM
- Why rejected: Would lose type safety, increase development time, and create more error-prone code

## References

- Feature Spec: ../specs/1-todo-web-app/spec.md
- Implementation Plan: ../specs/1-todo-web-app/plan.md
- Related ADRs:
- Evaluator Evidence: ../history/prompts/1-todo-web-app/2-implementation-plan-todo-fullstack-app.plan.prompt.md