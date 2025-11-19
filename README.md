# Flight ETL with Airflow and dbt

Flight-dbt-airflow-analysis is a portfolio-ready ELT project that orchestrates an end-to-end pipeline for aviation data. Apache Airflow extracts fresh flights from the AviationStack API, loads them into PostgreSQL, and dbt builds curated marts for downstream analysis. The repo also includes pytest coverage for the custom Airflow tasks so you can demonstrate testing habits.

## Features
- Reproducible Airflow DAG (`airflow/dags/flight_elt_dag.py`) with extract → load → transform tasks
- API ingestion logic that normalizes flight responses into tabular records ready for warehousing
- Pandas + SQLAlchemy loader that appends to a `raw_flights` table in PostgreSQL
- dbt project (`flight_dbt/`) that stages the raw data and produces airline, airport, and status facts
- Pytest suite for extract/load helpers to highlight engineering rigor

## Architecture
1. **Extract** – `extract_flights_data` calls `https://api.aviationstack.com/v1/flights`, limits the payload, and shapes the JSON.
2. **Load** – `load_flights_data` pulls the extracted records from Airflow XCom and writes them into PostgreSQL via SQLAlchemy.
3. **Transform** – A BashOperator runs `dbt run` inside `flight_dbt` to build staging and mart models on top of `raw_flights`.

```
AviationStack API ──> Airflow extract task ──> PostgreSQL raw_flights ──> dbt models ──> curated marts
```

## Repository Layout
```
airflow/
  dags/
    flight_elt_dag.py        # DAG definition
    extract/
      extract_flights.py     # extract/load helpers
      tests/test_elt_functions.py
flight_dbt/
  models/staging             # source + staging model
  models/marts               # fact tables: airports, delays, status
  dbt_project.yml            # dbt configuration
raw_flights_sample.json      # small example payload
```

## Getting Started
1. **Clone the repo**
   ```bash
   git clone https://github.com/<your-handle>/flight-dbt-airflow-analysis.git
   cd flight-dbt-airflow-analysis
   ```
2. **Create a Python environment and install dependencies**
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install apache-airflow pandas sqlalchemy psycopg2-binary requests dbt-postgres pytest
   ```
   *Optional:* add a `requirements.txt` later so installs are scripted.
3. **Configure credentials**
   - Update `ACCESS_KEY` in `airflow/dags/extract/extract_flights.py` with your AviationStack key.
   - Edit `database_url` in `airflow/dags/flight_elt_dag.py` (or move it to an Airflow connection/Variable) so it points at your PostgreSQL instance.
4. **Prepare the database**
   - Ensure PostgreSQL is running and the target database/schema exists.
   - The loader will create the `raw_flights` table automatically, but you can seed it with `raw_flights_sample.json` if you want quick tests.
5. **Start Airflow**
   ```bash
   export AIRFLOW_HOME=$(pwd)/airflow
   airflow db init
   airflow webserver --port 8080 &
   airflow scheduler &
   ```
   Once the web UI is live, trigger the `elt_tasks` DAG or let it follow its schedule.
6. **Run dbt manually (optional)**
   ```bash
   cd flight_dbt
   dbt deps   # if you add packages later
   dbt run
   dbt test
   ```

## Testing
Run the pytest suite to validate the extract/load helpers, including the XCom integration mock:
```bash
pytest airflow/dags/extract/tests/test_elt_functions.py
```
Add more unit tests (e.g., for dbt macros via `dbt test` or Great Expectations) as you extend the project.

## Portfolio Tips
- Capture screenshots of the Airflow graph and dbt docs site for visuals.
- Mention the API, database, and tooling versions you used (Airflow 2.x, PostgreSQL 14+, dbt 1.x).
- Highlight opportunities for future work: Airflow connections, secrets management, CI for dbt, or deploying the DAG to Astronomer.

Feel free to tailor this README with deployment details (Docker, managed Airflow, etc.) before publishing to GitHub.
