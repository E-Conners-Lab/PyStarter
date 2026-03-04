# PyStarter
<img width="1294" height="664" alt="Screenshot 2026-03-03 at 7 14 10 PM" src="https://github.com/user-attachments/assets/dbdc5128-0f73-4169-a767-4f9a99b5ca45" />

A beginner-friendly Python training platform that teaches programming through interactive lessons, sandboxed coding exercises, and AI-powered hints.

## Features

- **10-module curriculum** covering Python fundamentals through network automation
- **4 exercise types**: fill-in-the-blank, fix-the-bug, write code, predict the output
- **Sandboxed code execution** — user code runs in a restricted environment with import/builtin restrictions and timeouts
- **Progressive hint system** with XP penalties (5 levels from gentle nudge to full solution)
- **AI-powered help** via Claude — contextual hints, code critique, and error explanations
- **XP and belt progression** — earn XP for completing exercises, level up through belt ranks
- **Monaco code editor** with syntax highlighting in the browser

## Tech Stack

| Layer | Stack |
|-------|-------|
| Backend | Django 6, Django REST Framework, SimpleJWT |
| Frontend | React 19, TypeScript, Vite |
| Styling | TailwindCSS (dark theme) |
| State | Zustand (auth) + TanStack Query (data fetching) |
| Code Editor | Monaco Editor |
| AI | Anthropic Claude API |
| Database | SQLite (dev) / PostgreSQL (prod) |

## Quick Start

### Prerequisites

- Python 3.13+ with [uv](https://docs.astral.sh/uv/)
- Node.js 18+

### Backend

```bash
cd backend
cp .env.example .env          # fill in your API keys
uv run python manage.py migrate
uv run python manage.py seed_curriculum
uv run python manage.py runserver 8002
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173, register an account, and start learning.

## Curriculum

| # | Module | Topics |
|---|--------|--------|
| 1 | Your First Program | `print()`, strings, basic output |
| 2 | Variables & Data Types | Assignment, int/float/str, `type()` |
| 3 | Making Decisions | if/elif/else, comparisons, booleans |
| 4 | Loops | for, while, `range()`, break/continue |
| 5 | Functions | def, parameters, return values, scope |
| 6 | Lists & Tuples | Indexing, slicing, methods, immutability |
| 7 | Dictionaries | Key-value pairs, methods, iteration |
| 8 | String Magic | Slicing, methods, f-strings, split/join |
| 9 | Writing Cleaner Code | Ternary, enumerate, comprehensions, walrus operator |
| 10 | Python for Network Engineers | `ipaddress`, CLI output parsing, JSON configs |

Each module has 3 lessons (concept, interactive sandbox, graded exercises) and 4 exercises.

## Environment Variables

Copy `backend/.env.example` to `backend/.env`:

```
DJANGO_SECRET_KEY=<random-secret>
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-haiku-4-5-20241001
```

## Testing

```bash
# End-to-end tests (Playwright, 30 tests)
cd frontend
npx playwright test

# Backend unit tests
cd backend
uv run python manage.py test
```

## License

[MIT](LICENSE)
