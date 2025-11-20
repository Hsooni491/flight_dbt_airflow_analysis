# Flight ELT with Airflow & dbt

**Flight-dbt-airflow-analysis** is a production-grade ELT pipeline demonstrating modern data engineering best practices for aviation analytics. Apache Airflow orchestrates the workflow, AviationStack supplies live flight data, PostgreSQL stores the landing zone, and dbt transforms raw records into business-ready data marts.

---

## ✨ Highlights

- **Automated Orchestration** – Airflow DAG (`airflow/dags/flight_elt_dag.py`) orchestrates the complete extract → load → transform workflow
- **Resilient Ingestion** – `extract_flights_data` normalizes AviationStack API responses and enforces schemas before loading
- **Warehouse-Ready Loading** – Pandas + SQLAlchemy efficiently push curated rows into the `raw_flights` table
- **Modular Transformations** – dbt models (`flight_dbt/`) deliver staging layers plus airline, airport, and status fact tables
- **Test-First Mindset** – Pytest coverage (`airflow/dags/extract/tests`) validates custom operators and mocks Airflow XCom behavior
- **Structured Logging** – Custom logging integrated across extract & load steps for enhanced observability and debugging

---

## 📊 Architecture

```
AviationStack API 
    ↓
Airflow Extract Task (with logging)
    ↓
PostgreSQL raw_flights table
    ↓
dbt Models (staging + marts)
    ↓
Curated Data Marts
```

**ELT Pipeline Flow:**
1. **Extract** – `extract_flights_data` calls the AviationStack API, limits payload size, logs request/response metadata, and shapes JSON data
2. **Load** – `load_flights_data` retrieves XCom records, logs insert operations, and appends data to PostgreSQL via SQLAlchemy
3. **Transform** – BashOperator triggers `dbt run` in `flight_dbt/`, building staging models and fact marts on top of `raw_flights`

---

## 🪵 Logging

The project includes an enhanced logging layer for comprehensive traceability throughout the ELT pipeline.

### What's Logged?

- API call events with request start/end timestamps
- Number of records extracted per run
- Schema validation results and data quality checks
- Data load operations (rows inserted, target table, connection status)
- Error handling with detailed exception messages and stack traces

### Where Logs Appear

- **Airflow Task Logs** – Located in `airflow/logs/...` with full task execution history
- **Python Application Logs** – Using standard `logging` module within:
  - `extract_flights_data`
  - `load_flights_data`

### Why It Matters

Enhanced logging provides:
- **Faster Debugging** – Quickly identify API failures or database connection issues
- **ETL Throughput Visibility** – Track record counts and processing times
- **Production-Grade Observability** – Monitor pipeline health and data quality in real-time
- **Audit Trail** – Complete record of all extraction and loading operations

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Orchestration** | Apache Airflow 2.x |
| **Database** | PostgreSQL 14+ with SQLAlchemy |
| **Transformation** | dbt Core (Postgres adapter) |
| **Language** | Python 3.10+ |
| **Data Processing** | pandas, requests |
| **Testing** | pytest |
| **Observability** | Python logging module |

---

## 📁 Repository Structure

```
flight-dbt-airflow-analysis/
├── airflow/
│   ├── dags/
│   │   ├── flight_elt_dag.py              # Main DAG definition
│   │   └── extract/
│   │       ├── extract_flights.py         # Extract/load helpers with logging
│   │       └── tests/
│   │           └── test_elt_functions.py  # Unit tests
│   └── logs/                              # Airflow task logs
├── flight_dbt/
│   ├── models/
│   │   ├── staging/                       # Staging layer models
│   │   └── marts/                         # Business logic marts
│   └── dbt_project.yml                    # dbt configuration
├── raw_flights_sample.json                # Sample API response
└── README.md
```

---

## 🚀 Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Hsooni491/flight-dbt-airflow-analysis.git
cd flight-dbt-airflow-analysis
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install apache-airflow pandas sqlalchemy psycopg2-binary requests dbt-postgres pytest
```

### 4. Configure Credentials

- Set `ACCESS_KEY` in `extract_flights.py` with your AviationStack API key
- Update `database_url` in `flight_elt_dag.py` or configure via Airflow connections

### 5. Prepare PostgreSQL

- Ensure database and schema exist
- The loader automatically creates the `raw_flights` table if missing

---

## ▶️ Running the Pipeline

### Initialize Airflow

```bash
export AIRFLOW_HOME=$(pwd)/airflow
airflow db init
airflow users create \
  --username admin \
  --password admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com
```

### Start Airflow Services

```bash
# Terminal 1: Start webserver
airflow webserver --port 8080

# Terminal 2: Start scheduler
airflow scheduler
```

### Execute the DAG

1. Navigate to `http://localhost:8080`
2. Enable the `elt_tasks` DAG in the UI
3. Trigger manually or wait for scheduled run
4. Inspect logs to view extract/load/transform steps with detailed logging

---

## 🔄 dbt Workflow

Run dbt transformations independently:

```bash
cd flight_dbt
dbt run    # Execute all models
dbt test   # Run data quality tests
```

---

## 🧪 Testing

Run the test suite:

```bash
pytest airflow/dags/extract/tests/test_elt_functions.py
```

The test suite includes:
- Unit tests for extraction logic
- XCom behavior mocking
- Schema validation tests
- Error handling verification

---

## 📧 Contact

For questions, collaboration opportunities, or bug reports:
- **GitHub Issues**: [Open an issue](https://github.com/Hsooni491/flight-dbt-airflow-analysis/issues)
- **LinkedIn**: [Alhussain Baalawi](https://www.linkedin.com/in/alhussain-baalawi)

---

**Built with ❤️ for modern data engineering**