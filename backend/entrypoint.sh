#!/bin/sh
set -e

echo "Waiting for database..."
attempts=30
while ! python -c "
import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings.production')
import django; django.setup()
from django.db import connection; connection.ensure_connection()
" 2>/dev/null; do
    attempts=$((attempts - 1))
    if [ "$attempts" -le 0 ]; then
        echo "Database timeout after 60s"
        exit 1
    fi
    sleep 2
done

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

exec "$@"
