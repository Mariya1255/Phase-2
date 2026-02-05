# Quickstart Guide: Frontend Application & Full-Stack Integration

## Prerequisites

- Node.js 18+ for frontend development
- Python 3.9+ for backend development
- PostgreSQL database (or Neon Serverless PostgreSQL)
- Git for version control

## Environment Setup

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/your_database_name
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

4. Run database migrations (if using alembic):
```bash
alembic upgrade head
```

5. Start the backend server:
```bash
uvicorn src.main:app --reload --port 8000
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables in `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. Start the development server:
```bash
npm run dev
```

## Running the Application

1. Start the backend server (runs on http://localhost:8000)
2. Start the frontend server (runs on http://localhost:3000)
3. Visit http://localhost:3000 in your browser

## Using the Application

### User Registration
1. Navigate to http://localhost:3000/signup
2. Fill in your email and password (password must be at least 8 characters)
3. Click "Sign up" to create your account

### User Login
1. Navigate to http://localhost:3000/signin
2. Enter your registered email and password
3. Click "Sign in" to access the dashboard

### Task Management
1. After logging in, go to the dashboard at http://localhost:3000/dashboard
2. Navigate to the task management page at http://localhost:3000/dashboard/tasks
3. Create tasks using the form on the left
4. View your tasks in the list on the right
5. Delete tasks using the delete button

## API Testing

### Authentication Endpoints
- POST `/api/auth/signup` - Register a new user
- POST `/api/auth/signin` - Log in to an existing account
- POST `/api/auth/signout` - Log out of the current account

### Task Management Endpoints
- GET `/api/tasks` - Get all tasks for the authenticated user
- POST `/api/tasks` - Create a new task for the user
- GET `/api/tasks/{task_id}` - Get a specific task
- PUT `/api/tasks/{task_id}` - Update a specific task
- DELETE `/api/tasks/{task_id}` - Delete a specific task

## Troubleshooting

### Common Issues

1. **Backend not accessible**: Ensure the backend server is running on port 8000
2. **Authentication errors**: Check that JWT_SECRET_KEY matches between frontend and backend
3. **Database connection**: Verify DATABASE_URL is properly configured
4. **CORS errors**: Check backend CORS settings

### Environment Variables
Make sure all environment variables are properly set in both frontend and backend environments.