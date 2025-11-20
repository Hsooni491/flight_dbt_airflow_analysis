import requests
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
import logging
from logging_config import setup_project_logger

logger = setup_project_logger()


def extract_flights_data(api_url):
	ACCESS_KEY = 'c3802848e60ca64d6224613b9484c92d'
	ROW_NUM = 100
	
	logger.info(f"Starting data extraction from API: {api_url}")

	r = requests.get(api_url, params={
		'access_key': ACCESS_KEY,
		'limit': ROW_NUM
	})
	assert r.status_code == 200, f"API request failed with status code {r.status_code}"

	logger.info(f"API request successful with status code {r.status_code}")
	records = []

	for id, flight in enumerate(r.json()['data'], 1):
		records.append({
			"flight_id": id,
			"flight_date": flight['flight_date'],
			"airline_name": flight['airline']['name'],
			"flight_number": flight['flight']['iata'],
			"dep_airport": flight['departure']['iata'],
			"dep_delay_time": flight['departure']['delay'],
			"dep_time": flight['departure']['scheduled'],
			"arr_airport": flight['arrival']['iata'],
			"arr_time": flight['arrival']['scheduled'],
			"flight_status": flight['flight_status'],
			"arr_delay_minutes": flight['arrival']['delay']
		})

	logger.info(f"Extracted {len(records)} flight records")

	# return records so Airflow XCom can store it
	return records


def load_flights_data(database_url, ti):
    # Pull the extracted JSON records from XCom
    records = ti.xcom_pull(task_ids='extract_api_flight_data')
    engine = create_engine(database_url)

    df = pd.DataFrame(records)
    df = df.to_sql(
		name='raw_flights',
		if_exists='append',
		con=engine,
		index=False
	)

