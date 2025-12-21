#!/usr/bin/env bash
set -e

# reaching postgres
echo "Connecting to Postgres..."
until python - <<'EOF'
import os
import psycopg2
import time

url = os.environ.get("DATABASE_URL")
try:
    psycopg2.connect(url).close()
    print("Postgres is ready.")
except Exception:
    raise SystemExit(1)
EOF
do
  sleep 1
done

# running the db_setup.py script and create_tables.py
echo "Running DB setup and creating tables..."
python db_setup.py
python create_tables.py

# flask
echo "Starting Flask..."
exec flask run --host=0.0.0.0
