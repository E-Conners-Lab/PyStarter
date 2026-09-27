#!/bin/sh
set -eu
umask 077
cd "$(dirname "$0")"
if [ -e .env ]; then
    echo '.env already exists; leaving your settings unchanged.'
    exit 0
fi
command -v openssl >/dev/null 2>&1 || { echo 'Install OpenSSL, then rerun init.sh.'; exit 1; }
# noclobber prevents an accidental overwrite if another init starts concurrently.
set -C
{
    printf 'DJANGO_SECRET_KEY=%s\n' "$(openssl rand -hex 48)"
    printf 'DB_PASSWORD=%s\n' "$(openssl rand -hex 32)"
    printf 'POSTGRES_ADMIN_PASSWORD=%s\n' "$(openssl rand -hex 32)"
    printf 'NGINX_PORT=8080\nANTHROPIC_API_KEY=\nANTHROPIC_MODEL=\nANTHROPIC_BASE_URL=\n'
} > .env
echo 'Created private .env with unique local credentials.'
echo 'Optional: add your AI provider settings to .env. Then: docker compose up --build -d'
