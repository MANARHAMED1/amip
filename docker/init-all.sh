#!/bin/sh
# AMIP robust database initialization
# SQL files are mounted to /amip-sql/ to avoid entrypoint auto-execution.
# If database/data_inserts.sql is not present (it is intentionally NOT
# committed because it exceeds GitHub's 100 MB file limit), the tables are
# populated directly from the CSVs in generated_data/ via \copy.
set -e

DB="${POSTGRES_DB:-amip}"
USER="${POSTGRES_USER:-postgres}"
DIR="/amip-sql"

run_psql() {
    echo "[INIT] Running $1 ..."
    psql -v ON_ERROR_STOP=0 -U "$USER" -d "$DB" -f "$DIR/$1" || echo "[INIT] WARNING: $1 completed with warnings"
}

load_csv() {
    echo "[INIT] COPY $1 ..."
    psql -v ON_ERROR_STOP=1 -U "$USER" -d "$DB" \
        -c "\\copy $1 FROM '$DIR/generated_data/$1.csv' WITH (FORMAT csv, HEADER true)"
}

echo "[INIT] === AMIP Full Init ==="

run_psql 01-schema.sql
run_psql 01b-fix-actif.sql

if [ -f "$DIR/02-data.sql" ] && [ ! -d "$DIR/02-data.sql" ]; then
    run_psql 02-data.sql
else
    echo "[INIT] 02-data.sql not found - loading CSVs from generated_data/ (dependency order) ..."
    for t in secteur machine operateur matiere outil stock_outil piece \
             programme_usinage gamme_usinage phase_gamme ordre_fabrication \
             execution_phase execution_outil cause_rebut controle_qualite \
             maintenance sensor_data stock_piece stock_matiere; do
        load_csv "$t"
    done
fi

run_psql 03-warehouse-schema.sql
run_psql 04-warehouse-views.sql
run_psql 05-users.sql

echo "[INIT] === AMIP Init Complete ==="
