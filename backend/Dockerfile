# Build context is the repo root (set in docker-compose.yml)
# ── Stage 1: Build ──
FROM python:3.13-slim AS builder

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev 2>/dev/null || uv sync --no-dev

COPY backend/ ./backend/

WORKDIR /app/backend

ENV DJANGO_SETTINGS_MODULE=config.settings.production
ENV DJANGO_SECRET_KEY=build-placeholder
ENV ALLOWED_HOSTS=localhost
ENV CORS_ALLOWED_ORIGINS=http://localhost

RUN PYTHONPATH=/app/backend uv run python manage.py collectstatic --noinput

# ── Stage 2: Runtime ──
FROM python:3.13-slim

WORKDIR /app

COPY --from=builder /app .

WORKDIR /app/backend

ENV PATH="/app/.venv/bin:$PATH"
ENV DJANGO_SETTINGS_MODULE=config.settings.production
ENV PYTHONPATH=/app/backend

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
