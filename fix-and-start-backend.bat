@echo off
echo ========================================
echo  FIXING BACKEND - STEP BY STEP
echo ========================================
echo.

echo Step 1: Stopping all processes on port 8000...
echo.
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo Killing process %%a
    taskkill /F /PID %%a 2>nul
)

echo.
echo Step 2: Waiting for ports to be released...
timeout /t 3 /nobreak >nul

echo.
echo Step 3: Verifying port 8000 is free...
netstat -ano | findstr :8000 | findstr LISTENING
if %ERRORLEVEL% EQU 0 (
    echo WARNING: Port 8000 is still in use!
    echo Please close the applications manually and run this script again.
    pause
    exit /b 1
) else (
    echo SUCCESS: Port 8000 is now free!
)

echo.
echo Step 4: Starting Todo API backend...
cd /d "%~dp0backend"
echo Current directory: %CD%
echo.

if exist venv\Scripts\activate.bat (
    echo Activating virtual environment (venv)...
    call venv\Scripts\activate.bat
) else if exist backend_env\Scripts\activate.bat (
    echo Activating virtual environment (backend_env)...
    call backend_env\Scripts\activate.bat
) else (
    echo No virtual environment found. Using system Python.
)

echo.
echo Starting uvicorn server...
echo.
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
