# Contributing to PyStarter

Thanks for your interest in contributing! This guide covers the project architecture, conventions, and development workflow.

## Development Setup

### Prerequisites
- Python 3.13+ with [uv](https://docs.astral.sh/uv/) package manager
- Node.js 18+

### Backend
```bash
cd backend
cp .env.example .env          # fill in your API keys
uv run python manage.py migrate
uv run python manage.py seed_curriculum
uv run python manage.py runserver 8002
```

### Frontend (separate terminal)
```bash
cd frontend
npm install
npm run dev
```

The app runs at http://localhost:5173 (frontend) proxying API calls to http://localhost:8002 (backend).

### Development Settings
- Backend: port 8002 (`manage.py runserver 8002`)
- Frontend: port 5173 (Vite dev server, proxies `/api` to backend)
- Django settings module: `config.settings.development` (set via `DJANGO_SETTINGS_MODULE`)
- CORS: allow all origins in development
- API prefix: `/api/v1/`

## Architecture

| Layer | Stack | Directory |
|-------|-------|-----------|
| Backend API | Django 6, Django REST Framework, SimpleJWT | `backend/` |
| Frontend | React 19, TypeScript, Vite | `frontend/` |
| Database | SQLite (dev), PostgreSQL (prod) | `backend/db.sqlite3` |
| AI features | Anthropic Claude API | `backend/apps/ai/` |
| Code execution | Sandboxed `exec()` with import/builtin restrictions | `backend/apps/executor/` |

### Backend apps (`backend/apps/`)
- **accounts** — User registration, JWT auth, profile, XP/belt progression
- **curriculum** — Modules, Lessons, Exercises, TestCases, Hints (the content models)
- **submissions** — Exercise submission handling, grading, XP awards
- **executor** — Sandboxed Python code execution engine
- **ai** — Claude-powered hint generation, code critique, error explanation
- **common** — Shared utilities

### Frontend structure (`frontend/src/`)
- **pages/** — Route-level components: `Home`, `Login`, `Register`, `Dashboard`, `ModulePage`, `LessonPage`, `ExercisePage`, `Profile`
- **api/** — API client layer: `client.ts` (axios instance), `auth.ts`, `curriculum.ts`, `submissions.ts`, `types.ts`
- **components/** — Reusable UI: `layout/` (navbar, footer), `editor/` (Monaco wrapper), `ProtectedRoute`
- **stores/** — `authStore.ts` (Zustand for auth state)

### State management
- **Zustand** for auth state (JWT tokens, current user)
- **TanStack Query** for all server data fetching and caching

### Styling
- TailwindCSS with a dark theme
- Custom color palette via `tailwind.config.js`

### Markdown rendering
- **react-markdown** with **remark-gfm** for GitHub Flavored Markdown (tables, strikethrough, etc.)
- Lesson content and exercise instructions are stored as markdown strings and rendered client-side

## Data Model

```
Module (ordered 1-14)
  └── Lesson (ordered 1-4 within module)
        ├── 1: concept — teaches the topic
        ├── 2: interactive — sandbox experimentation
        ├── 3: exercise — graded exercises with test cases
        ├── 4: interactive — "Try It Yourself" open-ended challenges
        └── Exercise (ordered within lesson, only on exercise-type lessons)
              ├── type: fill_blank | fix_bug | write_code | output_predict
              ├── TestCase (expected input/output pairs)
              └── Hint (levels 1-2, increasing XP penalties)
```

Progression is strictly linear: complete all exercises in a module to unlock the next.

## Code Sandbox

User code runs in `backend/apps/executor/sandbox.py` with:
- **Allowed imports**: math, random, string, collections, datetime, json, re, typing, copy, itertools, functools, textwrap, ipaddress
- **Blocked builtins**: exec, eval, compile, open, input (replaced), \_\_import\_\_ (restricted), getattr, setattr, etc.
- **5-second timeout** per execution
- Output compared against TestCase expected output (flexible: strips whitespace, case-insensitive, numeric tolerance)

## Key Commands

```bash
# Re-seed curriculum (flush first if data exists)
cd backend
uv run python manage.py flush --no-input
uv run python manage.py seed_curriculum

# Run backend tests
cd backend
uv run python manage.py test

# Run Playwright e2e tests (99 tests)
cd frontend
npx playwright test

# Build frontend for production
cd frontend
npm run build
```

## Conventions

- Django apps live in `backend/apps/`
- All API endpoints are prefixed with `/api/v1/`
- Frontend pages in `frontend/src/pages/`, API layer in `frontend/src/api/`
- Exercise types: `fill_blank`, `fix_bug`, `write_code`, `output_predict`
- Lesson types: `concept`, `interactive`, `exercise`
- Icons are mapped by string key in `Dashboard.tsx` (`MODULE_ICONS` dict)
- Progressive hints: 2 levels with 0%/10% XP penalties

## CI/CD

All PRs run the CI pipeline (`.github/workflows/ci.yml`):

1. **backend-tests** — migrations, seed, `uv run python manage.py test`
2. **frontend-build** — `npm ci`, `npm run build` (includes type-check)
3. **e2e-tests** — full Playwright suite against both servers

All three jobs must pass before merging.

## Releasing

Published images live in GHCR; the runner bundle's `docker-compose.yml` pins exact tags, so
every release is a tag bump plus a push. Nothing here is automated by CI today.

**1. Bump the version.** It lives in two places that are asserted against each other:
`APP_VERSION` in `backend/config/settings/base.py` and `ARG APP_VERSION` in `backend/Dockerfile`.
`apps/common/tests/test_health.py::VersionDriftTest` fails if they drift apart. The backend
reports this value at `/api/v1/health/`, which is how you confirm what is actually deployed.

**2. Build and push both images, multi-arch.** The build arg is what stamps the version into
the image — omit it and health reports the previous release.

```bash
VERSION=1.0.6
docker buildx build --platform linux/amd64,linux/arm64 \
  -f backend/Dockerfile --build-arg APP_VERSION=$VERSION \
  -t ghcr.io/e-conners-lab/pystarter-backend:$VERSION --push .
docker buildx build --platform linux/amd64,linux/arm64 \
  -f frontend/Dockerfile \
  -t ghcr.io/e-conners-lab/pystarter-frontend:$VERSION --push frontend
```

**3. Move `latest` onto the new release.** This does not happen on its own — `latest` sat on
1.0.3 through the 1.0.4 and 1.0.5 releases, so anyone pulling it got a build whose default
model had already been retired.

```bash
for img in backend frontend; do
  docker buildx imagetools create \
    -t "ghcr.io/e-conners-lab/pystarter-${img}:latest" \
    "ghcr.io/e-conners-lab/pystarter-${img}:$VERSION"
done
```

`imagetools create` copies the manifest list server-side: both architectures stay attached and
no layers are re-uploaded. Keep the braces on `${img}` — in zsh, `$img:latest` is parsed as the
`:l` lowercase modifier and silently pushes to a `…-backendatest` repository instead.

**4. Verify from the outside**, as a new user would — pull anonymously, not from local cache:

```bash
docker buildx imagetools inspect ghcr.io/e-conners-lab/pystarter-backend:latest   # both arches, digest == $VERSION
curl -s localhost/api/v1/health/                                                  # {"version":"1.0.6",...}
```

**5. Ship the runner bundle.** Bump the image tags in the bundle's `docker-compose.yml`, refresh
the version references in the public `README.md`, re-zip as `pystarter-v$VERSION-runner.zip`, and
attach it to the GitHub release.

## Docker / Production

- **Docker Compose** runs 4 services: `db` (PostgreSQL 16), `backend` (Gunicorn), `frontend` (nginx-served React), `nginx` (reverse proxy)
- `backend/entrypoint.sh` auto-waits for DB, runs migrations, collects static files on container start
- Backend has a healthcheck via `/api/v1/health/`; nginx waits for healthy backend
- Production settings in `backend/config/settings/production.py` (SSL redirect, HSTS, proxy SSL header, rate limiting)
- Rate limiting via `django-ratelimit` on auth and AI endpoints
- Backup script: `scripts/backup-db.sh` (gzipped pg_dump with optional `PRUNE_DAYS` pruning)
