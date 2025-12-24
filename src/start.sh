#!/usr/bin/env bash
set -e

# check if required tables exist
TABLES_EXIST=$(python - <<'EOF'
import os
import psycopg2
url = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(url)
cur = conn.cursor()
tables = ['users', 'sessions', 'workouts']  # replace with actual table names
cur.execute(
    "SELECT tablename FROM pg_tables WHERE schemaname='public';"
)
existing = [row[0] for row in cur.fetchall()]
conn.close()
print('yes' if all(t in existing for t in tables) else 'no')
EOF
)

if [ "$TABLES_EXIST" = "no" ]; then
    echo "Tables missing, running DB setup..."
    python db_setup.py
    python create_tables.py
else
    echo "All tables exist, skipping DB setup."
fi

# start Flask
exec flask run --host=0.0.0.0 --reload
