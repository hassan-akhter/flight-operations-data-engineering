import psycopg2
import json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

PG_HOST = os.getenv("PG_HOST")
PG_DB = os.getenv("PG_DB")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")

def transform_bronze_to_silver():
    conn = psycopg2.connect(
        host=PG_HOST,
        dbname=PG_DB,
        user=PG_USER,
        password=PG_PASSWORD
    )
    cur = conn.cursor()

    # Get all raw JSON rows
    cur.execute("SELECT id, ingestion_timestamp, raw_json FROM bronze_flights_raw")
    rows = cur.fetchall()

    for row in rows:
        _, ingestion_ts, raw_json = row
        data = raw_json.get("data", [])

        for flight in data:
            airline = flight.get("airline", {})
            departure = flight.get("departure", {})
            arrival = flight.get("arrival", {})
            flight_info = flight.get("flight", {})

            insert_query = """
                INSERT INTO silver_flights (
                    ingestion_timestamp, flight_number, airline_name, airline_iata,
                    departure_airport, departure_iata, arrival_airport, arrival_iata,
                    scheduled_departure, actual_departure, scheduled_arrival, actual_arrival,
                    departure_delay, arrival_delay, status
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            cur.execute(insert_query, (
                ingestion_ts,
                flight_info.get("iata"),
                airline.get("name"),
                airline.get("iata"),
                departure.get("airport"),
                departure.get("iata"),
                arrival.get("airport"),
                arrival.get("iata"),
                departure.get("scheduled"),
                departure.get("actual"),
                arrival.get("scheduled"),
                arrival.get("actual"),
                departure.get("delay"),
                arrival.get("delay"),
                flight.get("status")
            ))

            # Insert airline
            if airline.get("iata"):
                cur.execute("""
                    INSERT INTO silver_airlines (airline_iata, airline_name)
                    VALUES (%s, %s)
                    ON CONFLICT (airline_iata) DO NOTHING
                """, (airline.get("iata"), airline.get("name")))

            # Insert airports
            if departure.get("iata"):
                cur.execute("""
                    INSERT INTO silver_airports (airport_iata, airport_name)
                    VALUES (%s, %s)
                    ON CONFLICT (airport_iata) DO NOTHING
                """, (departure.get("iata"), departure.get("airport")))

            if arrival.get("iata"):
                cur.execute("""
                    INSERT INTO silver_airports (airport_iata, airport_name)
                    VALUES (%s, %s)
                    ON CONFLICT (airport_iata) DO NOTHING
                """, (arrival.get("iata"), arrival.get("airport")))

    conn.commit()
    cur.close()
    conn.close()
    print("✔️ Silver layer updated successfully.")

if __name__ == "__main__":
    transform_bronze_to_silver()