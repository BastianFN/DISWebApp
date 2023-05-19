import csv
import psycopg2


def insert_ufo_sighting(sighting):
    from uffo import conn
    cur = conn.cursor()
    query = """INSERT INTO UFO_sightings (city, state, country, comments, date_posted, latitude, longitude) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    cur.execute(query, (sighting['city'], sighting['state'], sighting['country'],
                sighting['comments'], sighting['date_posted'], sighting['latitude'], sighting['longitude']))
    conn.commit()
    cur.close()


def select_all_ufo_sightings():
    from uffo import conn
    conn = psycopg2.connect(dbname='uffo', user='bastian', host='127.0.0.1', password='UIS')
    cursor = conn.cursor()
    
    cursor.execute("SELECT latitude, longitude, comments FROM UFO_sightings;")
    data = cursor.fetchall()  # Fetch all the data

    cursor.close()
    conn.close()

    return data

def get_ufo_comments(page=1, per_page=50):
    conn = psycopg2.connect(dbname='uffo', user='bastian', host='127.0.0.1', password='UIS')
    cursor = conn.cursor()

    cursor.execute(f"SELECT comments FROM UFO_sightings ORDER BY sighting_id ASC LIMIT {per_page} OFFSET {(page - 1) * per_page}")
    data = [row[0] for row in cursor.fetchall()]  # Fetch all the data

    cursor.close()
    conn.close()

    return data



# def import_from_csv(file_path):
#     with open(file_path, 'r') as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             insert_ufo_sighting(row)


# if __name__ == "__main__":
#     import_from_csv("scrubbed3.csv")
