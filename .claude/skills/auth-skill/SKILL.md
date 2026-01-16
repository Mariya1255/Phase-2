---
name: auth-skill
description: Implement secure authentication systems including signup, signin, password hashing, JWT tokens, and Better Auth integration.
---

# Authentication System

## Instructions

1. **Core Authentication Flows**
   - User signup with validation
   - User signin with credentials
   - Secure logout handling
   - Token refresh mechanism

2. **Security Implementation**
   - Password hashing using bcrypt or argon2
   - Never store plain-text passwords
   - Environment-based secret management
   - Rate limiting for auth endpoints

3. **JWT Token Handling**
   - Generate access and refresh tokens
   - Set token expiration times
   - Verify JWT on protected routes
   - Attach user context from token payload

4. **Better Auth Integration**
   - Configure Better Auth provider
   - Use built-in session handling
   - Support email/password auth
   - Optional OAuth providers (Google, GitHub)

## Best Practices
- Use HTTPS only
- Hash passwords with salt
- Keep JWT payload minimal
- Rotate secrets periodically
- Protect routes with middleware
- Handle auth errors gracefully

## Example Structure
```ts
// signup
POST /api/auth/signup
- validate input
- hash password
- store user
- return success

// signin
POST /api/auth/signin
- verify credentials
- generate JWT
- return token

// protected route
GET /api/profile
- verify JWT
- return user data
