import sys
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from dotenv import load_dotenv

# Import exception handlers
from .exception_handlers import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)

# Load environment variables
load_dotenv()

def create_app() -> FastAPI:
    app = FastAPI(
        title="Todo API",
        description="Secure Todo Management API with JWT Authentication",
        version="1.0.0"
    )

    # Register exception handlers to ensure proper JSON responses
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

    # Try to import and include API routes
    try:
        from .api.auth import router as auth_router
        from .api.todos import router as todos_router

        # Include API routes
        app.include_router(auth_router, prefix="/api/auth", tags=["authentication"])
        app.include_router(todos_router, prefix="/api/todos", tags=["todos"])

        print("API routes successfully loaded")
    except ImportError as e:
        print(f"Warning: Could not import API routes: {e}")
        print("This may be due to Python 3.13 compatibility issues with SQLModel/SQLAlchemy.")
        print("The server will start with basic endpoints only.")

        # Create fallback auth routes that return meaningful error messages
        @app.post("/api/auth/signin")
        def signin_fallback():
            from fastapi.responses import JSONResponse
            from fastapi import status
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={"detail": "Authentication service temporarily unavailable. Please check server logs."}
            )

        @app.post("/api/auth/signup")
        def signup_fallback():
            from fastapi.responses import JSONResponse
            from fastapi import status
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={"detail": "Registration service temporarily unavailable. Please check server logs."}
            )

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