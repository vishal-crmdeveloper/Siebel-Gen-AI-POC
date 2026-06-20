@echo off
echo ===================================================
echo   Oracle Siebel x Gen AI - Startup Script
echo ===================================================
echo.

echo [1/2] Starting Ollama AI Engine in the background...
set OLLAMA_REQUEST_TIMEOUT=600
start "Ollama Background Process" /MIN ollama serve

echo Waiting a few seconds for Ollama to initialize...
timeout /t 5 /nobreak >nul

echo.
echo [2/2] Starting FastAPI Server...
echo The web dashboard will be available at: http://localhost:8000
echo.
echo NOTE: Do not close this window while you are using the app.
echo.

cd /d "%~dp0"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

pause
