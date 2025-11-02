import psycopg2
from configparser import ConfigParser

# configuring based on the ini file
def config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)

    db_info = {}
    if parser.has_section(section):
        params = parser.items(section)

        # iterating through the key value pairs from the ini file
        for param in params:
            db_info[param[0]] = param[1]
    else:
        raise Exception("Section {0} not found in the {1} file".format(section, filename))

    return db_info

# connecting to postgresql
def connect():
    conn = None
    try:
        params = config()
        print("Connecting to PostgreSQL...")
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # printing out the version
        print("PostgreSQL version: ")
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed")


if __name__ == '__main__':
    connect()


