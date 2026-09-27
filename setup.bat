@echo off
setlocal enabledelayedexpansion

REM PyStarter — Windows Setup Script
REM Installs dependencies, configures the environment, and starts the app.
REM Requirements: Python 3.13+, uv, Node.js 18+

echo.
echo  PyStarter Setup
echo  ===============
echo.

REM ── Check prerequisites ──

where python >nul 2>&1 || (
    echo [x] Python is not installed. Get it at https://python.org/downloads/
    exit /b 1
)

where uv >nul 2>&1 || (
    echo [x] uv is not installed. Get it at https://docs.astral.sh/uv/
    exit /b 1
)

where node >nul 2>&1 || (
    echo [x] Node.js is not installed. Get it at https://nodejs.org/
    exit /b 1
)

echo [+] Prerequisites found.

REM ── Backend setup ──

echo [+] Installing Python dependencies...
uv sync
if errorlevel 1 goto :error

cd backend

if not exist .env (
    copy .env.example .env >nul
    REM Generate a random secret key
    for /f "delims=" %%K in ('python -c "import secrets; print(secrets.token_urlsafe(64))"') do set "SECRET=%%K"
    powershell -Command "(Get-Content .env) -replace '^DJANGO_SECRET_KEY=.*', 'DJANGO_SECRET_KEY=!SECRET!' | Set-Content .env"
    echo [!] Created backend\.env with a generated secret key.
    echo [!] Edit backend\.env to add your ANTHROPIC_API_KEY for AI features.
) else (
    echo [+] backend\.env already exists, skipping.
)

echo [+] Running database migrations...
uv run python manage.py migrate --noinput
if errorlevel 1 goto :error

echo [+] Seeding curriculum (14 modules, 66 exercises)...
uv run python manage.py seed_curriculum
if errorlevel 1 goto :error

cd ..

REM ── Frontend setup ──

echo [+] Installing frontend dependencies...
cd frontend
call npm install
if errorlevel 1 goto :error
cd ..

REM ── Done ──

echo.
echo [+] Setup complete!
echo.
echo   To start PyStarter, open two terminals:
echo.
echo     Terminal 1 (backend):
echo       cd backend
echo       uv run python manage.py runserver 8002
echo.
echo     Terminal 2 (frontend):
echo       cd frontend
echo       npm run dev
echo.
echo   Then open http://localhost:5173 in your browser.
echo.
exit /b 0

:error
echo.
echo [x] Setup failed. Check the error above and try again.
exit /b 1
