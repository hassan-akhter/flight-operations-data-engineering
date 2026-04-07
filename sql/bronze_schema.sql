CREATE TABLE IF NOT EXISTS bronze_flights_raw (
    id SERIAL PRIMARY KEY,
    ingestion_timestamp TIMESTAMP NOT NULL,
    source TEXT NOT NULL,
    raw_json JSONB NOT NULL
);