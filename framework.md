# Framework: Building an Interactive Learning Platform

A reusable blueprint for building web-based training platforms with sandboxed code execution, graded exercises, and AI-powered assistance. Copy this file into a new project and fill in the placeholders.

---

## How to Use This Document

1. Read through the framework to understand the architecture
2. Fill in the **[PLACEHOLDER]** sections with your project-specific details
3. Hand this to an LLM or developer as the spec for your project
4. Build in phase order — each phase depends on the ones before it

---

## Project Definition

Fill these in before building:

```
Project Name:       [YOUR PROJECT NAME]
Subject:            [What are you teaching? e.g., Python, SQL, JavaScript, Networking]
Target Audience:    [Who is this for? e.g., absolute beginners, career changers, engineers]
Module Count:       [How many modules? e.g., 10-15 is a good range]
Exercises Per Module: [How many graded exercises? e.g., 4-6]
Exercise Types:     [What kinds of practice? e.g., fill_blank, fix_bug, write_code, multiple_choice]
```

---

## The Core Loop

Every effective learning platform follows the same loop:

```
Present concept → Let user practice → Grade their work → Give feedback → Unlock next topic
```

Your entire architecture serves this loop. Every technical decision flows from it.

---

## Recommended Tech Stack

| Layer | Recommended | Alternatives | Why |
|-------|-------------|--------------|-----|
| Backend | Django + DRF + SimpleJWT | FastAPI, Express, Rails | Mature ORM for relational data, built-in admin, auth, security defaults |
| Frontend | React + TypeScript + Vite | Vue + Nuxt, Svelte, Next.js | Fast builds, strong typing, large ecosystem |
| Auth State | Zustand | Pinia (Vue), Redux, Context API | Minimal boilerplate for JWT token management |
| Server State | TanStack Query | SWR, Apollo (GraphQL) | Automatic caching, refetching, no manual state sync |
| Code Editor | Monaco Editor | CodeMirror | Same engine as VS Code, professional feel |
| Content Rendering | react-markdown + remark-gfm | MDX, custom renderer | Portable content, easy to author and version-control |
| Styling | TailwindCSS | CSS Modules, Styled Components | Rapid development, consistent design system |
| Database | SQLite (dev) / PostgreSQL (prod) | MySQL, MongoDB (not recommended for relational data) | Zero-setup dev, production-grade prod |
| AI | Claude API or OpenAI API | Local LLMs via Ollama/LM Studio | Best-in-class for educational content |
| E2E Testing | Playwright | Cypress | Multi-browser, reliable, built-in auto-wait |
| CI/CD | GitHub Actions | GitLab CI, CircleCI | Free for public repos, good ecosystem |
| Deployment | Docker Compose | Kubernetes (overkill for most), bare metal | Simple multi-container orchestration |

---

## Phase 1: Data Model

Design your content hierarchy before writing any code. The data model IS your spec.

### Content Hierarchy

```
Module (ordered, lockable)
  └── Lesson (ordered, typed)
        ├── type: concept — teaches the topic
        ├── type: interactive — sandbox for free experimentation
        ├── type: exercise — graded exercises with test cases
        └── type: challenge — open-ended "try it yourself" scenarios
              └── Exercise (ordered within lesson)
                    ├── type: [FILL IN YOUR EXERCISE TYPES]
                    ├── TestCase (input/output pairs for grading)
                    └── Hint (progressive levels with XP penalties)
```

### User & Progression Models

```
User (extends base user model)
├── email, bio
├── total_xp (drives rank/belt progression)
├── current_streak, longest_streak, last_activity_date
├── Rank thresholds: define 6-10 ranks with XP milestones
│   e.g., Beginner(0), Novice(200), Apprentice(600), Intermediate(1500),
│         Advanced(3000), Expert(6000), Master(10000), Grand Master(18000)
└── Methods: award_xp(amount), update_streak()

UserModuleProgress:   (user, module) unique_together
    is_unlocked, is_completed, started_at, completed_at

UserLessonProgress:   (user, lesson) unique_together
    is_completed, started_at, completed_at

UserExerciseProgress: (user, exercise) unique_together
    is_completed, best_code, xp_earned, attempts, hints_used, completed_at
```

### Curriculum Models

```
Module:
    title, slug, description, order (unique), icon, is_published

Lesson:
    module (FK), title, slug, order
    lesson_type: concept | interactive | exercise | challenge
    content (markdown — the lesson body)
    sandbox_code (starter code for interactive/challenge lessons)
    is_published

Exercise:
    lesson (FK), title, slug, order
    exercise_type: [YOUR TYPES, e.g., fill_blank | fix_bug | write_code | predict_output]
    difficulty (1-4)
    instructions (markdown — the problem statement)
    starter_code (pre-loaded in editor, with TODO markers)
    solution_code (reference solution, revealed after all hints)
    choices (JSON — for multiple choice types)
    xp_value (points awarded)
    concepts (comma-separated tags)
    is_published

TestCase:
    exercise (FK), input_data, expected_output
    is_hidden (hidden tests only shown after submission)
    description (human-friendly label)
    order

Hint:
    exercise (FK), level (1-5), content (markdown)
    xp_penalty_percent (0, 10, 25, 50, 100)
    order
```

### Submission Models

```
Submission:
    user, exercise (FK), code
    status: pending | running | passed | failed | error | timeout
    passed_tests, total_tests, execution_time, error_message
    xp_awarded, is_run_only (run vs submit)
    created_at

TestCaseResult:
    submission, test_case (FK)
    passed, actual_output, expected_output, error_message
    execution_time
```

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Linear progression | Beginners get overwhelmed by choice. Complete module N to unlock N+1. |
| Separate Run vs Submit | Run = practice freely, no stakes. Submit = graded, awards XP. Reduces anxiety. |
| Progressive hints with XP cost | Level 1 is free. Each deeper level costs more XP. Encourages trying first. |
| Hidden test cases | Visible tests let users iterate. Hidden tests prevent hard-coding answers. |
| unique_together on progress | One progress record per user per entity. Prevents duplicate tracking. |
| Slugs on content models | Clean URLs (/module/loops/lesson/for-loops/) instead of IDs. |

---

## Phase 2: Execution Engine

If your platform runs user code, the sandbox is your most critical component.

### Sandbox Architecture

```python
# What to restrict (for Python — adapt for your language)
ALLOWED_IMPORTS = {
    # Only safe standard library modules relevant to your curriculum
    # e.g., math, random, string, collections, json, re, datetime
    [FILL IN BASED ON YOUR CURRICULUM]
}

FORBIDDEN_BUILTINS = {
    "exec", "eval", "compile", "open", "__import__",
    "globals", "getattr", "setattr", "delattr",
    "breakpoint", "exit", "quit"
}
```

### Execution Strategy

```
1. Build restricted namespace (safe builtins + whitelisted imports)
2. Replace input() with a version that reads from pre-loaded queue
3. Set resource limits (memory: 128MB, recursion: 200)
4. Run code in a thread pool with timeout (5 seconds)
5. Capture stdout/stderr
6. Restore resource limits after execution
7. Compare output against test cases
```

### Output Comparison (Beginner-Friendly)

Your output comparison should be forgiving:
1. Strip leading/trailing whitespace
2. Case-insensitive comparison
3. Line-by-line comparison ignoring trailing spaces per line
4. Numeric tolerance (±1e-6 for floating point)

### Error Message Translation

Map language-specific errors to beginner-friendly messages:
```
NameError    → "Did you misspell a variable, or use it before creating it?"
TypeError    → "You might be mixing up data types (like adding a number to a string)."
SyntaxError  → "Python couldn't understand your code. Check for missing colons or brackets."
IndexError   → "You're trying to access an item that doesn't exist in the list."
KeyError     → "That key doesn't exist in the dictionary."
ZeroDivision → "You can't divide by zero!"
Indentation  → "Check that your lines are indented correctly."
Timeout      → "Your code took too long. Check for infinite loops!"
```

---

## Phase 3: API Layer

### Endpoint Structure

```
# Auth
POST   /api/v1/accounts/register/              → create user + return tokens
POST   /api/v1/accounts/token/                  → login (username + password → tokens)
POST   /api/v1/accounts/token/refresh/          → refresh access token
POST   /api/v1/accounts/token/blacklist/        → logout (blacklist refresh token)
GET    /api/v1/accounts/me/                     → current user profile + stats
GET    /api/v1/accounts/progress-summary/       → dashboard stats (XP, rank, counts)
GET    /api/v1/accounts/leaderboard/            → top users by XP
POST   /api/v1/accounts/password-reset/         → request reset email
POST   /api/v1/accounts/password-reset-confirm/ → confirm with uid + token

# Curriculum
GET    /api/v1/curriculum/modules/                                  → all modules + user progress
GET    /api/v1/curriculum/modules/<slug>/                            → module detail + lessons
GET    /api/v1/curriculum/modules/<slug>/lessons/<slug>/             → lesson + exercises
GET    /api/v1/curriculum/modules/<m>/lessons/<l>/exercises/<e>/     → exercise + test cases
POST   /api/v1/curriculum/exercises/<id>/hint/                       → reveal next hint level
GET    /api/v1/curriculum/exercises/<id>/hints/                       → get revealed hints
POST   /api/v1/curriculum/lessons/<id>/complete/                      → mark non-exercise lesson done

# Submissions
POST   /api/v1/submissions/sandbox/       → free code execution (no exercise context)
POST   /api/v1/submissions/run/<id>/      → run visible test cases only (no XP)
POST   /api/v1/submissions/submit/<id>/   → grade ALL tests (awards XP + progression)
GET    /api/v1/submissions/history/<id>/  → recent submissions for an exercise

# AI (optional)
POST   /api/v1/ai/hint/<id>/             → contextual hint based on code + error
POST   /api/v1/ai/critique/<id>/         → feedback on passing solution
POST   /api/v1/ai/explain-error/<id>/    → explain error in plain English

# Health
GET    /api/v1/health/                    → 200 OK
```

### Auth Flow

```
Register → server creates user, unlocks Module 1, returns access + refresh tokens
Login    → server validates credentials, returns access + refresh tokens
Request  → frontend sends Authorization: Bearer {access} on every request
401      → frontend auto-refreshes using refresh token
Refresh fails → clear tokens, redirect to /login
Logout   → POST refresh token to blacklist endpoint
```

### Submission Flow

```
User clicks "Run":
  → POST /submissions/run/{id}/ with { code }
  → Server runs code against VISIBLE test cases only
  → Returns results per test case (no XP, no progression)

User clicks "Submit":
  → POST /submissions/submit/{id}/ with { code }
  → Server runs code against ALL test cases (visible + hidden)
  → If ALL pass:
      → Calculate XP: exercise.xp_value * (100 - sum_of_hint_penalties) / 100
      → Award XP to user
      → Mark exercise complete
      → Check: all exercises in lesson done? → mark lesson complete
      → Check: all lessons in module done? → mark module complete → unlock next module
  → Return results + XP awarded
```

### Rate Limiting

| Endpoint | Limit | Why |
|----------|-------|-----|
| Code execution (sandbox/run/submit) | 60/minute per user | Prevent resource abuse |
| Password reset | 5/hour per IP | Prevent email enumeration |
| Auth endpoints | 30/minute per IP | Prevent brute force |
| General API | 120/minute per user | Fair usage |

---

## Phase 4: Frontend

### Page Structure

```
/                                           → Public landing page
/login                                      → Login form
/register                                   → Registration form
/forgot-password                            → Password reset request
/reset-password/:uid/:token                 → Password reset confirm
/dashboard                                  → Module list + progress + rank
/module/:moduleSlug                         → Lesson list + completion status
/module/:moduleSlug/lesson/:lessonSlug      → Markdown content + sandbox OR exercise list
/module/:moduleSlug/lesson/:lessonSlug/exercise/:exerciseSlug → Code editor + grading
/profile                                    → User stats, streak, rank progression
```

### State Management Pattern

```
Auth Store (Zustand/Pinia):
  - access token, refresh token
  - current user object
  - login(), logout(), refreshToken() actions

Server Data (TanStack Query/SWR):
  - useQuery(['modules']) → module list + progress
  - useQuery(['exercise', slug]) → exercise detail
  - useMutation(submitCode) → on success, invalidate related queries
  - NO server data in the auth store — let the query cache own it
```

### Component Structure

```
src/
├── pages/          → Route-level components (one per page above)
├── components/
│   ├── layout/     → Header, Footer, Sidebar
│   ├── editor/     → Code editor wrapper (Monaco/CodeMirror)
│   └── ProtectedRoute → Redirects to /login if not authenticated
├── api/
│   ├── client.ts   → HTTP client with auth interceptor + token refresh
│   ├── auth.ts     → register(), login(), logout(), resetPassword()
│   ├── curriculum.ts → getModules(), getLesson(), getExercise()
│   ├── submissions.ts → runCode(), submitCode(), getHistory()
│   └── types.ts    → TypeScript interfaces matching API responses
└── stores/
    └── authStore.ts → JWT tokens + current user
```

### Exercise Page UI Flow

```
┌──────────────────────────────────────────┐
│ Exercise Title              Difficulty: ★★ │
├──────────────────────────────────────────┤
│ Instructions (markdown)                    │
│                                            │
│ ┌────────────────────────────────────┐     │
│ │ Monaco Editor                      │     │
│ │ (starter code pre-loaded)          │     │
│ │                                    │     │
│ └────────────────────────────────────┘     │
│                                            │
│ [Run Code]  [Submit]  [Hint (2 remaining)] │
│                                            │
│ Test Results:                              │
│ ✓ Test 1: "Hello" → "Hello"               │
│ ✗ Test 2: Expected "World", got "world"    │
│ ? Test 3: (hidden — submit to reveal)      │
└──────────────────────────────────────────┘
```

---

## Phase 5: Content Authoring

### Seed Command

Build a management command (or script) that populates your database:

```bash
python manage.py seed_curriculum    # Create all modules, lessons, exercises
python manage.py flush --no-input   # Wipe and re-seed if content changes
```

### Content Structure Per Module

Each module should have 4 lessons in this order:

1. **Concept** (lesson_type=concept)
   - Markdown explaining the topic with examples
   - No exercises, no editor
   - Student reads and moves on

2. **Interactive Sandbox** (lesson_type=interactive)
   - Markdown with guided experiments
   - Pre-loaded sandbox_code in the editor
   - Student modifies and runs code freely
   - "Mark as Complete" button (no grading)

3. **Graded Exercises** (lesson_type=exercise)
   - 4-6 exercises of varying types and difficulty
   - Each exercise has test cases (visible + hidden) and hints
   - Must pass all exercises to complete the lesson

4. **Try It Yourself** (lesson_type=challenge)
   - Open-ended real-world scenarios
   - Empty editor, no grading
   - Builds confidence through application
   - "Mark as Complete" button

### Exercise Content Template

```
Title:          [Short, descriptive name]
Type:           [fill_blank | fix_bug | write_code | predict_output]
Difficulty:     [1-4]
XP:             [10-30, higher for harder]
Instructions:   [Markdown problem statement]
Starter Code:   [Code with # TODO markers or blanks to fill]
Solution Code:  [Reference solution]
Test Cases:
  - input: "", expected: "Hello, World!", hidden: false
  - input: "Alice", expected: "Hello, Alice!", hidden: true
Hints:
  - Level 1 (0% penalty):  "Think about what print() does..."
  - Level 2 (10% penalty): "You need to use an f-string: f\"Hello, {name}!\""
```

### XP Economy

| Element | Guideline |
|---------|-----------|
| XP per exercise | 10 (easy) to 30 (hard) |
| Hint level 1 | 0% penalty (free nudge) |
| Hint level 2 | 10% penalty |
| Hint level 3+ | 25-100% penalty (if you use more levels) |
| Rank thresholds | Space them exponentially — early ranks feel fast, later ones require commitment |
| Total curriculum XP | Should let a perfect student reach the second-highest rank. Highest rank = aspirational. |

---

## Phase 6: AI Integration

### Provider Pattern

Abstract your AI provider so you can swap implementations:

```python
class AIProvider(Protocol):
    def generate(self, system_prompt: str, user_prompt: str) -> str: ...

def get_provider() -> AIProvider:
    if settings.AI_BASE_URL:
        return OpenAICompatibleProvider()  # Ollama, LM Studio, etc.
    return CloudAPIProvider()              # Anthropic, OpenAI, etc.
```

### Three AI Features

**1. Contextual Hint**
```
System: You are a patient [SUBJECT] tutor helping an absolute beginner.
        Give a hint in 2-4 sentences. Guide their thinking — do NOT give the answer.
        Use simple language and analogies.

User:   Exercise: [title]
        Instructions: [instructions]
        Concepts: [concepts]
        Student's code: [code]
        Error: [error message]
```

**2. Code Critique** (only after passing)
```
System: The student just solved this exercise. Give brief, encouraging feedback.
        Celebrate their success. Suggest ONE way to improve. Keep it to 3-4 sentences.

User:   Exercise: [title]
        Student's solution: [code]
        Reference solution: [solution_code]
```

**3. Error Explanation**
```
System: Explain this error to someone who has never programmed before.
        Use plain English. 2-3 sentences max. No jargon.

User:   Code: [code]
        Error: [error message]
```

### Configuration

```env
# Cloud API (recommended)
AI_API_KEY=sk-...
AI_MODEL=claude-haiku-4-5-20241001    # Fast + cheap for hints

# OR Local LLM (free, private, offline)
AI_API_KEY=not-needed
AI_MODEL=llama3.2
AI_BASE_URL=http://localhost:11434/v1  # Ollama
```

---

## Phase 7: Production & Deployment

### Docker Compose Architecture

```
services:
  db:         PostgreSQL (persistent volume, healthcheck: pg_isready)
  backend:    App server (gunicorn/uvicorn, depends on healthy db)
  frontend:   Static build served by nginx
  nginx:      Reverse proxy (/api → backend, / → frontend)
```

### Dockerfile Strategy (Multi-Stage)

```dockerfile
# Stage 1: Build (large image with build tools)
FROM python:3.13-slim AS builder
# Install deps, collect static files

# Stage 2: Runtime (minimal image)
FROM python:3.13-slim
# Copy only the venv and app code from builder
# Reduces final image size significantly
```

### Entrypoint Script

```bash
#!/bin/sh
set -e
# Wait for database to be ready (retry loop)
# Run migrations (idempotent — safe to run every start)
# Collect static files
exec "$@"  # Then run the CMD (gunicorn)
```

### Health Checks

```yaml
backend:
  healthcheck:
    test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/v1/health/')"]
    interval: 30s
    timeout: 10s
    retries: 3
    start_period: 40s

nginx:
  depends_on:
    backend:
      condition: service_healthy
```

### Production Settings Checklist

```
Security:
  - [ ] SECRET_KEY: unique random value (reject insecure default)
  - [ ] ALLOWED_HOSTS: explicit domain list
  - [ ] CORS_ALLOWED_ORIGINS: explicit origin list
  - [ ] SECURE_SSL_REDIRECT: True
  - [ ] SECURE_PROXY_SSL_HEADER: ("HTTP_X_FORWARDED_PROTO", "https")
  - [ ] SESSION_COOKIE_SECURE: True
  - [ ] CSRF_COOKIE_SECURE: True
  - [ ] SECURE_HSTS_SECONDS: 3600 (start conservative)
  - [ ] SECURE_CONTENT_TYPE_NOSNIFF: True

Rate Limiting:
  - [ ] Code execution: 60/minute per user
  - [ ] Password reset: 5/hour per IP
  - [ ] Auth endpoints: 30/minute per IP

Database:
  - [ ] PostgreSQL (not SQLite)
  - [ ] Credentials via environment variables
  - [ ] Automated backups (pg_dump + gzip, cron daily)

Monitoring:
  - [ ] Error tracking (Sentry or equivalent)
  - [ ] Health check endpoint
```

### CI/CD Pipeline (GitHub Actions)

```yaml
Jobs:
  1. backend-tests:
     - Install deps, migrate, seed, run tests

  2. frontend-build:
     - Install deps, build (type-check + bundle)

  3. e2e-tests (needs 1 + 2):
     - Start both servers
     - Run Playwright against the running app
     - Upload test report as artifact

Triggers: push to main, pull requests
Concurrency: cancel-in-progress for same branch
```

### Backup Script

```bash
#!/bin/sh
# Timestamped gzipped dump
docker compose exec -T db pg_dump -U $DB_USER $DB_NAME | gzip > backups/backup_$(date +%Y%m%d_%H%M%S).sql.gz

# Optional: prune old backups
# PRUNE_DAYS=30 — delete backups older than 30 days
```

---

## Build Checklist

Use this to track your progress:

### Foundation
- [ ] Initialize backend project with framework of choice
- [ ] Initialize frontend project with build tool
- [ ] Set up development database
- [ ] Configure dev settings (CORS, ports, debug mode)

### Phase 1: Data Model
- [ ] User model with XP and rank progression
- [ ] Module, Lesson, Exercise, TestCase, Hint models
- [ ] Progress tracking models (module, lesson, exercise level)
- [ ] Run migrations

### Phase 2: Content
- [ ] Write seed command
- [ ] Author all module content (concept lessons in markdown)
- [ ] Author all exercises with test cases and hints
- [ ] Verify seed creates correct data

### Phase 3: Execution Engine
- [ ] Sandbox with restricted builtins and import whitelist
- [ ] Timeout mechanism
- [ ] Memory and recursion limits (save/restore after execution)
- [ ] Output comparison (flexible matching)
- [ ] Friendly error messages

### Phase 4: API
- [ ] Auth endpoints (register, login, token refresh, logout)
- [ ] Curriculum endpoints (modules, lessons, exercises)
- [ ] Submission endpoints (run, submit, history)
- [ ] Hint reveal endpoint
- [ ] Lesson completion endpoint
- [ ] Progress summary endpoint
- [ ] Module unlock cascade logic

### Phase 5: Frontend
- [ ] Auth pages (login, register, password reset)
- [ ] Dashboard with module list and progress
- [ ] Module page with lesson list
- [ ] Lesson page with markdown rendering
- [ ] Exercise page with code editor
- [ ] Submission flow (run → results → submit → XP)
- [ ] Hint reveal UI
- [ ] Profile page with stats

### Phase 6: AI (Optional)
- [ ] Provider abstraction
- [ ] Hint endpoint
- [ ] Critique endpoint
- [ ] Error explanation endpoint
- [ ] System prompts tuned for your audience

### Phase 7: Testing
- [ ] Backend unit tests
- [ ] E2E tests for critical user flows
- [ ] CI pipeline

### Phase 8: Production
- [ ] Dockerfile (multi-stage)
- [ ] docker-compose.yml
- [ ] Entrypoint with auto-migration
- [ ] Health checks
- [ ] Production settings (SSL, HSTS, rate limiting)
- [ ] Backup script
- [ ] README with setup instructions
