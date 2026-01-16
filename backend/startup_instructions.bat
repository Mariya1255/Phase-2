#!/bin/bash
# startup_instructions.bat for Windows

echo "==============================================="
echo "TODO API BACKEND STARTUP INSTRUCTIONS"
echo "==============================================="

echo ""
echo "NOTICE: Due to Python 3.13 compatibility issues with SQLAlchemy,"
echo "you need to use Python 3.11 or 3.12 to run the full backend server."
echo ""

echo "Step 1: Check your Python version:"
echo "python --version"
echo ""

echo "Step 2: If using Python 3.13, please install Python 3.11 or 3.12"
echo "and then create a virtual environment:"
echo "python -m venv todo_backend_env"
echo "todo_backend_env\Scripts\activate"
echo ""

echo "Step 3: Install dependencies:"
echo "pip install -r requirements.txt"
echo ""

echo "Step 4: Run the server:"
echo "uvicorn src.main:app --reload --host 0.0.0.0 --port 8000"
echo ""

echo "Step 5: Visit http://localhost:8000 to see your running API"
echo ""

echo "For more details, see the README.md file in this directory."
echo "==============================================="