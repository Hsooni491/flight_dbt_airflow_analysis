import sys
import os
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(project_root)
from extract.extract_flights import extract_flights_data, load_flights_data

api_url = 'https://api.aviationstack.com/v1/flights'
database_url = 'postgresql+psycopg2://postgres:1234@localhost:5432/mydb'

with DAG(
	'elt_tasks',
	default_args={
		'depends_on_past': False,
		'retries': 1,
		'retry_delay': timedelta(minutes=1)
	},
	description='An elt dag for extracting data, load it and transform it',
	schedule=timedelta(days=1),
	start_date=datetime(2025, 11, 18),
	catchup=False,
	tags=["example"]
) as dag:
	
	extract_data = PythonOperator(
		task_id="extract_api_flight_data",
		python_callable=extract_flights_data,
		op_kwargs={'api_url': api_url}
	)

	load_data = PythonOperator(
		task_id='load_data_to_postgres',
		python_callable=load_flights_data,
		op_kwargs={'database_url': database_url}
	)

	transform_data = BashOperator(
		task_id='run_dbt_models',
		bash_command="cd /home/hsooni/flight-dbt-airflow-analysis/flight_dbt && dbt run"
	)	

extract_data >> load_data >> transform_data