@echo off
title MoodMate - AI Companion & Music
cd /d "%~dp0"

echo ========================================================
echo  Starting MoodMate Web Application...
echo ========================================================
echo.
echo  App URL: http://127.0.0.1:8000
echo  Press Ctrl+C to stop the server.
echo.

if exist "venv\Scripts\uvicorn.exe" (
    venv\Scripts\uvicorn.exe backend.main:app --host 127.0.0.1 --port 8000 --reload
) else (
    python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
)
pause

