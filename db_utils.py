import psycopg2
from psycopg2 import sql

def save_to_db(data):
    print("Connecting to PostgreSQL...")

    try:
        conn = psycopg2.connect(
            dbname="flights",
            user="postgres",             # Replace with your actual username if different
            password="admin123",    # Replace with your actual password
            host="localhost",
            port="5432"
        )
        print("Connected to database.")
    except Exception as e:
        print("Error: Could not connect to the database.")
        print(e)
        return

    cur = conn.cursor()

    insert_query = sql.SQL("""
        INSERT INTO flight_fares (source, destination, travel_date, airline, price, scraped_at)
        VALUES (%s, %s, %s, %s, %s, DEFAULT)
    """)

    for row in data:
        try:
            print("Inserting row:", row)
            cur.execute(insert_query, row)
        except Exception as e:
            print("Error inserting row:", row)
            print(e)

    conn.commit()
    cur.close()
    conn.close()
    print("All data saved.")

