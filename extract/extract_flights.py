import requests
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine

ACCESS_KEY = 'c3802848e60ca64d6224613b9484c92d'
ROW_NUM = 100

# API Request
r = requests.get(f'https://api.aviationstack.com/v1/flights', params={
	'access_key': ACCESS_KEY,
	'dep_iata': 'JED',
	'limit': ROW_NUM
})

# Database connection
engine = create_engine('postgresql+psycopg2://postgres:1234@localhost:5432/mydb')

flights_df = pd.DataFrame(columns=[
    'flight_id',
    "flight_date",
    "airline",
    "flight_number",
    "dep_airport",
    "dep_delay_time",
    "dep_time",
    "arr_airport",
    "arr_time",
    "flight_status",
    "arr_delay_minutes"
])


records = []

# Fetching data
for idx, flight in enumerate(r.json()['data'], 1):
    records.append({
        "flight_id": idx,
        "flight_date": flight['flight_date'],
        "airline_name": flight['airline']['name'],
        "flight_number": flight['flight']['iata'],
        "dep_airport": flight['departure']['iata'],
        "dep_delay_time": flight['departure']['delay'],
        "dep_time": datetime.strptime(flight['departure']['scheduled'], "%Y-%m-%dT%H:%M:%S%z").time(),
        "arr_airport": flight['arrival']['iata'],
        "arr_time": datetime.strptime(flight['arrival']['scheduled'], "%Y-%m-%dT%H:%M:%S%z").time(),
        "flight_status": flight['flight_status'],
        "arr_delay_minutes": flight['arrival']['delay']
    })

flights_df = pd.DataFrame(records)

# Inserting data into the database
flights_df.to_sql('raw_flights', engine, if_exists='append', index=False)