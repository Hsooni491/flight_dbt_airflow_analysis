def test_extract_flights_data():
	from extract.extract_flights import extract_flights_data
	api_url = 'https://api.aviationstack.com/v1/flights'
	records = extract_flights_data(api_url=api_url)
	assert isinstance(records, list)
	assert len(records) > 0
	assert isinstance(records[0], dict)



def test_load_flights_data():
	from extract.extract_flights import load_flights_data
	import pandas as pd
	from unittest.mock import MagicMock

	database_url = 'postgresql+psycopg2://postgres:1234@localhost:5432/mydb'

	# Mock the XCom pull to return sample data
	sample_records = [
		{
			"flight_id": 1,
			"flight_date": "2023-01-01",
			"airline_name": "Test Airline",
			"flight_number": "TA123",
			"dep_airport": "JFK",
			"dep_delay_time": 10,
			"dep_time": "2023-01-01T10:00:00",
			"arr_airport": "LAX",
			"arr_time": "2023-01-01T13:00:00",
			"flight_status": "scheduled",
			"arr_delay_minutes": 5
		}
	]

	ti_mock = MagicMock()
	ti_mock.xcom_pull.return_value = sample_records

	load_flights_data(database_url, ti_mock)

	# Verify data was loaded correctly
	from sqlalchemy import create_engine, text

	engine = create_engine(database_url)
	with engine.connect() as conn:
		result = conn.execute(text("SELECT * FROM raw_flights"))
		rows = result.fetchall()
		assert rows[0]['flight_id'] == 1