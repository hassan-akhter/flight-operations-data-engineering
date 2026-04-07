import requests
import psycopg2
import json
from datetime import datetime
from dotenv import load_dotenv
import os
import time

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
PG_HOST = os.getenv("PG_HOST")
PG_DB = os.getenv("PG_DB")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")

BASE_URL = "http://api.aviationstack.com/v1/flights"

# -----------------------------
# Fetch flights from API
# -----------------------------
def fetch_flights(dep_iata, limit=100, offset=0):
    params = {
        "access_key": API_KEY,
        "dep_iata": dep_iata,
        "limit": limit,
        "offset": offset
    }

    response = requests.get(BASE_URL, params=params)

    # Handle API limit errors
    if response.status_code == 429:
        print("API rate limit reached. Sleeping for 60 seconds...")
        time.sleep(60)
        return fetch_flights(dep_iata, limit, offset)

    response.raise_for_status()
    return response.json()

# -----------------------------
# Save raw JSON to Postgres
# -----------------------------
def save_raw_to_db(data, source="aviationstack"):
    try:
        conn = psycopg2.connect(
            host=PG_HOST,
            dbname=PG_DB,
            user=PG_USER,
            password=PG_PASSWORD
        )
        cur = conn.cursor()

        insert_query = """
            INSERT INTO bronze_flights_raw (ingestion_timestamp, source, raw_json)
            VALUES (%s, %s, %s)
        """

        cur.execute(insert_query, (
            datetime.utcnow(),
            source,
            json.dumps(data)
        ))

        conn.commit()
        cur.close()
        conn.close()

        print("✔️ Data inserted into bronze_flights_raw")

    except Exception as e:
        print("Database insertion error:", e)

# -----------------------------
# Load airports dynamically
# -----------------------------
def load_airports_from_db():
    conn = psycopg2.connect(
        host=PG_HOST,
        dbname=PG_DB,
        user=PG_USER,
        password=PG_PASSWORD
    )
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT departure_airport_id
        FROM fact_flight
        UNION
        SELECT DISTINCT arrival_airport_id
        FROM fact_flight
    """)

    airports = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()

    print(f"Loaded {len(airports)} airports from dataset")
    return airports

# -----------------------------
# Main pipeline runner
# -----------------------------
def run_ingestion():
    airports = load_airports_from_db()

    for airport in airports:
        print(f"Fetching flights for {airport}...")

        # Fetch up to 500 flights per airport (safe for free API)
        for offset in range(0, 500, 100):
            print(f"   → Page offset {offset}")

            try:
                data = fetch_flights(dep_iata=airport, offset=offset)
                save_raw_to_db(data)
                time.sleep(1)  # avoid rate limits
            except Exception as e:
                print(f"Error fetching offset {offset} for {airport}: {e}")

    print("Ingestion pipeline completed.")

# -----------------------------
# Run script
# -----------------------------
if __name__ == "__main__":
    run_ingestion()