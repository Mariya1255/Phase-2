@echo off
echo Starting FastAPI Backend Server...
echo.
cd /d "%~dp0backend"
echo Current directory: %CD%
echo.
echo Activating virtual environment...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else if exist backend_env\Scripts\activate.bat (
    call backend_env\Scripts\activate.bat
) else (
    echo WARNING: No virtual environment found. Using system Python.
)
echo.
echo Starting uvicorn server...
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
