import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .exception_handlers import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Add the current directory to the Python path to allow relative imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

# Import API routers - these are in the api subdirectory relative to this file
from api.auth import router as auth_router
from api.todos import router as todos_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="Todo API",
        description="Secure Todo Management API with JWT Authentication",
        version="1.0.0"
    )

    # Register exception handlers to ensure JSON responses
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)

    # CORS configuration
    origins = [
        "http://localhost:3000",  # Next.js default port
        "http://127.0.0.1:3000",
        "http://localhost:3001",  # Alternative Next.js port
        "http://127.0.0.1:3001",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(auth_router, prefix="/api/auth", tags=["authentication"])
    app.include_router(todos_router, prefix="/api/todos", tags=["todos"])

    @app.get("/")
    def read_root():
        return {"message": "Todo API is running!"}

    @app.get("/health")
    def health_check():
        return {"status": "healthy"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)