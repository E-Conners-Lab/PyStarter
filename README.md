# PyStarter
<img width="1499" height="770" alt="Screenshot 2026-03-03 at 9 46 59 PM" src="https://github.com/user-attachments/assets/2f453ac4-816e-4ac8-9d22-d045875871e8" />





A beginner-friendly Python training platform that teaches programming through interactive lessons, sandboxed coding exercises, and AI-powered hints.

## Features

- **14-module curriculum** covering Python fundamentals through network automation
- **4 exercise types**: fill-in-the-blank, fix-the-bug, write code, predict the output
- **Sandboxed code execution** — user code runs in a restricted environment with import/builtin restrictions and timeouts
- **Progressive hint system** with XP penalties (2 levels: free nudge + deeper hint at 10% XP cost)
- **AI-powered help** via Claude — contextual hints, code critique, and error explanations
- **XP and belt progression** — earn XP for completing exercises, level up through belt ranks
- **Monaco code editor** with syntax highlighting in the browser

## Tech Stack

| Layer       | Stack                                          |
|-------------|------------------------------------------------|
| Backend     | Django 6, Django REST Framework, SimpleJWT      |
| Frontend    | React 19, TypeScript, Vite                     |
| Styling     | TailwindCSS (dark theme)                       |
| State       | Zustand (auth) + TanStack Query (data fetching) |
| Code Editor | Monaco Editor                                  |
| Markdown    | react-markdown + remark-gfm                   |
| AI          | Anthropic Claude API                           |
| Database    | SQLite (dev) / PostgreSQL (prod)               |

## Quick Start

### Prerequisites

- [Python 3.13+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- [Node.js 18+](https://nodejs.org/)

### 1. Clone the repository

```bash
git clone https://github.com/E-Conners-Lab/PyStarter.git
cd PyStarter
```

### 2. Start the backend

```bash
cd backend
cp .env.example .env          # fill in your API keys (see AI Setup below)
uv run python manage.py migrate
uv run python manage.py seed_curriculum
uv run python manage.py runserver 8002
```

### 3. Start the frontend (in a separate terminal)

```bash
cd PyStarter/frontend
npm install
npm run dev
```

### 4. Start learning

Open http://localhost:5173, register an account, and start learning.

## Curriculum

| #  | Module                       | Topics                                                         |
|----|------------------------------|----------------------------------------------------------------|
| 1  | Your First Program           | `print()`, strings, basic output                               |
| 2  | Variables & Data Types       | Assignment, int/float/str, `type()`                            |
| 3  | Making Decisions             | if/elif/else, comparisons, booleans                            |
| 4  | Loops                        | for, while, `range()`, break/continue                          |
| 5  | Functions                    | def, parameters, return values, scope                          |
| 6  | Lists & Tuples               | Indexing, slicing, methods, immutability                       |
| 7  | Dictionaries                 | Key-value pairs, methods, iteration                            |
| 8  | String Magic                 | Slicing, methods, f-strings, split/join                        |
| 9  | Writing Cleaner Code         | Ternary, enumerate, comprehensions, walrus operator            |
| 10 | Python for Network Engineers | `ipaddress`, CLI output parsing, JSON configs                  |
| 11 | Handling Errors              | try/except, common exceptions, else/finally                    |
| 12 | User Input & While Loops     | `input()`, type conversion, sentinel values, break/continue    |
| 13 | Regular Expressions          | `re.search()`, `re.findall()`, `re.sub()`, groups, patterns    |
| 14 | Building a Network Toolkit   | Capstone: validation functions, parsing pipelines, audit reports |

Each module has 4 lessons (concept, interactive sandbox, graded exercises, "Try It Yourself" challenges) and 4-6 exercises. 66 exercises total across 56 lessons.

## AI Setup

The AI features (contextual hints, code critique, error explanations) need an LLM. Everything else works without one. You have two options:

```bash
cd backend
cp .env.example .env
```

### Option A: Anthropic API (recommended)

Edit `backend/.env`:

```
ANTHROPIC_API_KEY=sk-ant-...
```

To get a key: sign up at [console.anthropic.com](https://console.anthropic.com), go to **API Keys**, and create one. API calls are billed to your account — each hint costs a fraction of a cent.

### Option B: Local LLM (free, private, offline)

You can run a local model instead of using the Anthropic API. Any tool that provides an OpenAI-compatible API will work.

**Using [Ollama](https://ollama.com):**

1. Install Ollama and pull a model:
   ```bash
   ollama pull llama3.2
   ```

2. Edit `backend/.env`:
   ```
   ANTHROPIC_API_KEY=not-needed
   ANTHROPIC_MODEL=llama3.2
   ANTHROPIC_BASE_URL=http://localhost:11434/v1
   ```

**Using [LM Studio](https://lmstudio.ai):**

1. Download a model in LM Studio and start the local server
2. Edit `backend/.env`:
   ```
   ANTHROPIC_API_KEY=not-needed
   ANTHROPIC_MODEL=<your-model-name>
   ANTHROPIC_BASE_URL=http://localhost:1234/v1
   ```

**Using any OpenAI-compatible server** (llama.cpp, vLLM, text-generation-webui, etc.):

Set `ANTHROPIC_BASE_URL` to your server's URL and `ANTHROPIC_MODEL` to the model name it expects. The `ANTHROPIC_API_KEY` can be any non-empty string if your server doesn't require auth.

> **Note:** Hint quality depends on the model. Smaller local models (~3B–8B parameters) work but may give less precise hints than Claude. For the best experience, use a 13B+ model or the Anthropic API.

## Docker Deployment

Run the full stack with Docker Compose:

```bash
cp backend/.env.example .env    # fill in DJANGO_SECRET_KEY, ALLOWED_HOSTS, etc.

docker compose build
docker compose up -d
```

This starts 4 services:

| Service    | Description                              |
|------------|------------------------------------------|
| `db`       | PostgreSQL 16                            |
| `backend`  | Django + Gunicorn (3 workers)            |
| `frontend` | Built React app served by nginx          |
| `nginx`    | Reverse proxy (`/api/` → backend, `/` → frontend) |

The app is available at `http://localhost` (or the port set via `NGINX_PORT`).

Migrations run automatically on container start via the entrypoint script. To seed curriculum data:

```bash
docker compose exec backend python manage.py seed_curriculum
```

## Testing

```bash
# End-to-end tests (Playwright, 99 tests)
cd frontend
npx playwright test

# Backend unit tests
cd backend
uv run python manage.py test
```

## Database Backups

Back up the PostgreSQL database with the included script:

```bash
./scripts/backup-db.sh
```

Backups are saved to `./backups/` as timestamped gzipped SQL dumps (e.g. `pystarter_20260304_120000.sql.gz`).

**Automatic daily backups with cron:**

```bash
0 2 * * * cd /path/to/project && PRUNE_DAYS=30 ./scripts/backup-db.sh >> /var/log/pystarter-backup.log 2>&1
```

**Restore from backup:**

```bash
gunzip -c backups/pystarter_20260304_120000.sql.gz | docker compose exec -T db psql -U pystarter pystarter
```

## Sandbox Security

User-submitted code runs in a restricted Python sandbox (`backend/apps/executor/sandbox.py`) with these safeguards:

- **Import whitelist** — only safe standard library modules (math, random, string, collections, datetime, json, re, typing, copy, itertools, functools, textwrap, ipaddress)
- **Blocked builtins** — exec, eval, compile, open, \_\_import\_\_ (restricted), getattr, setattr, and other dangerous functions are removed or replaced
- **Replaced input()** — reads from a pre-loaded input queue instead of stdin
- **5-second timeout** — execution is killed after 5 seconds
- **Memory limit** — resource limits prevent memory exhaustion
- **Recursion limit** — set to 200 to prevent stack overflow

This is appropriate for a single-tenant training platform. For untrusted multi-tenant use, code execution should be moved to containerized isolation (e.g. gVisor, Firecracker, or a dedicated code execution service).

## License

Personal use only. See [LICENSE](LICENSE) for details.
