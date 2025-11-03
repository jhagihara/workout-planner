import psycopg2
from db_setup import config

# creates a user table, session table, workout info table
def create_tables():
    try:
        params = config()
        conn = psycopg2.connect(**params)
    except Exception as e:
        print(f"Unable to connect: {e}")
        return

    try:
        with conn:
            # using with for automatic commit
            with conn.cursor() as cur:
                # creating the users table
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        user_id SERIAL PRIMARY KEY,
                        username VARCHAR(255) NOT NULL UNIQUE,
                        password VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
                        split_type VARCHAR(255) NOT NULL,
                        weight_lbs NUMERIC,
                        height_ft NUMERIC,
                        age INTEGER,
                        gender VARCHAR(255) NOT NULL
                    );
                    """
                )

                # sessions table linking to users
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS sessions (
                        session_id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                        session_date TIMESTAMP WITH TIME ZONE DEFAULT,
                        duration_mins NUMERIC,
                        session_type VARCHAR(255) NOT NULL,
                        muscle_group VARCHAR(255) NOT NULL
                    );
                    """
                )

                # workouts table linking to sessions
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS workouts (
                        workout_id SERIAL PRIMARY KEY,
                        session_id INTEGER NOT NULL REFERENCES sessions(session_id) ON DELETE CASCADE,
                        name VARCHAR(255) NOT NULL,
                        sets INTEGER,
                        reps INTEGER,
                        weight_lbs NUMERIC,
                        muscle VARCHAR(255) NOT NULL
                    );
                    """
                )

                print("Tables created (if they did not already exist)")
    except Exception as e:
        print(f"Error creating tables: {e}")
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()
