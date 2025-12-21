import os
import psycopg2


# connecting to postgres
# uses env vars
def connect():
    conn = None
    try:
        database_url = os.environ["DATABASE_URL"]

        print("Connecting to Postgres...")
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()

        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        print("PostgreSQL version:", db_version)

        cur.close()
    except Exception as error:
        print("Database connection error:", error)
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed")


if __name__ == "__main__":
    connect()
