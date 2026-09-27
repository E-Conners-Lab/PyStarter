# PyStarter

**Learn Python. Write Code. Level Up.**

A self-hosted training platform that teaches Python from scratch through interactive lessons, a sandboxed code editor, graded exercises, and AI-powered tutoring. 14 modules, 56 lessons, 66 graded exercises — complete and ready to run.

<img width="1499" height="770" alt="PyStarter Dashboard" src="https://github.com/user-attachments/assets/2f453ac4-816e-4ac8-9d22-d045875871e8" />

---

## Open source, and unmaintained

PyStarter is **MIT licensed** and the full source is in this repo. Clone it, fork it, modify it, teach with it, rebrand it, sell it — whatever you want. No attribution required beyond keeping the copyright notice in `LICENSE`.

**It is not actively maintained.** Treat this as a finished artifact, not a living project: issues and pull requests may go unanswered, and there are no promises of future releases, security patches, or dependency bumps. **If you deploy it, you own it** — updating Django, patching CVEs, rotating keys, and fixing whatever breaks is yours. Fork it rather than depending on this repo staying current.

It is a complete, working codebase with a test suite (Django unit tests + 99 Playwright E2E tests) and CI, so it is a reasonable base to build on.

---

## Install

Two paths. **Docker** is the fastest way to just use it. **From source** is what you want if you plan to change anything.

### Option A — Docker (no toolchain, ~500 MB of images)

Runs PostgreSQL, Django, React, and nginx. Migrations and curriculum seeding happen automatically on first start.

```bash
# 1. Download and unzip the runner bundle
curl -LO https://github.com/E-Conners-Lab/PyStarter/releases/download/v1.0.6/pystarter-v1.0.6-runner.zip
unzip pystarter-v1.0.6-runner.zip -d pystarter
cd pystarter

# 2. Generate .env (Django secret key, optional Anthropic key)
./init.sh

# 3. Start
docker compose up -d
```

Open **http://localhost**, sign up, and Module 1 is unlocked.

`./init.sh` asks for an Anthropic API key and you can press Enter to skip it — everything except the AI features works without one.

Stop with `docker compose down` (keeps your data) or `docker compose down -v` (deletes the database).

Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/) or Docker Engine + Compose v2. Images are `linux/amd64` and `linux/arm64`.

### Option B — From source

Needs [Python 3.13+](https://www.python.org/downloads/), [uv](https://docs.astral.sh/uv/), and [Node.js 18+](https://nodejs.org/). No configuration file is required — the dev settings use SQLite and sensible defaults.

```bash
git clone https://github.com/E-Conners-Lab/PyStarter.git
cd PyStarter
```

**Backend** (terminal 1):

```bash
cd backend
uv run python manage.py migrate
uv run python manage.py seed_curriculum
uv run python manage.py runserver 8002
```

**Frontend** (terminal 2):

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173**. Vite proxies `/api` to the backend on port 8002.

To enable AI features, `cp backend/.env.example backend/.env` and set `ANTHROPIC_API_KEY`. For production deployment from source, see the compose file and `CONTRIBUTING.md`.

---

## AI setup (optional)

Hints, code critique, and error explanations call an LLM. Everything else — lessons, exercises, the sandbox, XP, belts — works without one.

**Anthropic API:** put `ANTHROPIC_API_KEY=sk-ant-...` in `.env` ([get a key](https://console.anthropic.com)). Calls are billed to your account; a hint costs roughly a cent on the default model, `claude-opus-5`. For cheaper hints set `ANTHROPIC_MODEL=claude-haiku-4-5`. Always use an alias like these, never a date-suffixed snapshot ID, so the model does not retire out from under you.

**Local model (free, offline):** point `ANTHROPIC_BASE_URL` at any OpenAI-compatible server and set `ANTHROPIC_MODEL` to its model name.

```bash
# Ollama
ANTHROPIC_API_KEY=not-needed
ANTHROPIC_MODEL=llama3.2
ANTHROPIC_BASE_URL=http://host.docker.internal:11434/v1   # http://localhost:11434/v1 from source
```

Hint quality tracks model quality; models under ~13B give noticeably vaguer hints.

---

## What's inside

**Built-in code editor** — Monaco (the VS Code engine) in the browser, with syntax highlighting and auto-indent.

**Sandboxed execution** — student code runs with an import whitelist, blocked builtins, a 5-second timeout, and memory limits.

**4 exercise types** — fill in the blank, fix the bug, write code, predict the output.

**Progressive hints** — first hint free, second costs 10% of the exercise XP.

**Run vs Submit** — "Run" tests against visible cases with no stakes; "Submit" grades against hidden cases too and awards XP.

**XP and belts** — 8 ranks, White through Black.

### Curriculum

| # | Module | What students learn |
|---|--------|---------------------|
| 1 | Your First Program | `print()`, strings, basic output |
| 2 | Variables & Data Types | Assignment, int/float/str, `type()` |
| 3 | Making Decisions | if/elif/else, comparisons, boolean logic |
| 4 | Loops | for, while, `range()`, break/continue |
| 5 | Functions | def, parameters, return values, scope |
| 6 | Lists & Tuples | Indexing, slicing, methods, immutability |
| 7 | Dictionaries | Key-value pairs, methods, iteration |
| 8 | String Magic | Slicing, methods, f-strings, split/join |
| 9 | Writing Cleaner Code | Ternary, enumerate, comprehensions, walrus operator |
| 10 | Python for Network Engineers | `ipaddress` module, CLI output parsing, JSON configs |
| 11 | Handling Errors | try/except, common exceptions, else/finally |
| 12 | User Input & While Loops | `input()`, type conversion, sentinel values |
| 13 | Regular Expressions | `re.search()`, `re.findall()`, `re.sub()`, groups |
| 14 | Building a Network Toolkit | Capstone: validation, parsing pipelines, audit reports |

---

## Making it yours

| To change… | Edit |
|---|---|
| Lessons, exercises, hints, test cases | `backend/apps/curriculum/management/commands/seed_curriculum.py`, then re-seed |
| Sandbox limits and the import whitelist | `backend/apps/executor/sandbox.py` |
| AI prompts and behavior | `backend/apps/ai/` |
| XP values and belt thresholds | `backend/apps/accounts/` |
| UI, theme, pages | `frontend/src/` (TailwindCSS, dark theme) |
| Module icons | `MODULE_ICONS` in `frontend/src/pages/Dashboard.tsx` |

Re-seeding after curriculum edits rebuilds curriculum content — flush first if you have existing data.

`CONTRIBUTING.md` documents the architecture, data model, conventions, test commands, and how the Docker images are built and released.

---

## Tech stack

| Layer | Technology |
|-------|------------|
| Backend | Django 6, Django REST Framework, SimpleJWT |
| Frontend | React 19, TypeScript, Vite |
| Styling | TailwindCSS (dark theme) |
| Code editor | Monaco Editor |
| State | Zustand + TanStack Query |
| AI | Anthropic Claude API, or any OpenAI-compatible LLM |
| Database | SQLite (development) / PostgreSQL (production) |
| Deployment | Docker Compose with nginx reverse proxy |
| Testing | Django unit tests + 99 Playwright E2E tests |
| CI | GitHub Actions |

Pre-built images: `ghcr.io/e-conners-lab/pystarter-backend:1.0.6` and `ghcr.io/e-conners-lab/pystarter-frontend:1.0.6` (both `linux/amd64` + `linux/arm64`). `/api/v1/health/` reports the running version.

---

## License

MIT — see [LICENSE](LICENSE). Provided as is, without warranty of any kind.

Originally built by [**The Tech-E**](https://www.thetech-e.com).
