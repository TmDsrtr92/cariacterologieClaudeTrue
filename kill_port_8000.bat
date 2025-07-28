@echo off
echo Checking for processes on port 8000...
netstat -ano | findstr :8000

echo.
echo Killing processes on port 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    echo Killing PID %%a
    taskkill /F /PID %%a 2>nul
)

echo.
echo Port 8000 should now be free.
pause