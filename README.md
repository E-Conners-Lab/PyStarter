# PyStarter

**Learn Python. Write Code. Level Up.**

A self-hosted training platform that teaches Python from scratch through interactive lessons, a sandboxed code editor, graded exercises, and AI-powered tutoring.

<img width="1499" height="770" alt="PyStarter Dashboard" src="https://github.com/user-attachments/assets/2f453ac4-816e-4ac8-9d22-d045875871e8" />

---

## What You Get

PyStarter is a complete, ready-to-run learning platform -- not a template or starter kit. Install it, seed the curriculum, and you have a fully functional Python course with 14 modules, 56 lessons, and 66 graded exercises.

### Built-in Code Editor
Write and run Python directly in the browser using the Monaco editor (the same engine behind VS Code). Syntax highlighting, auto-indentation, and a professional coding experience from day one.

### Sandboxed Execution
Student code runs in a restricted Python sandbox with an import whitelist, blocked dangerous builtins, 5-second timeouts, and memory limits. Safe enough for self-hosted use without worrying about what students might run.

### 4 Exercise Types
- **Fill in the Blank** -- complete partially written code
- **Fix the Bug** -- find and correct errors in broken code
- **Write Code** -- solve problems from scratch
- **Predict the Output** -- read code and predict what it prints

### Progressive Hint System
Each exercise offers two levels of hints. The first is free. The second costs 10% of the exercise's XP. Students are encouraged to try before asking for help.

### AI-Powered Tutoring
Three AI features powered by Claude (or any OpenAI-compatible LLM, including local models via Ollama):
- **Contextual Hints** -- the AI reads the student's code and error, then guides their thinking without giving the answer
- **Code Critique** -- after passing, the AI suggests one way to improve their solution
- **Error Explanations** -- cryptic Python errors translated into plain English

### XP and Belt Progression
Students earn XP for completing exercises and progress through 8 belt ranks -- White through Black. XP penalties from hints make perfect scores meaningful. The belt system gives students a visible sense of progress through the curriculum.

### Run vs Submit
"Run" lets students test their code against visible test cases with no stakes. "Submit" grades against all test cases (including hidden ones) and awards XP. This separation reduces anxiety and encourages experimentation.

---

## Curriculum

14 modules covering Python fundamentals through a network automation capstone. Each module follows the same structure: concept lesson, interactive sandbox, graded exercises, and open-ended challenges.

| # | Module | What Students Learn |
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
| 14 | Building a Network Toolkit | Capstone: validation functions, parsing pipelines, audit reports |

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Django 6, Django REST Framework, SimpleJWT |
| Frontend | React 19, TypeScript, Vite |
| Styling | TailwindCSS (dark theme) |
| Code Editor | Monaco Editor |
| State Management | Zustand + TanStack Query |
| AI | Anthropic Claude API (or any OpenAI-compatible LLM) |
| Database | SQLite (development) / PostgreSQL (production) |
| Deployment | Docker Compose with nginx reverse proxy |
| Testing | Playwright (99 E2E tests) + Django unit tests |
| CI/CD | GitHub Actions |

---

## Deployment Options

**Local development** -- Python 3.13 + Node.js 18. One setup script installs everything.

**Docker** -- `docker compose up` runs the full stack: PostgreSQL, Django + Gunicorn, React served by nginx, and a reverse proxy. Migrations run automatically on container start.

AI features are optional. The platform works fully without an API key -- students just won't have access to AI hints, code critique, or error explanations.

---

## Who It's For

- **Trainers and educators** building a Python course for their students
- **Bootcamp operators** who want a self-hosted, brandable training platform
- **Self-learners** who want a structured, gamified path through Python
- **Network engineers** learning Python for automation (modules 10 and 14 are tailored for this)

---

## Included Extras

Beyond the platform itself, every purchase includes:

- **`framework.md`** -- A reusable blueprint for building your own interactive learning platform. Covers data modeling, sandbox design, API architecture, frontend patterns, AI integration, and production deployment. Use it to build courses in other languages or subjects.
- **`skills.md`** -- A detailed implementation guide documenting every architectural decision, the build order, data models, API endpoints, and testing strategy behind PyStarter.
- **One-command setup scripts** for macOS, Linux, and Windows
- **Docker Compose** production config with PostgreSQL, nginx, health checks, and automated backups
- **GitHub Actions CI/CD** pipeline (backend tests, frontend build, 99 Playwright E2E tests)
- **Database backup script** with optional automated pruning

---

## License

Single-user license. You may use and modify the software for personal learning. Redistribution and commercial repackaging are prohibited. See [LICENSE](LICENSE) for full terms.

---

Built by **The Tech-E**
