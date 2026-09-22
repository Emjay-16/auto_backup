@echo off
cd /d "%~dp0"
echo Starting Auto Backup API Server (Port 8000)...
.\.venv\Scripts\python.exe -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
pause

