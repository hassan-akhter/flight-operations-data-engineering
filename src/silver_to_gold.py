import psycopg2
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

PG_HOST = os.getenv("PG_HOST")
PG_DB = os.getenv("PG_DB")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")

def insert_time_dimension(cur, timestamp):
    if timestamp is None:
        return None

    cur.execute("""
        INSERT INTO dim_time (full_timestamp, date, year, month, day, hour, weekday)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING time_id
    """, (
        timestamp,
        timestamp.date(),
        timestamp.year,
        timestamp.month,
        timestamp.day,
        timestamp.hour,
        timestamp.weekday()
    ))

    return cur.fetchone()[0]

def transform_silver_to_gold():
    conn = psycopg2.connect(
        host=PG_HOST,
        dbname=PG_DB,
        user=PG_USER,
        password=PG_PASSWORD
    )
    cur = conn.cursor()

    cur.execute("SELECT * FROM silver_flights")
    rows = cur.fetchall()

    for row in rows:
        (
            silver_id, ingestion_ts, flight_number, airline_name, airline_iata,
            dep_airport, dep_iata, arr_airport, arr_iata,
            sched_dep, act_dep, sched_arr, act_arr,
            dep_delay, arr_delay, status
        ) = row

        # Insert airline
        cur.execute("""
            INSERT INTO dim_airline (airline_iata, airline_name)
            VALUES (%s, %s)
            ON CONFLICT (airline_iata) DO UPDATE SET airline_name = EXCLUDED.airline_name
            RETURNING airline_id
        """, (airline_iata, airline_name))
        airline_id = cur.fetchone()[0]

        # Insert airports
        cur.execute("""
            INSERT INTO dim_airport (airport_iata, airport_name)
            VALUES (%s, %s)
            ON CONFLICT (airport_iata) DO UPDATE SET airport_name = EXCLUDED.airport_name
            RETURNING airport_id
        """, (dep_iata, dep_airport))
        dep_airport_id = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO dim_airport (airport_iata, airport_name)
            VALUES (%s, %s)
            ON CONFLICT (airport_iata) DO UPDATE SET airport_name = EXCLUDED.airport_name
            RETURNING airport_id
        """, (arr_iata, arr_airport))
        arr_airport_id = cur.fetchone()[0]

        # Insert time dimensions
        sched_dep_id = insert_time_dimension(cur, sched_dep)
        act_dep_id = insert_time_dimension(cur, act_dep)
        sched_arr_id = insert_time_dimension(cur, sched_arr)
        act_arr_id = insert_time_dimension(cur, act_arr)

        # Insert fact row
        cur.execute("""
            INSERT INTO fact_flight (
                ingestion_timestamp, airline_id, departure_airport_id, arrival_airport_id,
                scheduled_departure_time_id, actual_departure_time_id,
                scheduled_arrival_time_id, actual_arrival_time_id,
                flight_number, status, departure_delay, arrival_delay
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            ingestion_ts, airline_id, dep_airport_id, arr_airport_id,
            sched_dep_id, act_dep_id, sched_arr_id, act_arr_id,
            flight_number, status, dep_delay, arr_delay
        ))

    conn.commit()
    cur.close()
    conn.close()
    print("✔️ Gold layer updated successfully.")

if __name__ == "__main__":
    transform_silver_to_gold()