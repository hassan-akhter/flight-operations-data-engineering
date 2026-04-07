-- KPI 1: On-time performance
CREATE OR REPLACE VIEW kpi_on_time_performance AS
SELECT
    COUNT(*) FILTER (WHERE departure_delay <= 15 OR departure_delay IS NULL) * 100.0 
        / COUNT(*) AS on_time_percentage
FROM fact_flight;

-- KPI 2: Average departure delay
CREATE OR REPLACE VIEW kpi_avg_departure_delay AS
SELECT
    AVG(departure_delay) AS avg_departure_delay_minutes
FROM fact_flight
WHERE departure_delay IS NOT NULL;

-- KPI 3: Average arrival delay
CREATE OR REPLACE VIEW kpi_avg_arrival_delay AS
SELECT
    AVG(arrival_delay) AS avg_arrival_delay_minutes
FROM fact_flight
WHERE arrival_delay IS NOT NULL;

-- KPI 4: Cancellation rate
CREATE OR REPLACE VIEW kpi_cancellation_rate AS
SELECT
    COUNT(*) FILTER (WHERE status = 'cancelled') * 100.0 / COUNT(*) AS cancellation_rate
FROM fact_flight;

-- KPI 5: Busiest routes
CREATE OR REPLACE VIEW kpi_busiest_routes AS
SELECT
    da.airport_iata AS departure_iata,
    aa.airport_iata AS arrival_iata,
    COUNT(*) AS flight_count
FROM fact_flight f
JOIN dim_airport da ON f.departure_airport_id = da.airport_id
JOIN dim_airport aa ON f.arrival_airport_id = aa.airport_id
GROUP BY da.airport_iata, aa.airport_iata
ORDER BY flight_count DESC
LIMIT 10;

-- KPI 6: Peak hours
CREATE OR REPLACE VIEW kpi_peak_hours AS
SELECT
    t.hour,
    COUNT(*) AS flights
FROM fact_flight f
JOIN dim_time t ON f.scheduled_departure_time_id = t.time_id
GROUP BY t.hour
ORDER BY flights DESC;