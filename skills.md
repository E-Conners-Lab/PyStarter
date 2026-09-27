# Building an Interactive Learning Platform — Framework & Skills Guide

A reusable framework for building web-based training platforms with sandboxed code execution and AI-powered assistance. Based on the architecture behind PyStarter.

---

## Part 1: General Framework

### The Core Loop

Every effective learning platform follows the same loop:

```
Present concept → Let user practice → Grade their work → Give feedback → Unlock next topic
```

Your entire architecture should serve this loop. Every technical decision flows from it.

### Phase 1: Data Model First

Design your content hierarchy before writing any code. The data model IS your spec.

```
Course / Track
  └── Module (ordered, lockable)
        └── Lesson (ordered, typed)
              └── Exercise (ordered, typed, graded)
                    ├── Test Cases (input/output pairs)
                    └── Hints (progressive, with cost)
```

Key decisions at this stage:
- **Progression model**: Linear (unlock next when current is done) vs. open (access anything). Linear is better for beginners — it prevents overwhelm.
- **Exercise types**: Decide what kinds of practice you'll support. Each type needs different UI and grading logic.
- **Hint economics**: Free hints don't motivate effort. Progressive hints with increasing XP penalties encourage self-reliance.

### Phase 2: Execution Engine

If your platform runs user code, the sandbox is your most critical component.

**Minimum viable sandbox:**
1. Restricted namespace — remove dangerous builtins (exec, eval, open, \_\_import\_\_)
2. Import whitelist — only allow safe standard library modules
3. Timeout — kill execution after N seconds
4. Memory limit — prevent allocation bombs
5. Custom input() — replace stdin with a queue for exercises that need user input

**Output comparison** must be forgiving for beginners:
- Strip whitespace
- Case-insensitive matching
- Numeric tolerance (1.0 == 1 == 1.000000)
- Line-by-line comparison ignoring trailing spaces

**Error messages** should be translated into plain English. Map Python exception types to friendly explanations.

### Phase 3: API Layer

Build a REST API that serves the core loop:

| Concern | Endpoints |
|---------|-----------|
| Auth | Register, login, token refresh, logout, password reset |
| Content | List modules, get lesson, get exercise + test cases |
| Execution | Run code (no grade), submit code (graded) |
| Progress | Track completion, award XP, unlock next module |
| AI (optional) | Generate hints, critique solutions, explain errors |

**Key patterns:**
- Separate "Run" (practice, no XP) from "Submit" (graded, awards XP)
- Progress tracking needs three levels: module progress, lesson progress, exercise progress
- Module completion should cascade: all exercises done → lesson done → all lessons done → module done → unlock next module

### Phase 4: Frontend

The frontend is a thin presentation layer over your API.

**Page structure mirrors the content hierarchy:**
```
Dashboard → Module list with progress bars
Module Page → Lesson list with completion checkmarks
Lesson Page → Content (markdown) + exercise list
Exercise Page → Code editor + test results + hints
```

**State management:**
- Auth state (tokens, current user) → lightweight store (Zustand, Pinia, etc.)
- Server data (modules, lessons, progress) → query cache (TanStack Query, SWR, etc.)
- Don't put server data in your state store. Let the query cache handle it.

**Code editor:** Use Monaco (VS Code engine) or CodeMirror. Don't build your own.

### Phase 5: Content Authoring

Your curriculum is your product. The platform is just the delivery mechanism.

**Content format:** Store lesson content as Markdown. Render it client-side. This keeps content portable and easy to author.

**Seed command:** Build a management command that populates your database from structured data (hardcoded or from files). This lets you version-control your curriculum and recreate it from scratch.

**Content structure per module:**
1. Concept lesson — teach the topic with examples
2. Interactive sandbox — let them experiment freely
3. Graded exercises — test their understanding
4. Open-ended challenges — apply concepts to real scenarios (no grading, just practice)

### Phase 6: AI Integration

AI features are optional but powerful for learning platforms.

**Three AI features that matter:**
1. **Contextual hints** — Given the exercise, the student's code, and their error, guide their thinking without giving the answer
2. **Code critique** — After they pass, suggest one improvement (Pythonic style, edge cases, etc.)
3. **Error explanation** — Translate cryptic error messages into beginner-friendly language

**Prompting strategy for education:**
- System prompt: "You are a patient tutor. Keep responses to 2-4 sentences."
- Include: exercise instructions, student's code, error message, concepts being tested
- Never give the complete solution unless they've exhausted all hints
- Use analogies and everyday language

**Provider pattern:** Abstract your AI provider so you can swap between cloud APIs and local LLMs. Support OpenAI-compatible endpoints for local models (Ollama, LM Studio).

### Phase 7: Production & Deployment

**Docker Compose** for multi-container deployment:
- Database (PostgreSQL)
- Backend (application server behind gunicorn/uvicorn)
- Frontend (static build served by nginx)
- Reverse proxy (nginx routing /api to backend, / to frontend)

**Entrypoint script:** Auto-run migrations on container start. Wait for database to be ready before starting the application server.

**Health checks:** Every service should have one. The reverse proxy should wait for the backend to be healthy before routing traffic.

**CI/CD pipeline:**
1. Backend tests (unit + integration)
2. Frontend build (type-check + bundle)
3. End-to-end tests (Playwright against running app)

---

## Part 2: PyStarter-Specific Implementation

### Tech Stack

| Layer | Choice | Why |
|-------|--------|-----|
| Backend | Django 6 + DRF + SimpleJWT | Mature ORM, built-in admin, security defaults, excellent for relational data |
| Frontend | React 19 + TypeScript + Vite | Fast builds, strong typing, large ecosystem |
| State | Zustand (auth) + TanStack Query (data) | Minimal boilerplate, automatic cache management |
| Editor | Monaco Editor | Same engine as VS Code, professional feel |
| Markdown | react-markdown + remark-gfm | GitHub-flavored markdown with tables and code blocks |
| Styling | TailwindCSS (dark theme) | Rapid UI development, consistent design |
| Database | SQLite (dev) / PostgreSQL (prod) | Zero-setup dev, production-grade prod |
| AI | Anthropic Claude API (or any OpenAI-compatible LLM) | Best-in-class for educational content |

### Build Order (What to Build First)

This is the order that minimizes rework:

**1. Backend data models** (accounts app + curriculum app)
- User model with XP and belt progression
- Module → Lesson → Exercise → TestCase → Hint hierarchy
- Progress tracking models (UserModuleProgress, UserLessonProgress, UserExerciseProgress)

**2. Seed command**
- Populate all 14 modules, 56 lessons, 66 exercises with real content
- This forces you to finalize your data model before building UI

**3. Sandbox engine** (executor app)
- Restricted exec() with safe builtins
- Import whitelist, timeout, memory limits
- Output comparison with beginner-friendly tolerance
- Friendly error message formatting

**4. API views and serializers**
- Curriculum endpoints (list/detail for modules, lessons, exercises)
- Submission endpoints (run, submit, history)
- Auth endpoints (register, login, token refresh)
- Progress tracking and module unlock logic

**5. Frontend pages**
- Auth pages (login, register)
- Dashboard (module list with progress)
- Module page (lesson list)
- Lesson page (markdown content)
- Exercise page (editor + test results + submission flow)

**6. AI integration** (ai app)
- Provider abstraction (Anthropic + OpenAI-compatible)
- Hint, critique, and error explanation endpoints
- System prompts tuned for beginners

**7. Polish and progression**
- XP awards, belt progression, streaks
- Progressive hint reveal with XP penalties
- "Try It Yourself" open-ended challenge lessons

**8. Production hardening**
- Docker multi-stage build
- docker-compose with PostgreSQL, nginx, healthchecks
- Production Django settings (SSL, HSTS, CORS, rate limiting)
- CI/CD pipeline (GitHub Actions)
- Database backup script

### Data Model Details

#### User & Progression

```python
# User extends AbstractUser
User:
    email (unique)
    bio, total_xp, current_streak, longest_streak, last_activity_date
    # Belt thresholds: White(0), Yellow(200), Orange(600), Green(1500),
    #   Blue(3000), Purple(6000), Brown(10000), Black(18000)
    # Properties: current_belt, current_belt_display, next_belt_xp
    # Methods: award_xp(amount), update_streak()

UserModuleProgress:   (user, module) unique_together
    is_unlocked, is_completed, started_at, completed_at

UserLessonProgress:   (user, lesson) unique_together
    is_completed, started_at, completed_at

UserExerciseProgress: (user, exercise) unique_together
    is_completed, best_code, xp_earned, attempts, hints_used, completed_at
```

#### Curriculum

```python
Module:
    title, slug, description, order (unique), icon, is_published

Lesson:
    module (FK), title, slug, order, lesson_type (concept|interactive|exercise)
    content (markdown), sandbox_code (starter code for interactive), is_published

Exercise:
    lesson (FK), title, slug, order
    exercise_type (fill_blank|fix_bug|write_code|output_predict)
    difficulty (1-4), instructions (markdown), starter_code, solution_code
    choices (JSON, for output_predict), xp_value, concepts, is_published

TestCase:
    exercise (FK), input_data, expected_output, is_hidden, description, order

Hint:
    exercise (FK), level (1-5), content (markdown), xp_penalty_percent, order
```

#### Submissions

```python
Submission:
    user, exercise (FK), code, status (pending|running|passed|failed|error|timeout)
    passed_tests, total_tests, execution_time, error_message
    xp_awarded, is_run_only (run vs submit), created_at

TestCaseResult:
    submission, test_case (FK), passed, actual_output, expected_output, error_message
```

### API Endpoints

```
# Auth
POST   /api/v1/accounts/register/              → create user + tokens
POST   /api/v1/accounts/token/                  → login (get tokens)
POST   /api/v1/accounts/token/refresh/          → refresh access token
POST   /api/v1/accounts/token/blacklist/        → logout
GET    /api/v1/accounts/me/                     → current user profile
GET    /api/v1/accounts/progress-summary/       → dashboard stats
GET    /api/v1/accounts/leaderboard/            → top 20 by XP
POST   /api/v1/accounts/password-reset/         → request reset email
POST   /api/v1/accounts/password-reset-confirm/ → confirm with uid+token

# Curriculum
GET    /api/v1/curriculum/modules/                              → all modules + progress
GET    /api/v1/curriculum/modules/<slug>/                        → module detail + lessons
GET    /api/v1/curriculum/modules/<slug>/lessons/<slug>/         → lesson + exercises
GET    /api/v1/curriculum/modules/<m>/lessons/<l>/exercises/<e>/ → exercise + test cases
POST   /api/v1/curriculum/exercises/<id>/hint/                   → reveal next hint
GET    /api/v1/curriculum/exercises/<id>/hints/                   → revealed hints
POST   /api/v1/curriculum/lessons/<id>/complete/                  → mark lesson done

# Submissions
POST   /api/v1/submissions/sandbox/      → free code execution (no exercise)
POST   /api/v1/submissions/run/<id>/     → run visible tests only (no XP)
POST   /api/v1/submissions/submit/<id>/  → grade all tests (awards XP)
GET    /api/v1/submissions/history/<id>/ → last 10 submissions

# AI
POST   /api/v1/ai/hint/<id>/          → contextual hint
POST   /api/v1/ai/critique/<id>/      → feedback on passing code
POST   /api/v1/ai/explain-error/<id>/ → explain error in plain English

# Health
GET    /api/v1/health/                 → 200 OK
```

### Sandbox Implementation

```python
ALLOWED_IMPORTS = {
    "math", "random", "string", "collections", "datetime",
    "json", "re", "typing", "copy", "itertools", "functools",
    "textwrap", "ipaddress"
}

FORBIDDEN_BUILTINS = {
    "exec", "eval", "compile", "open", "input", "__import__",
    "globals", "getattr", "setattr", "delattr", "breakpoint", "exit", "quit"
}

# Execution: ThreadPoolExecutor with 5-second timeout
# Memory: 128MB via resource.setrlimit (save/restore after each run)
# Recursion: sys.setrecursionlimit(200) (save/restore after each run)
# Input: Custom input() reads from pre-loaded queue
# Output comparison: strip, case-insensitive, numeric tolerance, line-by-line
```

### Submission Flow

```
User clicks "Run":
  → POST /submissions/run/{id}/
  → Run visible test cases only
  → Return results (no XP, no progression)

User clicks "Submit":
  → POST /submissions/submit/{id}/
  → Run ALL test cases (visible + hidden)
  → If all pass:
      → Calculate XP (exercise.xp_value * (100 - hint_penalties) / 100)
      → Award XP to user
      → Mark exercise complete
      → Check if all exercises in lesson are done → mark lesson complete
      → Check if all lessons in module are done → mark module complete
      → If module complete → unlock next module
  → Return results + XP awarded
```

### XP Economy

| Element | Value |
|---------|-------|
| XP per exercise | 10-30 (based on difficulty) |
| Hint penalty (level 1) | 0% (free nudge) |
| Hint penalty (level 2) | 10% |
| Total possible XP | ~1320 across 66 exercises |
| Belt ranks | White(0) → Yellow(200) → Orange(600) → Green(1500) → Blue(3000) → Purple(6000) → Brown(10000) → Black(18000) |

### Frontend Page Structure

```
/ → Home (public landing page)
/login → Login
/register → Register
/dashboard → Module list with progress bars and belt display
/module/:slug → Lesson list with completion checkmarks
/module/:slug/lesson/:slug → Markdown content + exercise list OR sandbox
/module/:slug/lesson/:slug/exercise/:slug → Monaco editor + test results
/profile → User stats, streak, belt progression
```

### Key Design Decisions

| Decision | Why |
|----------|-----|
| Linear progression | Beginners get overwhelmed by choice. Complete module N to unlock N+1. |
| Separate Run vs Submit | Let users iterate freely (Run) before committing (Submit). Only Submit awards XP. |
| Progressive hints with XP cost | Free hints don't motivate effort. Escalating penalties encourage trying first. |
| Friendly error messages | "NameError" means nothing to a beginner. Translate to plain English. |
| Flexible output matching | Beginners add extra spaces, different casing. Be forgiving. |
| Markdown for content | Easy to author, version-control, and render. No CMS needed. |
| SQLite for dev | Zero setup. New contributor runs `migrate` and they're coding. |
| AI hints guide, not solve | "Walk you through your thinking" — not "here's the answer." |
| Dark theme | Developers expect it. Reduces eye strain during long coding sessions. |
| Monaco editor | Professional feel. Syntax highlighting makes code readable for beginners. |

### Testing Strategy

| Layer | Tool | Count | What's Tested |
|-------|------|-------|---------------|
| E2E | Playwright | 99 tests | Full user flows: register, navigate, write code, submit, earn XP, unlock modules |
| Backend | Django TestCase | 17 tests | Models, views, sandbox (memory limits, timeouts, imports), API endpoints |
| Frontend | Vite build | — | TypeScript type-checking catches errors at build time |
| CI | GitHub Actions | 3 jobs | Backend tests → Frontend build → E2E tests (must all pass) |

### Production Checklist

- [ ] Set `DJANGO_SECRET_KEY` to a unique random value
- [ ] Set `ALLOWED_HOSTS` to your domain(s)
- [ ] Set `CORS_ALLOWED_ORIGINS` to your frontend URL(s)
- [ ] Set `DB_PASSWORD` to a secure password
- [ ] Configure SSL/TLS termination (nginx or load balancer)
- [ ] Set up `ANTHROPIC_API_KEY` if using AI features
- [ ] Run `seed_curriculum` after first deploy
- [ ] Set up cron for database backups (`scripts/backup-db.sh`)
- [ ] Set up cron for `manage.py flushexpiredtokens` (weekly)
- [ ] Configure Sentry DSN for error tracking (optional)
- [ ] Configure SMTP for password reset emails (optional)
