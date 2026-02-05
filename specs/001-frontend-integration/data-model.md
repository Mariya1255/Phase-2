# Data Model Design: Frontend Application & Full-Stack Integration

## Entity: User

**Fields:**
- id (UUID, primary key)
- email (string, unique, required)
- password (string, hashed, required)
- created_at (timestamp, required)
- updated_at (timestamp, required)

**Relationships:**
- Has many: tasks (via user_id foreign key)

**Validation:**
- Email must be valid email format
- Email must be unique across all users
- Password must be at least 8 characters when creating
- Email and password are required for authentication

## Entity: Task

**Fields:**
- id (UUID, primary key)
- user_id (UUID, foreign key to User.id, required)
- title (string, max 255 chars, required)
- description (string, max 1000 chars, optional)
- status (enum: pending, in_progress, completed, default: pending)
- created_at (timestamp, required)
- updated_at (timestamp, required)

**Relationships:**
- Belongs to: user (via user_id foreign key)

**Validation:**
- Title is required
- Title must be less than 255 characters
- User_id must correspond to an existing user
- Status must be one of the allowed enum values
- Users can only access tasks where user_id matches their own ID

## Entity: Authentication Token (JWT)

**Structure:**
- Header: Algorithm and token type
- Payload: user_id, email (sub), expiration time, issued-at time
- Signature: Verified using shared secret

**Validation:**
- Token must not be expired
- Signature must be valid
- user_id in token must match the requested resource owner
- Stored in browser localStorage on frontend

## Data Flow

1. **User Registration:**
   - User provides email and password
   - Backend creates User record with hashed password
   - Backend generates JWT token containing user_id
   - Token returned to frontend and stored in localStorage

2. **User Authentication:**
   - User provides email and password
   - Backend validates credentials against stored hash
   - Backend generates JWT token containing user_id
   - Token returned to frontend and stored in localStorage

3. **Task Management:**
   - Frontend sends API request with JWT in Authorization header
   - Backend middleware validates JWT and extracts user_id
   - Backend ensures requested operations are scoped to user_id
   - Backend returns only tasks belonging to the authenticated user

4. **Security Isolation:**
   - All API endpoints validate JWT authenticity
   - All data operations are filtered by user_id
   - Users cannot access other users' tasks by design
   - Foreign key constraints enforce data relationships at database level