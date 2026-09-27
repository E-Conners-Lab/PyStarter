# Build context is the repository root. Base digests are reviewed with lock updates.
FROM ghcr.io/astral-sh/uv:0.11.10@sha256:bca7f6959666f3524e0c42129f9d8bbcfb0c180d847f5187846b98ff06125ead AS uv
FROM python:3.13-alpine@sha256:79e7a9b9ff1cbceff819f856fb374477792a5967759d94df266de7b7b4120e6f AS runtime-base
# Owner-approved SEC-31 minimal-base exception; see .github/security/README.md.
# Use patched system libpq, with compiler tools confined to the builder.
RUN apk upgrade --no-cache \
    && apk add --no-cache libpq \
    && python -m pip uninstall -y pip

FROM runtime-base AS builder
RUN apk add --no-cache build-base libpq-dev
COPY --from=uv /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project --extra container
COPY backend/ ./backend/
WORKDIR /app/backend
ENV DJANGO_SETTINGS_MODULE=config.settings.production \
    ALLOWED_HOSTS=localhost \
    CORS_ALLOWED_ORIGINS=http://localhost \
    PYTHONPATH=/app/backend
RUN /app/.venv/bin/python -c "import psycopg"
# Ephemeral build-only key; never persisted in the final image configuration.
RUN DJANGO_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')" \
    /app/.venv/bin/python manage.py collectstatic --noinput

FROM runtime-base
WORKDIR /app/backend
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/backend /app/backend
ENV PATH="/app/.venv/bin:$PATH" \
    DJANGO_SETTINGS_MODULE=config.settings.production \
    PYTHONPATH=/app/backend \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
ARG APP_VERSION=1.0.8
ENV APP_VERSION=${APP_VERSION}
RUN addgroup -S -g 10001 pystarter \
    && adduser -S -u 10001 -G pystarter -h /home/pystarter -s /sbin/nologin pystarter \
    && chmod +x /app/backend/entrypoint.sh \
    && chown -R pystarter:pystarter /app/backend \
    && find /usr/bin /usr/sbin -type f -perm /6000 -exec chmod a-s {} +
USER pystarter
EXPOSE 8000
ENTRYPOINT ["/app/backend/entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
