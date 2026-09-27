# Contributing to PyStarter

PyStarter is a local learning app, MIT licensed and not actively maintained.
Read [SECURITY.md](SECURITY.md) before modifying execution or deployment behavior.

## Development

Use Python 3.13, uv, Node 22.12+, and `./setup.sh` on macOS/Linux. The script
uses `uv sync --locked` and `npm ci`. Run Django on localhost:8002 and Vite on
localhost:5173 as described in [README.md](README.md). Use Docker Desktop on
Windows; native Windows execution is intentionally unsupported.

The backend defaults to SQLite and non-debug responses. Set `DJANGO_DEBUG=true`
only for local debugging. CORS permits the explicit local frontend origins.
Never bind the development servers to an external network interface.

## Architecture

| Component | Responsibility |
|---|---|
| accounts | HttpOnly cookie JWT sessions, CSRF, rate limits, profiles and XP |
| curriculum | Published modules, lessons, exercises, visible tests and hints |
| submissions | Server-side grading, ownership, progress and hint costs |
| executor | Bounded subprocess lifecycle for trusted local Python |
| ai | Optional text-only tutoring with bounded/redacted input |
| common | JSON errors, request IDs, API security headers, authentication |
| React frontend | Monaco editor, lesson UI, user state and API calls |

Tokens stay in HttpOnly cookies; Zustand stores user/loading state. The API
prefix is `/api/v1/`, echoed by `X-API-Version`. POSTs require JSON and CSRF.
Frontend requests with no payload still send `{}`. Non-public data is scoped
server-side to the authenticated user. Logout and password resets revoke sessions.

The Python subprocess shares the backend identity and is **not a hostile-code
sandbox**. Native Windows fails closed. Linux enforces resource limits; macOS
memory limits are advisory. Do not weaken this description when adding features.

## Verification

```bash
uv sync --locked
cd backend
uv run --frozen python manage.py makemigrations --check --dry-run
uv run --frozen coverage run --rcfile=../pyproject.toml manage.py test
uv run --frozen coverage report --rcfile=../pyproject.toml
uv run --frozen pip-audit
uv run --frozen bandit -r apps config -lll
```

```bash
cd frontend
npm ci
npm audit
npm run build
npx --no-install playwright install chromium
npm run test:e2e
```

Browser tests start their own servers on 5187/8017. Prepare a disposable local
SQLite database with `migrate` and `seed_curriculum` first. Dedicated e2e settings
raise only the test authentication request limit; production limits remain on.
Do not point tests at your own learning database.

CI also scans full Git history with Gitleaks, checks Python/TypeScript with
CodeQL, builds/scans runtime images, and uploads security reports. GitHub must
require those checks before merging; workflow files alone do not protect main.

## Optional AI changes

The tutor has no tools. Keep instructions separate from untrusted serialized
input and never include reference solutions or credentials. Test the adversarial
and regression cases described in [the verification record](docs/security-verification.md).
Provider requests can cost money and disclose submitted code. Redaction is
best-effort. Check the provider's current supported model IDs rather than
assuming an alias will remain available indefinitely.

## Existing Docker database upgrade

Back up before any upgrade. Never run `down -v` to resolve an authentication
problem: that deletes the database. Keep your original `DB_PASSWORD` and
`DJANGO_SECRET_KEY`. Changing a PostgreSQL environment variable does not change
an existing database role's password.

Fresh installs now use a limited application role (`pystarter`) and a separate
cluster administrator (`pystarter_admin`). For an old volume whose `pystarter`
role is the cluster superuser, create the administrator before starting the new
Compose configuration. Connect interactively using the **old** working stack:

```bash
docker compose exec db psql -U pystarter -d pystarter
```

```sql
CREATE ROLE pystarter_admin LOGIN SUPERUSER;
\password pystarter_admin
ALTER ROLE pystarter NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION;
```

Enter a new random password at the prompt, then store that same value as
`POSTGRES_ADMIN_PASSWORD` in your private `.env`. Preserve `DB_PASSWORD` for
`pystarter`. The application role remains owner of its database for migrations.
Only after a verified backup and successful role setup, start the updated stack.
If your role names differ, adapt this migration to your installation; do not
blindly recreate or delete existing roles/volumes.

## Release checklist

1. Bump `APP_VERSION` in settings and the backend Dockerfile together; the health
   test checks them. This branch prepares 1.0.8; 1.0.7 artifacts are unchanged.
2. Pass tests, coverage >=80%, audits, secret/SAST scans, and image gates.
3. Review source on a protected branch. Require independent approval and signed
   commits, no force pushes or administrator bypass; keep push protection on.
4. For a binary/image release, build each advertised architecture on hosted CI,
   attach an SBOM and build provenance, and sign the image digests with Sigstore.
   Verify the downloaded artifact anonymously before advertising it. Never move
   an old version tag onto different contents.
5. Update download links only after verified artifacts exist. A successful local
   source build does not certify earlier published images or ZIP files.

No prebuilt-image publishing workflow is supplied by this source-only change.
The currently published 1.0.7 runner must not be presented as containing 1.0.8 fixes.
