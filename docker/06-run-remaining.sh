#!/bin/bash
# Run after 02-data.sql regardless of its exit code
set +e

echo "[INIT] Running warehouse schema..."
psql -v ON_ERROR_STOP=0 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /docker-entrypoint-initdb.d/03-warehouse-schema.sql

echo "[INIT] Running warehouse views..."
psql -v ON_ERROR_STOP=0 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /docker-entrypoint-initdb.d/04-warehouse-views.sql

echo "[INIT] Running users table..."
psql -v ON_ERROR_STOP=0 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /docker-entrypoint-initdb.d/05-users.sql

echo "[INIT] Post-data init complete."
