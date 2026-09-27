#!/bin/sh
set -eu
# The application owns only its database; it never receives cluster-admin keys.
psql --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" \
    --set=ON_ERROR_STOP=1 --set=app_password="$APP_DB_PASSWORD" <<'SQL'
CREATE ROLE pystarter LOGIN PASSWORD :'app_password' NOSUPERUSER NOCREATEDB NOCREATEROLE;
ALTER DATABASE pystarter OWNER TO pystarter;
ALTER SCHEMA public OWNER TO pystarter;
SQL
