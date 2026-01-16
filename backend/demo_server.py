import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import with error handling to demonstrate the API structure without database dependencies
try:
    # These imports would normally come from the API modules
    # But we'll define basic routes to demonstrate functionality
    from typing import Dict, List

    app = FastAPI(
        title="Todo API - Demo",
        description="Secure Todo Management API with JWT Authentication - DEMO VERSION",
        version="1.0.0"
    )

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

    @app.get("/")
    def read_root():
        return {
            "message": "Todo API is running!",
            "status": "operational",
            "note": "This is a demo version without database connectivity due to Python version compatibility issues. See README for full setup instructions."
        }

    @app.get("/health")
    def health_check():
        return {"status": "healthy", "database": "not connected (compatibility issue)"}

    # Define placeholder routes to show the API structure
    @app.get("/api/auth/demo")
    def auth_demo():
        return {
            "endpoints": [
                "POST /api/auth/signup",
                "POST /api/auth/signin",
                "POST /api/auth/signout"
            ],
            "description": "Authentication endpoints for user management"
        }

    @app.get("/api/todos/demo")
    def todos_demo():
        return {
            "endpoints": [
                "GET /api/todos/",
                "POST /api/todos/",
                "GET /api/todos/{id}",
                "PUT /api/todos/{id}",
                "PATCH /api/todos/{id}/complete",
                "DELETE /api/todos/{id}"
            ],
            "description": "Todo management endpoints"
        }

    print("Demo server ready to start. Note: This is a limited demo due to Python 3.13 compatibility issues with SQLAlchemy.")

except ImportError as e:
    print(f"Import error occurred: {e}")
    print("This indicates the compatibility issue with Python 3.13 and SQLAlchemy/SQLModel")

    # Create a minimal app just to show that the server can start
    app = FastAPI(
        title="Todo API - Minimal Demo",
        description="Minimal API demo due to compatibility issues",
        version="1.0.0"
    )

    @app.get("/")
    def read_root():
        return {
            "message": "Todo API - MINIMAL DEMO",
            "status": "operational (limited)",
            "error": "Full functionality requires Python 3.11 or 3.12 due to SQLAlchemy compatibility",
            "next_steps": [
                "Install Python 3.11 or 3.12",
                "Follow README.md installation instructions",
                "Run the full server with proper dependencies"
            ]
        }

    @app.get("/health")
    def health_check():
        return {"status": "limited demo only"}

if __name__ == "__main__":
    import uvicorn
    print("\nStarting FastAPI demo server...")
    print("Note: This is a limited demo version due to Python 3.13 compatibility issues.")
    print("For full functionality, please use Python 3.11 or 3.12 as detailed in README.md")
    print("Visit http://localhost:8000 to see the demo API in action\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)