✈️ Flight Operations Analytics
A full end-to-end data pipeline — from raw API data to an interactive Power BI dashboard.
Show Image
Show Image
Show Image
Show Image

What is this?
I built this project to practice the full data engineering lifecycle — not just the analysis part, but everything that comes before it: ingesting raw data, cleaning it, modeling it properly, and then making it useful through a dashboard.
The data comes from the AviationStack API and covers real flight operations including delays, airline performance, airport traffic, and route efficiency.

What I built

An automated ETL pipeline in Python
A Bronze → Silver → Gold data architecture in PostgreSQL
A star schema with dimension and fact tables
Reusable SQL KPI views
A 3-page interactive Power BI dashboard

Numbers:

16,273 flights processed
193 airlines
176 airports


Architecture
AviationStack API
       ↓
  Bronze Layer       ← raw JSON stored as-is
       ↓
  Silver Layer       ← cleaned and structured tables
       ↓
  Gold Layer         ← star schema ready for analysis
       ↓
  Power BI           ← KPIs, charts, and slicers
The layered approach makes the pipeline easy to debug, maintain, and extend.

Tech Stack
ToolPurposePythonETL scripts, API calls, data cleaningPostgreSQLData storage and modelingSQLSchema design, KPI viewsPower BIDashboard and visualizationsDAXCalculated measures

ETL Pipeline
1. Bronze — Raw Ingestion (fetch_flights.py)
Pulls flight data from the AviationStack API and stores the raw JSON response into a PostgreSQL table. No transformations here — just raw data as it came in.
2. Silver — Cleaning (bronze_to_silver.py)
Reads the raw JSON, extracts what matters (airlines, airports, flight details), and loads it into clean structured tables.
3. Gold — Star Schema (silver_to_gold.py)
Builds the final model:

dim_airline — airline details
dim_airport — airport details
dim_time — time dimension generated dynamically
fact_flight — one row per flight with all foreign keys


Power BI Dashboard
Page 1 — Flight Operations Overview
A high-level view of the entire dataset. KPIs at the top, breakdowns by airline and airport, and a flights-by-hour line chart.
Page 2 — Airline Performance Deep Dive
Focuses on individual airline performance — who delays the most, who has the best on-time rate, and what the busiest route is.
Page 3 — Route & Delay Exploration
Deeper exploration with scatter plots, delay trends, and route-level filtering.
Screenshots are in the /screenshots folder.

KPI Views
The dashboard is powered by reusable SQL views:

kpi_on_time_performance
kpi_avg_departure_delay
kpi_avg_arrival_delay
kpi_cancellation_rate
kpi_busiest_routes
kpi_peak_hours

These views make it easy to update the dashboard or plug the data into other tools later.

Folder Structure
flight-ops-project/
│
├── powerbi/
│   └── Flight_Dashboard.pbix
│
├── screenshots/
│   ├── overview_page.png
│   ├── airline_performance_page.png
│   └── exploration_page.png
│
├── sql/
│   ├── bronze_schema.sql
│   ├── silver_schema.sql
│   ├── gold_schema.sql
│   ├── kpi_views.sql
│   └── sample_queries.sql
│
├── src/
│   ├── fetch_flights.py
│   ├── bronze_to_silver.py
│   └── silver_to_gold.py
│
├── .env
├── .gitignore
└── README.md

How to Run
1. Create a .env file with your credentials:
PG_HOST=...
PG_DB=...
PG_USER=...
PG_PASSWORD=...
AVIATIONSTACK_API_KEY=...
2. Run the pipeline in order:
bashpython src/fetch_flights.py
python src/bronze_to_silver.py
python src/silver_to_gold.py
3. Open Power BI:
Load Flight_Dashboard.pbix and click Refresh.

Limitations

Data covers one day due to the API free tier
Real-time refresh needs an active API key
Some route data derived from IATA codes


What I learned
This project taught me how much work happens before the dashboard. The pipeline, the schema design, the cleaning logic — that's where most of the real engineering is. The dashboard is the last 20%.

Built by Hassan — open to feedback and contributions.