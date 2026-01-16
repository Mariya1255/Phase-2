# Quickstart Guide: Todo Full-Stack Web Application (Phase-2)

## Overview
This guide provides instructions for setting up, configuring, and running the Todo Full-Stack Web Application with Next.js frontend, FastAPI backend, Neon PostgreSQL database, and Better Auth authentication.

## Prerequisites

### System Requirements
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)
- pip (Python package manager)
- npm or yarn (Node.js package manager)
- Git for version control
- Docker (optional, for containerized deployment)

### Environment Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Install frontend dependencies:
   ```bash
   cd ../frontend
   npm install
   # or
   yarn install
   ```

## Environment Variables

### Backend (.env in backend directory)
```env
DATABASE_URL="postgresql://username:password@localhost:5432/todo_app"
BETTER_AUTH_SECRET="your-super-secret-jwt-key-here-make-it-long-and-random"
BETTER_AUTH_URL="http://localhost:3000"
DATABASE_SSL_REQUIRED=false
LOG_LEVEL="INFO"
```

### Frontend (.env in frontend directory)
```env
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
NEXTAUTH_SECRET="your-super-secret-jwt-key-here-make-it-long-and-random"
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
```

## Database Setup

### Neon PostgreSQL Configuration
1. Create a Neon PostgreSQL database instance
2. Update DATABASE_URL in backend/.env with your Neon connection string
3. Run database migrations:
   ```bash
   cd backend
   alembic upgrade head
   ```

### Local Database (Alternative)
1. Install and start PostgreSQL locally
2. Create a database for the application
3. Update DATABASE_URL in backend/.env:
   ```env
   DATABASE_URL="postgresql://username:password@localhost:5432/todo_app"
   ```

## Running the Application

### Development Mode

#### Backend (FastAPI)
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Run the FastAPI server:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

   Or using Python:
   ```bash
   python -m src.main
   ```

3. The backend API will be available at: `http://localhost:8000`

#### Frontend (Next.js)
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Run the Next.js development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

3. The frontend will be available at: `http://localhost:3000`

### Production Mode
1. Build the frontend:
   ```bash
   cd frontend
   npm run build
   ```

2. Start the backend server:
   ```bash
   cd backend
   gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

## API Endpoints

### Authentication Endpoints
- `POST /api/auth/signup` - User registration
- `POST /api/auth/signin` - User login
- `POST /api/auth/signout` - User logout

### Todo Management Endpoints
- `GET /api/todos` - Get user's todos
- `POST /api/todos` - Create new todo
- `GET /api/todos/{id}` - Get specific todo
- `PUT /api/todos/{id}` - Update todo
- `PATCH /api/todos/{id}/complete` - Toggle completion status
- `DELETE /api/todos/{id}` - Delete todo

## Authentication Flow

### User Registration
1. User navigates to `/auth/sign-up`
2. User enters email and password
3. Frontend sends request to `POST /api/auth/signup`
4. Backend creates user and returns JWT token
5. Frontend stores token and redirects to dashboard

### User Login
1. User navigates to `/auth/sign-in`
2. User enters email and password
3. Frontend sends request to `POST /api/auth/signin`
4. Backend validates credentials and returns JWT token
5. Frontend stores token and redirects to dashboard

### Protected Routes
1. All todo endpoints require Authorization header with Bearer token
2. Backend middleware validates JWT token
3. User ID extracted from token for data isolation
4. Requests without valid token return 401 Unauthorized

## Development Commands

### Backend Commands
```bash
# Run tests
cd backend && pytest

# Run with coverage
cd backend && pytest --cov=src

# Format code
cd backend && black src tests

# Check code quality
cd backend && flake8 src && mypy src

# Run migrations
cd backend && alembic revision --autogenerate -m "Description of changes"
cd backend && alembic upgrade head
```

### Frontend Commands
```bash
# Run development server
cd frontend && npm run dev

# Build for production
cd frontend && npm run build

# Run linting
cd frontend && npm run lint

# Run tests
cd frontend && npm run test

# Format code
cd frontend && npm run format
```

## Testing

### Backend Testing
1. Run unit tests:
   ```bash
   cd backend
   pytest tests/unit/
   ```

2. Run integration tests:
   ```bash
   cd backend
   pytest tests/integration/
   ```

3. Run all tests with coverage:
   ```bash
   cd backend
   pytest --cov=src --cov-report=html
   ```

### Frontend Testing
1. Run component tests:
   ```bash
   cd frontend
   npm run test
   ```

2. Run E2E tests (if configured):
   ```bash
   cd frontend
   npm run test:e2e
   ```

## Deployment

### Environment Configuration
1. Set up production environment variables
2. Configure SSL certificates for HTTPS
3. Set up reverse proxy (nginx, Apache, etc.)

### Docker Deployment
1. Build Docker images:
   ```bash
   # Backend
   docker build -f backend/Dockerfile -t todo-backend .

   # Frontend
   docker build -f frontend/Dockerfile -t todo-frontend .
   ```

2. Run with docker-compose:
   ```bash
   docker-compose up -d
   ```

### Cloud Deployment
1. Deploy backend to cloud provider (AWS, GCP, Azure, etc.)
2. Deploy frontend to CDN or static hosting service
3. Configure environment variables securely
4. Set up CI/CD pipeline for automated deployments

## Troubleshooting

### Common Issues

#### Database Connection
- Ensure DATABASE_URL is correctly configured
- Verify database server is running and accessible
- Check firewall settings if connecting remotely

#### Authentication Issues
- Verify BETTER_AUTH_SECRET is identical in both frontend and backend
- Ensure JWT tokens are being passed correctly in Authorization header
- Check that CORS settings allow frontend-backend communication

#### Frontend-Backend Communication
- Verify API endpoints are correctly configured
- Check that NEXT_PUBLIC_API_BASE_URL points to the correct backend URL
- Ensure CORS settings allow cross-origin requests

### Debugging Tips
1. Check backend logs for error messages
2. Use browser developer tools to inspect network requests
3. Verify environment variables are properly set
4. Test API endpoints directly using tools like Postman or curl

## Security Best Practices

### Secrets Management
- Never commit secrets to version control
- Use environment variables for sensitive data
- Rotate secrets regularly
- Use strong, random values for JWT secrets

### API Security
- Always validate input data
- Implement rate limiting for authentication endpoints
- Use HTTPS in production
- Sanitize user inputs to prevent injection attacks

### Data Protection
- Encrypt sensitive data in transit and at rest
- Implement proper user access controls
- Regular security audits and penetration testing
- Monitor for suspicious activity