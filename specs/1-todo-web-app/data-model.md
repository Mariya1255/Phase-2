# Data Model Design: Todo Full-Stack Web Application (Phase-2)

## Overview
This document defines the data models for the Todo Full-Stack Web Application, including entity relationships, field definitions, and database schema design.

## Entity Models

### User Entity
**Purpose**: Represents a registered user in the system

#### Fields
- `id` (UUID, Primary Key)
  - Type: UUID (string format)
  - Constraints: Required, Unique, Auto-generated
  - Description: Unique identifier for the user

- `email` (String)
  - Type: String (max 255 characters)
  - Constraints: Required, Unique, Valid email format, Indexed
  - Description: User's email address for authentication

- `created_at` (DateTime)
  - Type: DateTime (ISO 8601 format)
  - Constraints: Required, Auto-generated
  - Description: Timestamp when the user account was created

- `updated_at` (DateTime)
  - Type: DateTime (ISO 8601 format)
  - Constraints: Required, Auto-generated, Updated on change
  - Description: Timestamp when the user account was last updated

#### Constraints & Indexes
- Primary Key: `id`
- Unique Constraint: `email`
- Index: `email` (for authentication lookups)

#### Validation Rules
- Email format must be valid (RFC 5322 compliant)
- Email must be unique across all users
- Email cannot be empty or null

### Todo Entity
**Purpose**: Represents a todo task created by a user

#### Fields
- `id` (UUID, Primary Key)
  - Type: UUID (string format)
  - Constraints: Required, Unique, Auto-generated
  - Description: Unique identifier for the todo item

- `title` (String)
  - Type: String (max 255 characters)
  - Constraints: Required
  - Description: Title or summary of the todo task

- `description` (Text)
  - Type: Text (max 1000 characters)
  - Constraints: Optional
  - Description: Detailed description of the todo task

- `completed` (Boolean)
  - Type: Boolean
  - Constraints: Required, Default: false
  - Description: Status indicating if the todo task is completed

- `user_id` (UUID, Foreign Key)
  - Type: UUID (string format)
  - Constraints: Required, References User.id, Indexed
  - Description: Foreign key linking to the user who owns this todo

- `created_at` (DateTime)
  - Type: DateTime (ISO 8601 format)
  - Constraints: Required, Auto-generated
  - Description: Timestamp when the todo was created

- `updated_at` (DateTime)
  - Type: DateTime (ISO 8601 format)
  - Constraints: Required, Auto-generated, Updated on change
  - Description: Timestamp when the todo was last updated

#### Constraints & Indexes
- Primary Key: `id`
- Foreign Key: `user_id` references `User.id`
- Index: `user_id` (for efficient user-specific queries)
- Check Constraint: `user_id` must reference an existing user

#### Validation Rules
- Title cannot be empty or null
- Title must be less than 256 characters
- Description must be less than 1001 characters if provided
- Completed status must be a boolean value
- User ID must reference an existing user

## Entity Relationships

### User → Todo (One-to-Many)
- A User can have many Todo items
- A Todo belongs to exactly one User
- Foreign key: `Todo.user_id` references `User.id`
- Cascade behavior: When a User is deleted, their Todos are also deleted (to be configured)

### Relationship Constraints
- Referential integrity: Todo.user_id must reference an existing User.id
- Data isolation: Users can only access Todos where user_id matches their own id
- Cascade deletion: When a User is deleted, all their Todos are automatically deleted

## Database Schema

### SQL Schema Definition
```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Index for email lookups (authentication)
CREATE INDEX idx_users_email ON users(email);

-- Todos table
CREATE TABLE todos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Index for user-specific queries
CREATE INDEX idx_todos_user_id ON todos(user_id);

-- Index for completed status (for potential filtering)
CREATE INDEX idx_todos_completed ON todos(completed);
```

## Data Access Patterns

### Common Queries
1. **User authentication**: `SELECT * FROM users WHERE email = ?`
2. **User's todos**: `SELECT * FROM todos WHERE user_id = ? ORDER BY created_at DESC`
3. **Specific todo**: `SELECT * FROM todos WHERE id = ? AND user_id = ?`
4. **Update todo**: `UPDATE todos SET title = ?, description = ?, completed = ? WHERE id = ? AND user_id = ?`
5. **Delete todo**: `DELETE FROM todos WHERE id = ? AND user_id = ?`

### Performance Considerations
- Email index for fast authentication lookups
- User ID index for efficient user-specific queries
- Potential composite indexes for complex filtering (to be added if needed)
- UUIDs provide security by making IDs unpredictable

## Security Considerations

### Data Isolation
- Foreign key constraints ensure data integrity
- Application-level checks ensure users can only access their own todos
- UUID primary keys prevent enumeration attacks

### Access Validation
- All todo operations must validate that the todo belongs to the authenticated user
- User ID from JWT token must match the user_id in the todo record
- Proper error responses for unauthorized access attempts

## Validation Requirements

### Input Validation
- Email format validation using standard regex patterns
- Title length validation (1-255 characters)
- Description length validation (0-1000 characters)
- Boolean validation for completed field
- UUID format validation for IDs

### Business Logic Validation
- Users cannot modify or access other users' todos
- Todo creation requires valid user ID
- Todo updates maintain user ownership
- Proper error handling for validation failures

## Migration Strategy

### Initial Schema Migration
1. Create users table with required fields and indexes
2. Create todos table with required fields, constraints, and indexes
3. Verify referential integrity constraints
4. Test basic CRUD operations

### Future Migration Considerations
- Additional indexes for performance optimization
- Audit trail fields (created_by, updated_by) if needed
- Soft delete functionality if required
- Additional metadata fields for advanced features