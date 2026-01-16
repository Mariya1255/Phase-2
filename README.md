# Todo Full-Stack Web Application

A secure, multi-user todo management application built with Next.js, FastAPI, and Neon PostgreSQL.

## Features

- User registration and authentication with JWT tokens
- Secure todo management with user isolation
- Responsive web interface
- RESTful API endpoints
- Modern tech stack with Next.js 16+ and FastAPI

## Tech Stack

- **Frontend**: Next.js 16+ with App Router
- **Backend**: Python FastAPI
- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLModel
- **Authentication**: Better Auth with JWT

## Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL (or use Docker Compose)

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   cd ../frontend
   npm install
   ```
3. Set up environment variables (copy `.env.example` to `.env`)
4. Start the development servers:
   ```bash
   # Terminal 1: Start backend
   cd backend
   uvicorn src.main:app --reload

   # Terminal 2: Start frontend
   cd frontend
   npm run dev
   ```

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/signin` - Login user
- `POST /api/auth/signout` - Logout user

### Todo Management
- `GET /api/todos` - Get all user's todos
- `POST /api/todos` - Create new todo
- `GET /api/todos/{id}` - Get specific todo
- `PUT /api/todos/{id}` - Update todo
- `PATCH /api/todos/{id}/complete` - Toggle completion
- `DELETE /api/todos/{id}` - Delete todo

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Secret key for JWT signing
- `BETTER_AUTH_SECRET`: Secret for Better Auth
- `NEXT_PUBLIC_API_URL`: Frontend API URL

## Running with Docker

```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Health check: http://localhost:8000/health