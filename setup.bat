@echo off
REM Native Windows cannot enforce the executor resource/process controls.
echo Use Docker Desktop with Linux containers for PyStarter on Windows.
echo From PowerShell in this folder, run:
echo   powershell -ExecutionPolicy Bypass -File .\init.ps1
echo   docker compose up --build -d
echo Then open http://localhost:8080
exit /b 0
