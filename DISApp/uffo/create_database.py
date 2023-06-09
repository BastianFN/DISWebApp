import psycopg2
import csv

db = "dbname='uffo' user='bastian' host='127.0.0.1' password = ''"

# Helper function to validate floating point numbers
def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def create_database():
    # connect to the 'uffo' database
    conn = psycopg2.connect(db)
    cursor = conn.cursor()

    # drop the 'ufo_sightings' table if it exists
    cursor.execute("DROP TABLE IF EXISTS UFO_sightings;")

    # create the 'ufo_sightings' table
    cursor.execute("""
        CREATE TABLE UFO_sightings(
            sighting_id SERIAL PRIMARY KEY,
            city VARCHAR(255),
            state VARCHAR(255),
            country VARCHAR(255),
            comments TEXT,
            date_posted DATE,
            latitude FLOAT,
            longitude FLOAT
        );
    """)

    # commit the transaction
    conn.commit()

    # load data from csv file
    with open("UFO/scrubbed3.csv", "r") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)  # Skip the header row.
        for row in reader:
            if len(row) >= 7 and is_float(row[5]) and is_float(row[6]):
                try:
                    cursor.execute(
                        "INSERT INTO UFO_sightings (city, state, country, comments, date_posted, latitude, longitude) VALUES (%s, %s, %s, %s, TO_DATE(%s, 'MM/DD/YYYY'), %s, %s)",
                        (row[0], row[1], row[2], row[3], row[4], row[5], row[6]),
                    )
                    conn.commit()
                except Exception as e:
                    print(f"Error occurred: {e}")
                    conn.rollback()
            else:
                print(f"Invalid data: {row}")

    # close the cursor and the connection
    cursor.close()
    conn.close()

def create_user_table():
    conn = psycopg2.connect(db)
    cur = conn.cursor()

    # drop the 'users' table if it exists along with dependent objects
    cur.execute("DROP TABLE IF EXISTS users CASCADE;")

    cur.execute("""
        CREATE TABLE users(
            username VARCHAR(30) PRIMARY KEY,
            password varchar(120)
        );
    """)

    conn.commit()
    cur.close()

def create_post_table():
    conn = psycopg2.connect(db)
    cur = conn.cursor()

    # drop the 'Posts' table if it exists
    cur.execute("DROP TABLE IF EXISTS Posts;")

    cur.execute("""
        CREATE TABLE Posts(
            post_number SERIAL PRIMARY KEY,
            longitude DECIMAL(11,8),
            latitude DECIMAL(11,8),
            comments TEXT,
            date_posted DATE,
            username VARCHAR(30) REFERENCES Users(username)
        );
    """)

    conn.commit()
    cur.close()

def create_user_sightings_table():
    conn = psycopg2.connect(db)
    cur = conn.cursor()

    # drop the 'User_sightings' table if it exists
    cur.execute("DROP TABLE IF EXISTS User_sightings;")

    cur.execute("""
        CREATE TABLE User_sightings(
            sighting_id SERIAL PRIMARY KEY,
            comments TEXT,
            latitude FLOAT,
            longitude FLOAT,
            username VARCHAR(30) REFERENCES users(username)
        );
    """)

    conn.commit()
    cur.close()

def add_to_ufo_sightings():
    conn = psycopg2.connect(db)
    cur = conn.cursor()

    cur.execute("""
        CREATE OR REPLACE FUNCTION add_to_ufo_sightings() RETURNS TRIGGER AS $$
        BEGIN
            INSERT INTO UFO_sightings (comments, latitude, longitude) 
            VALUES (NEW.comments, NEW.latitude, NEW.longitude);
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    conn.commit()
    cur.close()

def create_trigger():
    conn = psycopg2.connect(db)
    cur = conn.cursor()

    cur.execute("""
        DROP TRIGGER IF EXISTS update_ufo_sightings_trigger ON Posts;
        CREATE TRIGGER update_ufo_sightings_trigger
        AFTER INSERT ON Posts
        FOR EACH ROW EXECUTE FUNCTION add_to_ufo_sightings();
    """)

    conn.commit()
    cur.close()

def add_users():
    conn = psycopg2.connect(db)
    cur = conn.cursor()

    users = [("bastian", "1"), ("simon", "2"), ("magnus", "3"), ("kasper", "4"), ("dis", "uffo")]

    for user in users:
        cur.execute("""
            INSERT INTO users (username, password) VALUES (%s, %s);
        """, (user[0], user[1]))

    conn.commit()
    cur.close()

# Run the functions
create_database()
create_user_table()
add_users()
create_post_table()
create_user_sightings_table()
add_to_ufo_sightings()
create_trigger()
