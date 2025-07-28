@echo off
echo Starting Cariacterologie Claude Full Stack Application...
echo.

echo Killing any existing processes on port 8000-8003...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :800') do (
    taskkill /F /PID %%a >nul 2>&1
)

echo Starting Python Backend API Server...
start "API Server" cmd /k "cd /d "%~dp0" && python api_server.py"

echo Waiting for backend to start...
timeout /t 8 /nobreak > nul

echo Starting React Frontend Development Server...
start "React Frontend" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo.
echo Both servers are starting...
echo Backend API: http://localhost:8001 (configured to avoid port conflicts)
echo React Frontend: http://localhost:5173
echo API Documentation: http://localhost:8001/docs
echo Health Check: http://localhost:8001/health
echo.
echo Press any key to close this window...
pause > nul