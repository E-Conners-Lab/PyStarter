#!/bin/sh
set -e

# PyStarter — Local Setup Script
# Installs dependencies, configures the environment, and starts the app.
# Requirements: Python 3.13+, uv, Node.js 18+

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info()  { printf "${GREEN}[+]${NC} %s\n" "$1"; }
warn()  { printf "${YELLOW}[!]${NC} %s\n" "$1"; }
error() { printf "${RED}[x]${NC} %s\n" "$1"; exit 1; }

# ── Check prerequisites ──

command -v python3 >/dev/null 2>&1 || error "Python 3 is not installed. Get it at https://python.org/downloads/"
command -v uv >/dev/null 2>&1      || error "uv is not installed. Get it at https://docs.astral.sh/uv/"
command -v node >/dev/null 2>&1    || error "Node.js is not installed. Get it at https://nodejs.org/"

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
NODE_VERSION=$(node -v | sed 's/v//' | cut -d. -f1)

info "Python $PYTHON_VERSION, Node $NODE_VERSION detected"

# ── Backend setup ──

info "Installing Python dependencies..."
uv sync

cd backend

if [ ! -f .env ]; then
    cp .env.example .env
    # Generate a random Django secret key
    SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(64))")
    if [ "$(uname)" = "Darwin" ]; then
        sed -i '' "s/^DJANGO_SECRET_KEY=.*/DJANGO_SECRET_KEY=$SECRET/" .env
    else
        sed -i "s/^DJANGO_SECRET_KEY=.*/DJANGO_SECRET_KEY=$SECRET/" .env
    fi
    warn "Created backend/.env with a generated secret key."
    warn "Edit backend/.env to add your ANTHROPIC_API_KEY for AI features."
else
    info "backend/.env already exists, skipping."
fi

info "Running database migrations..."
uv run python manage.py migrate --noinput

info "Seeding curriculum (14 modules, 66 exercises)..."
uv run python manage.py seed_curriculum

cd ..

# ── Frontend setup ──

info "Installing frontend dependencies..."
cd frontend
npm install
cd ..

# ── Done ──

printf "\n"
info "Setup complete!"
printf "\n"
echo "  To start PyStarter, open two terminals:"
echo ""
echo "    Terminal 1 (backend):"
echo "      cd backend"
echo "      uv run python manage.py runserver 8002"
echo ""
echo "    Terminal 2 (frontend):"
echo "      cd frontend"
echo "      npm run dev"
echo ""
echo "  Then open http://localhost:5173 in your browser."
printf "\n"
