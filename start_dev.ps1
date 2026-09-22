Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "   Starting Auto Backup (Mock Mode)" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "[1/2] Starting API on http://localhost:8000 ..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$scriptDir'; .\.venv\Scripts\python.exe -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload"

Write-Host "[2/2] Starting Frontend on http://localhost:3000 ..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$scriptDir\front_end\my_app'; npm run dev"

Write-Host ""
Write-Host "Both API and Frontend are starting in separate windows!" -ForegroundColor Green
Write-Host "- API: http://localhost:8000 (Docs: http://localhost:8000/docs)" -ForegroundColor White
Write-Host "- Web: http://localhost:3000" -ForegroundColor White
Write-Host "- Default Login: admin / admin (or system / system)" -ForegroundColor White
Write-Host "==============================================" -ForegroundColor Cyan

