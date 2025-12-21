import os
import psycopg2

def create_tables():
    conn = None
    try:
        # gets its own connection separate from db_setup
        database_url = os.environ["DATABASE_URL"]
        conn = psycopg2.connect(database_url)

        with conn:
            with conn.cursor() as cur:
                # Users table
                cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id SERIAL PRIMARY KEY,
                    username VARCHAR(255) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
                    weight_lbs NUMERIC,
                    height_ft NUMERIC,
                    age INTEGER,
                    gender VARCHAR(255) NOT NULL
                );
                """)

                # Sessions table
                cur.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                    session_date TIMESTAMP WITH TIME ZONE DEFAULT now(),
                    duration_mins NUMERIC,
                    session_type VARCHAR(255) NOT NULL,
                    muscle_group VARCHAR(255) NOT NULL
                );
                """)

                # Workouts table
                cur.execute("""
                CREATE TABLE IF NOT EXISTS workouts (
                    workout_id SERIAL PRIMARY KEY,
                    session_id INTEGER NOT NULL REFERENCES sessions(session_id) ON DELETE CASCADE,
                    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                    exercise_name VARCHAR(255) NOT NULL,
                    num_sets INTEGER,
                    num_reps INTEGER,
                    weight_lbs NUMERIC,
                    muscle VARCHAR(255) NOT NULL
                );
                """)

                print("Tables created successfully (if they did not exist)")

    except Exception as e:
        print(f"Error creating tables: {e}")

    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    create_tables()
