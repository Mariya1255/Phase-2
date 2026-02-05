# Data Model: Authentication & Security Layer

## User Entity

**Description**: Represents an authenticated user with credentials and identity information

**Fields**:
- `id`: Unique identifier for the user (UUID/string)
- `email`: User's email address (string, unique, required)
- `password_hash`: Hashed password for authentication (string, required)
- `created_at`: Timestamp when user account was created (datetime)
- `updated_at`: Timestamp when user account was last updated (datetime)

**Validation Rules**:
- Email must be valid email format
- Email must be unique across all users
- Password must meet minimum security requirements
- All required fields must be present

## JWT Token Structure

**Description**: JSON Web Token containing user identity claims for stateless authentication

**Claims**:
- `sub`: Subject (user ID) - identifies the user
- `iat`: Issued at time - when token was created
- `exp`: Expiration time - when token becomes invalid
- `email`: User's email address (optional, for convenience)

**Validation Rules**:
- Token signature must be verified using `BETTER_AUTH_SECRET`
- Token must not be expired
- `sub` claim must correspond to a valid user ID

## Session Context

**Description**: Runtime context extracted from JWT token for request processing

**Fields**:
- `user_id`: Identifier of authenticated user
- `user_email`: Email of authenticated user
- `is_authenticated`: Boolean indicating authentication status
- `permissions`: List of permissions granted to user (for future expansion)

**State Transitions**:
- Unauthenticated → Authenticated: When valid JWT token is presented
- Authenticated → Unauthenticated: When token expires or is invalid

## Relationships

- One User entity can have multiple active JWT tokens (though typically one per device/session)
- JWT tokens are stateless and self-contained (no database relationship needed)
- User data isolation is enforced by matching JWT `sub` claim with user ID in database queries