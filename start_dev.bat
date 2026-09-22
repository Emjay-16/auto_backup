@echo off
cd /d "%~dp0"
echo ==============================================
echo   Starting Auto Backup (Mock Mode)
echo ==============================================
echo [1/2] Starting API on http://localhost:8000 ...
start "Auto Backup API" cmd /k ".\.venv\Scripts\python.exe -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload"

echo [2/2] Starting Frontend on http://localhost:3000 ...
start "Auto Backup Web" cmd /k "cd /d "%~dp0front_end\my_app" && npm run dev"

echo.
echo Both API and Web are starting in separate windows!
echo - API: http://localhost:8000 (Docs: http://localhost:8000/docs)
echo - Web: http://localhost:3000
echo - Default login: admin / admin (or system / system)
echo ==============================================
pause

