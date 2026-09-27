# Build context is the repository root. Base digests are reviewed with lock updates.
FROM ghcr.io/astral-sh/uv:0.11.10@sha256:bca7f6959666f3524e0c42129f9d8bbcfb0c180d847f5187846b98ff06125ead AS uv
FROM python:3.13-slim@sha256:7c61056e61ac89e852de05f3dc6fa51a6dd2181797bceed46aa725dd7cb2cd3b AS runtime-base
# libpq comes from Debian security updates; avoid binary wheels with vendored libs.
RUN apt-get update \
    && apt-get install --no-install-recommends -y libpq5 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && python -m pip uninstall -y pip

FROM runtime-base AS builder
COPY --from=uv /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project
COPY backend/ ./backend/
WORKDIR /app/backend
ENV DJANGO_SETTINGS_MODULE=config.settings.production \
    ALLOWED_HOSTS=localhost \
    CORS_ALLOWED_ORIGINS=http://localhost \
    PYTHONPATH=/app/backend
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
RUN useradd --create-home --uid 10001 --shell /usr/sbin/nologin pystarter \
    && chmod +x /app/backend/entrypoint.sh \
    && chown -R pystarter:pystarter /app/backend \
    && rm -f /usr/bin/infocmp /usr/bin/mount /usr/bin/umount /usr/bin/nsenter \
    && find /usr/bin /usr/sbin -type f -perm /6000 -exec chmod a-s {} +
USER pystarter
EXPOSE 8000
ENTRYPOINT ["/app/backend/entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
