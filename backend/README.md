# Backend Server - Todo API

This is a Python-based backend server built with FastAPI, designed to provide a secure Todo Management API with JWT Authentication. The backend follows modern development practices and integrates with a Neon Serverless PostgreSQL database.

## Technologies Used

- **Python 3.11+** - Programming language
- **FastAPI** - Modern, fast web framework for building APIs with Python 3.7+ based on standard Python type hints
- **SQLModel** - SQL toolkit and ORM that combines SQLAlchemy and Pydantic, designed for building APIs with FastAPI
- **PostgreSQL** - Object-relational database system (using Neon Serverless)
- **Uvicorn** - Lightning-fast ASGI server implementation, using uvloop and httptools
- **Pydantic** - Data validation and settings management using Python type hints
- **Better Auth** - Authentication solution for the application
- **Alembic** - Database migration tool
- **Passlib** - Password hashing library
- **Python-JOSE** - JavaScript Object Signing and Encryption library for JWT handling

## Project Structure

```
backend/
├── alembic/                 # Database migration scripts
├── alembic.ini             # Alembic configuration
├── pyproject.toml          # Project metadata and configuration
├── requirements.txt        # Full list of dependencies
├── requirements_minimal.txt # Minimal dependencies for basic functionality
├── src/                    # Source code directory
│   ├── api/                # API route definitions
│   │   ├── auth.py         # Authentication endpoints (signup, signin, signout)
│   │   └── todos.py        # Todo management endpoints
│   ├── database/           # Database connection and configuration
│   ├── lib/                # Utility functions
│   ├── main.py             # Main application entry point
│   ├── middleware/         # Middleware components (auth, cors, etc.)
│   ├── models/             # Data models and schemas
│   └── services/           # Business logic implementations
├── tests/                  # Test files
└── README.md               # This file
```

## Features

- **User Authentication**: Secure signup and signin with JWT token-based authentication
- **Todo Management**: CRUD operations for managing personal todo items
- **User Isolation**: Todos are isolated by user - users can only access their own todos
- **RESTful API**: Well-designed REST API endpoints following best practices
- **CORS Support**: Configured to work with frontend applications
- **Database Integration**: PostgreSQL database with SQLModel ORM
- **Request Validation**: Automatic request validation with Pydantic models

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register a new user
- `POST /api/auth/signin` - Authenticate a user and return access token
- `POST /api/auth/signout` - Sign out a user

### Todo Management
- `GET /api/todos/` - Get all todos for the authenticated user
- `POST /api/todos/` - Create a new todo for the authenticated user
- `GET /api/todos/{todo_id}` - Get a specific todo by ID
- `PUT /api/todos/{todo_id}` - Update a specific todo by ID
- `PATCH /api/todos/{todo_id}/complete` - Toggle completion status of a todo
- `DELETE /api/todos/{todo_id}` - Delete a specific todo by ID

### Health Check
- `GET /` - Root endpoint with API status
- `GET /health` - Health check endpoint

## Prerequisites

- Python 3.11 or 3.12 (Python 3.13 has compatibility issues with SQLAlchemy)
- PostgreSQL database (Neon Serverless PostgreSQL recommended)
- pip (Python package installer)

## Installation and Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd backend
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

For full functionality (recommended):
```bash
pip install -r requirements.txt
```

For minimal setup (if facing PostgreSQL installation issues):
```bash
pip install -r requirements_minimal.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Backend Configuration
DATABASE_URL='postgresql://username:password@localhost:5432/database_name'
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Better Auth Configuration
BETTER_AUTH_SECRET=your-better-auth-secret
BETTER_AUTH_URL=http://localhost:8000

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 5. Run Database Migrations

```bash
alembic upgrade head
```

### 6. Start the Server

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Or run directly:

```bash
python src/main.py
```

The server will start at `http://localhost:8000`

## Known Issues

### Python 3.13 Compatibility Issue
There is a known compatibility issue with Python 3.13 due to SQLAlchemy not supporting the latest Python version yet. The error manifests as:
```
AssertionError: Class <class 'sqlalchemy.sql.elements.SQLCoreOperations'> directly inherits TypingOnly but has additional attributes {'__static_attributes__', '__firstlineno__'}.
```

**Solution**: Use Python 3.11 or 3.12 instead of Python 3.13.

To check your Python version:
```bash
python --version
```

### Alternative: Use SQLite for Development
If you must use Python 3.13, you can modify the application to use SQLite temporarily for development:

1. Install SQLite dependencies:
```bash
pip install sqlite3
```

2. Update your `.env` file to use SQLite:
```env
DATABASE_URL=sqlite:///./todo_app.db
```

3. You may need to install the `aiosqlite` driver for async operations:
```bash
pip install aiosqlite
```

However, for the best experience, we strongly recommend using Python 3.11 or 3.12.

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

The project uses Black for code formatting:

```bash
black src/
```

### Environment Variables for Development

For development purposes, you can use SQLite instead of PostgreSQL by changing the DATABASE_URL:

```env
DATABASE_URL='sqlite:///./todo.db'
```

## Security Features

- JWT token-based authentication
- Password hashing with bcrypt
- Secure token handling
- User isolation (users can only access their own data)
- Input validation and sanitization
- CORS configuration for frontend integration

## Production Deployment

For production deployment:
- Use strong, unique values for SECRET_KEY and BETTER_AUTH_SECRET
- Enable HTTPS
- Use environment variables for sensitive configuration
- Set up proper logging
- Monitor performance and security
- Regular dependency updates

## Troubleshooting

### Common Issues:

1. **Database Connection Errors**: Verify your DATABASE_URL is correctly configured
2. **Import Errors**: Check Python version compatibility (avoid Python 3.13)
3. **Port Already in Use**: Change the port in the uvicorn command
4. **Missing Dependencies**: Reinstall using requirements.txt
5. **"'uvicorn' is not recognized"**: Install uvicorn with `pip install "uvicorn[standard]"`

### Python Version Solution (Most Important)

If you're experiencing the SQLAlchemy compatibility issue with Python 3.13, here's how to solve it:

#### Option 1: Downgrade Python (Recommended)
1. Install Python 3.11 or 3.12 from [python.org](https://www.python.org/downloads/)
2. Verify the installation: `python --version`
3. Create a new virtual environment:
   ```bash
   python -m venv todo_backend_env
   todo_backend_env\Scripts\activate  # On Windows
   ```
4. Install dependencies: `pip install -r requirements.txt`
5. Run the server: `uvicorn src.main:app --reload --host 0.0.0.0 --port 8000`

#### Option 2: Use Docker (Alternative)
If you have Docker installed:
1. Create a Dockerfile:
   ```Dockerfile
   FROM python:3.11-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install -r requirements.txt

   COPY . .

   CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```
2. Build and run: `docker build -t todo-backend . && docker run -p 8000:8000 todo-backend`

### Successful Server Startup (Once Fixed)

When the Python compatibility issue is resolved, you should see output similar to:

```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Started reloader process [PID]
INFO:     Started server process [PID]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

At this point, visit `http://localhost:8000` to access your fully functional Todo API.

### For Windows Users:
- Use `venv\Scripts\activate` instead of `source venv/bin/activate`
- Make sure you have Microsoft Visual C++ Build Tools installed for some dependencies

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Run tests to ensure everything works
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request