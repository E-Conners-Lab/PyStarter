# PyStarter

**Learn Python. Write Code. Level Up.**

A self-hosted training platform that teaches Python from scratch through interactive lessons, a built-in code editor, graded exercises, and AI-powered tutoring. 14 modules, 56 lessons, 66 graded exercises — for local learning.

<img width="1499" height="770" alt="PyStarter Dashboard" src="https://github.com/user-attachments/assets/2f453ac4-816e-4ac8-9d22-d045875871e8" />

---

## Open source, and unmaintained

PyStarter is **MIT licensed** and the full source is in this repo. Clone it, fork it, modify it, teach with it, rebrand it, sell it — whatever you want. No attribution required beyond keeping the copyright notice in `LICENSE`.

**It is not actively maintained.** Treat this as a finished artifact, not a living project: issues and pull requests may go unanswered, and there are no promises of future releases, security patches, or dependency bumps. **If you deploy it, you own it** — updating Django, patching CVEs, rotating keys, and fixing whatever breaks is yours. Fork it rather than depending on this repo staying current.

It is a complete, working codebase with a test suite (Django tests + Playwright browser tests) and CI, so it is a reasonable base to build on.

> **Read [SECURITY.md](SECURITY.md) before you deploy it.** PyStarter executes
> student-submitted Python. That execution is sandboxed but the sandbox is *not* a
> hard security boundary — it is meant for local use with people you trust, and the
> default install binds to `127.0.0.1` accordingly. Do not put it on the public
> internet with open registration.

---

## Install

Two paths. **Docker** is the fastest way to just use it. **From source** is what you want if you plan to change anything.

### Option A — Docker (recommended, including Windows)

This source checkout prepares **1.0.8**. Existing **1.0.7** images and runner ZIPs
are older artifacts and do not include these fixes. Build from this checkout;
do not substitute an older runner bundle.

Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) with
Linux containers (or Docker Engine + Compose v2), then download this repository
with GitHub's **Code → Download ZIP**, extract it, and open a terminal there.
Alternatively:

```bash
git clone https://github.com/E-Conners-Lab/PyStarter.git
cd PyStarter
```

On macOS/Linux:

```bash
./init.sh
docker compose up --build -d
```

On Windows, open PowerShell in the extracted folder:

```powershell
powershell -ExecutionPolicy Bypass -File .\init.ps1
docker compose up --build -d
```

Open **http://localhost:8080**, sign up, and start Module 1. The initial build
requires internet access; normal lessons and the editor work without a CDN.
AI features are optional. Change `NGINX_PORT` in `.env` if port 8080 is occupied.
The web port is always bound to `127.0.0.1`; do not forward it through a tunnel.

`init.sh` / `init.ps1` generate unique application and database credentials and
leave an existing `.env` unchanged. Keep that file private and out of Git.
Stop with `docker compose down` (keeps your data).
**`docker compose down -v` deletes your learning database.**

**Upgrading an existing install:** back up your data first. The new database
setup separates the application user from the database administrator. An old
PostgreSQL volume needs an explicit role migration; do not replace its passwords
or delete its volume to work around a startup error. See [CONTRIBUTING.md](CONTRIBUTING.md).

### Option B — From source (macOS/Linux)

Needs Python **3.13**, [uv](https://docs.astral.sh/uv/), and Node.js **22.12+**.
Windows users should use Docker: native Windows execution is not supported.
After cloning, run `./setup.sh` to install the pinned dependencies and initialize
the local SQLite database. Then start two terminals:

```bash
# Terminal 1, from the repository root
cd backend
uv run --frozen python manage.py runserver 8002
```

```bash
# Terminal 2, from the repository root
cd frontend
npm run dev
```

Open **http://localhost:5173**. Neither server needs a public network bind.
Submitted code has the same filesystem permissions as your local account;
use Docker for a smaller filesystem exposure, and run only code you trust.


---

## Password recovery (optional)

Password-reset email requires a real email address on the account and configured
SMTP (`EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`,
`DEFAULT_FROM_EMAIL`). Signup without an email uses a placeholder and cannot
receive recovery messages. Reset links are never printed to the terminal.
Without SMTP, keep your login credentials safe; recovery mail is disabled.

## AI setup (optional)

Hints, code critique, and error explanations call an LLM. Everything else — lessons, exercises, the sandbox, XP, belts — works without one.

**Hosted provider:** set `ANTHROPIC_API_KEY` and an available `ANTHROPIC_MODEL`
in `.env` for Docker, or `backend/.env` for source installs. Provider calls may
cost money. Check the provider's current model availability and pricing before
turning this on. Your submitted code and relevant lesson context are sent to
that provider; do not submit credentials, private data, or confidential code.
Pattern-based redaction is a precaution, not a guarantee.

**Local model:** set `ANTHROPIC_BASE_URL` to your OpenAI-compatible server and
`ANTHROPIC_MODEL` to its model name. For source installs a typical URL is
`http://localhost:11434/v1`. Docker Desktop can use
`http://host.docker.internal:11434/v1`; Linux Docker Engine requires separate
host-network access configuration. Keep that model server private too.

The tutor returns text only and has no execution tools. Core lessons, grading,
XP, and the editor do not require a provider. Test your chosen model against
[the AI evaluation checklist](docs/security-verification.md) before relying on
its advice.

---

## What's inside

**Built-in code editor** — Monaco (the VS Code engine) in the browser, with syntax highlighting and auto-indent.

**Local code execution** — separate processes, bounded output, timeouts, and Linux resource limits protect against ordinary programming mistakes. Python restrictions are bypassable, and code runs under the application’s OS identity. This is not an isolation boundary for hostile code — see [SECURITY.md](SECURITY.md).

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
| Sandbox limits and the import allowlist | `backend/apps/executor/sandbox.py` (orchestration) and `runner.py` (the child process) |
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
| Testing | Django tests + Playwright browser tests |
| CI | GitHub Actions |

`/api/v1/health/` reports the running version. A source change does not update
previously published Docker images or release ZIPs.

---

## License

MIT — see [LICENSE](LICENSE). Provided as is, without warranty of any kind.

Originally built by [**The Tech-E**](https://www.thetech-e.com).
