# Flight ETL with Airflow & dbt

Flight-dbt-airflow-analysis is a production-style ELT pipeline that highlights modern data engineering practices for aviation analytics. Apache Airflow orchestrates the workflow, AviationStack supplies live flight data, PostgreSQL stores the landing zone, and dbt transforms the records into business-ready marts. This repository is tailored for portfolio showcases and includes unit tests that emphasize engineering rigor.

## Highlights
- **Automated orchestration** – Airflow DAG (`airflow/dags/flight_elt_dag.py`) wires the extract → load → transform flow.
- **Resilient ingestion** – `extract_flights_data` normalizes AviationStack responses and enforces schemas before loading.
- **Warehouse-ready loading** – Pandas + SQLAlchemy push curated rows into the `raw_flights` table.
- **Modular transformations** – dbt models (`flight_dbt/`) deliver staging layers plus airline, airport, and status fact tables.
- **Test-first mindset** – Pytest coverage (`airflow/dags/extract/tests`) validates custom operators and mocks Airflow XCom behavior.

## Architecture
1. **Extract** – `extract_flights_data` calls `https://api.aviationstack.com/v1/flights`, limits the payload, and shapes the JSON.
2. **Load** – `load_flights_data` retrieves the records from Airflow XCom and appends them to PostgreSQL via SQLAlchemy.
3. **Transform** – A BashOperator triggers `dbt run` in `flight_dbt`, building staging models and fact marts on top of `raw_flights`.

```
AviationStack API ──> Airflow extract task ──> PostgreSQL raw_flights ──> dbt models ──> curated marts
```

## Tech Stack
- Apache Airflow 2.x
- PostgreSQL 14+ with SQLAlchemy
- dbt Core (Postgres adapter)
- Python 3.10+, pandas, requests
- Pytest for unit testing

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
raw_flights_sample.json      # example payload for quick validation
```

## Prerequisites
- Python 3.10+ and virtualenv/venv
- PostgreSQL instance reachable from Airflow
- AviationStack API key (free tier works for demos)
- Airflow CLI access (local install or managed service)

## Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-handle>/flight-dbt-airflow-analysis.git
   cd flight-dbt-airflow-analysis
   ```
2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies**
   ```bash
   pip install apache-airflow pandas sqlalchemy psycopg2-binary requests dbt-postgres pytest
   ```
4. **Configure credentials**
   - Replace `ACCESS_KEY` in `airflow/dags/extract/extract_flights.py` with your AviationStack token.
   - Update `database_url` in `airflow/dags/flight_elt_dag.py`, or move it into an Airflow connection/Variable for production use.
5. **Prepare PostgreSQL**
   - Ensure the target database/schema exists.
   - The loader creates `raw_flights` if needed; you can manually inspect schema using `raw_flights_sample.json`.

## Running the Pipeline
1. **Bootstrap Airflow**
   ```bash
   export AIRFLOW_HOME=$(pwd)/airflow
   airflow db init
   airflow users create \
     --username admin --password admin \
     --firstname Admin --lastname User --role Admin --email admin@example.com
   ```
2. **Start services (new terminals or background jobs)**
   ```bash
   airflow webserver --port 8080
   airflow scheduler
   ```
3. **Trigger the DAG**
   - Open `http://localhost:8080`, enable `elt_tasks`, and trigger a manual run.
   - Monitor logs to verify extract/load success and confirm dbt tasks finish.

## dbt Workflow
You can run dbt standalone to iterate quickly on models:
```bash
cd flight_dbt
dbt deps   # only if packages are added
dbt run
dbt test
```
Generated models materialize airline delays, airport performance, and status summaries for dashboarding.

## Testing
Execute the unit tests to validate the Airflow helpers and the XCom contract:
```bash
pytest airflow/dags/extract/tests/test_elt_functions.py
```
Add integration tests (e.g., dbt `sources` + `schema` tests or data-diff checks) as the project grows.

## Portfolio Guidance
- Document your environment in the GitHub description (Airflow/dbt/PostgreSQL versions, OS, Python version).
- Include screenshots of the Airflow graph view, task logs, and dbt documentation site for visual storytelling.
- Consider enhancements such as Airflow Connections/Secrets, CI for dbt, Dockerization, or deployments to Astronomer/AWS MWAA to showcase roadmap thinking.

Feel free to adapt this README for deployment-specific instructions (Docker Compose, Terraform, managed Airflow, etc.) before publishing.
