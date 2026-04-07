CREATE TABLE IF NOT EXISTS dim_airline (
    airline_id SERIAL PRIMARY KEY,
    airline_iata TEXT UNIQUE,
    airline_name TEXT
);

CREATE TABLE IF NOT EXISTS dim_airport (
    airport_id SERIAL PRIMARY KEY,
    airport_iata TEXT UNIQUE,
    airport_name TEXT,
    city TEXT,
    country TEXT
);

CREATE TABLE IF NOT EXISTS dim_time (
    time_id SERIAL PRIMARY KEY,
    full_timestamp TIMESTAMP,
    date DATE,
    year INT,
    month INT,
    day INT,
    hour INT,
    weekday INT
);

CREATE TABLE IF NOT EXISTS fact_flight (
    flight_id SERIAL PRIMARY KEY,
    ingestion_timestamp TIMESTAMP NOT NULL,

    airline_id INT REFERENCES dim_airline(airline_id),
    departure_airport_id INT REFERENCES dim_airport(airport_id),
    arrival_airport_id INT REFERENCES dim_airport(airport_id),

    scheduled_departure_time_id INT REFERENCES dim_time(time_id),
    actual_departure_time_id INT REFERENCES dim_time(time_id),
    scheduled_arrival_time_id INT REFERENCES dim_time(time_id),
    actual_arrival_time_id INT REFERENCES dim_time(time_id),

    flight_number TEXT,
    status TEXT,
    departure_delay INT,
    arrival_delay INT
);