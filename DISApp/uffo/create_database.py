import psycopg2
import csv

# Helper function to validate floating point numbers
def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def create_database():
    # connect to the 'uffo' database
    conn = psycopg2.connect(dbname='uffo', user='bastian', host='127.0.0.1', password='UIS')
    cursor = conn.cursor()

    # drop the 'ufo_sightings' table if it exists
    cursor.execute('''
        DROP TABLE IF EXISTS UFO_sightings;
    ''')

    # create the 'ufo_sightings' table
    cursor.execute('''
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
    ''')

    # commit the transaction
    conn.commit()

    # load data from csv file
    with open('UFO/scrubbed3.csv', 'r') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)  # Skip the header row.
        for row in reader:
            if len(row) >= 7 and is_float(row[5]) and is_float(row[6]):
                try:
                    cursor.execute(
                        "INSERT INTO UFO_sightings (city, state, country, comments, date_posted, latitude, longitude) VALUES (%s, %s, %s, %s, TO_DATE(%s, 'MM/DD/YYYY'), %s, %s)",
                        (row[0], row[1], row[2], row[3], row[4], row[5], row[6])
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

# Run the function
create_database()
