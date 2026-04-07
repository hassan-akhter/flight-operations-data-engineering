CREATE TABLE IF NOT EXISTS silver_flights (
    id SERIAL PRIMARY KEY,
    ingestion_timestamp TIMESTAMP NOT NULL,
    flight_number TEXT,
    airline_name TEXT,
    airline_iata TEXT,
    departure_airport TEXT,
    departure_iata TEXT,
    arrival_airport TEXT,
    arrival_iata TEXT,
    scheduled_departure TIMESTAMP,
    actual_departure TIMESTAMP,
    scheduled_arrival TIMESTAMP,
    actual_arrival TIMESTAMP,
    departure_delay INT,
    arrival_delay INT,
    status TEXT
);
CREATE TABLE IF NOT EXISTS silver_airlines (
    airline_iata TEXT PRIMARY KEY,
    airline_name TEXT
);
CREATE TABLE IF NOT EXISTS silver_airports (
    airport_iata TEXT PRIMARY KEY,
    airport_name TEXT
);