@echo off
echo Stopping all processes on port 8000...
taskkill /F /PID 3656 2>nul
taskkill /F /PID 12556 2>nul
taskkill /F /PID 5748 2>nul
taskkill /F /PID 10524 2>nul
echo.
echo Waiting for ports to be released...
timeout /t 3 /nobreak >nul
echo.
echo Checking if port 8000 is free...
netstat -ano | findstr :8000
if %ERRORLEVEL% EQU 0 (
    echo WARNING: Port 8000 is still in use!
    echo Please manually close the applications using port 8000.
) else (
    echo SUCCESS: Port 8000 is now free!
)
echo.
pause
